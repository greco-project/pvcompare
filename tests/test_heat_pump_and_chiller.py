import pytest
import pandas as pd
import numpy as np
import os
from pandas.util.testing import assert_series_equal

from pvcompare import heat_pump_and_chiller as hc
import pvcompare.constants as constants


class TestCalculateCopsAndEers:
    @classmethod
    def setup_class(self):
        self.date_range = pd.date_range("2017", periods=6, freq="H")
        self.weather = pd.DataFrame(
            [11.85, 6.85, 2.0, 0.0, -3.0, 27.0],
            columns=["temp_air"],
            index=self.date_range,
        )
        self.lat = 53.2
        self.lon = 13.2
        self.mvs_inputs_directory = constants.TEST_USER_INPUTS_MVS_SECTOR_COUPLING
        self.user_inputs_pvcompare_directory = constants.TEST_USER_INPUTS_PVCOMPARE

    def test_calculate_cops_and_eers_heat_pump_without_icing(self):
        cops = hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )
        cops_exp = pd.Series(
            [
                3.413615989515072,
                3.018063731170336,
                2.7131135416666665,
                2.604589,
                2.457159433962264,
                5.66215,
            ],
            index=self.date_range,
            name="no_unit",
        )
        assert_series_equal(cops, cops_exp)

    @pytest.fixture(scope="function")
    def add_icing_to_csv(self):
        filename = os.path.join(
            self.user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
        )
        original_data = pd.read_csv(filename, header=0, index_col=0)
        data = original_data.copy()
        data["factor_icing"]["heat_pump"] = 0.8
        data["temp_threshold_icing"]["heat_pump"] = 2
        data.to_csv(filename)
        yield None  # provide the fixture value
        original_data.to_csv(filename)

    def test_calculate_cops_and_eers_heat_pump_consider_icing(self, add_icing_to_csv):
        cops = hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )
        cops_exp = pd.Series(
            [
                3.413615989515072,
                3.018063731170336,
                2.7131135416666665,
                2.0836712,
                1.9657275471698115,
                5.66215,
            ],
            index=self.date_range,
            name="no_unit",
        )

        cops = cops.round(10)
        cops_exp = cops_exp.round(10)
        assert_series_equal(cops, cops_exp)

    def test_calculate_cops_and_eers_chiller(self):
        pass

    def test_calculate_cops_and_eers_misspelled_mode(self):
        with pytest.raises(ValueError):
            hc.calculate_cops_and_eers(
                weather=self.weather,
                lat=self.lat,
                lon=self.lon,
                temperature_col="temp_air",
                mode="misspelled_mode",
                user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
                user_inputs_mvs_directory=self.mvs_inputs_directory,
            )

    def test_calculate_cops_and_eers_saved_file(self):
        hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )
        assert os.path.exists(
            os.path.join(
                self.mvs_inputs_directory,
                "time_series",
                "cops_heat_pump_2017_53.2_13.2_50.0.csv",
            )
        )

    def teardown_method(self):
        # delete file
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2017_53.2_13.2_50.0.csv",
        )
        if os.path.exists(filename):
            os.remove(filename)

    def test_calculate_cops_and_eers_process_temperatures_hp_temp_high(self):
        """
        This tests examine the proper processing of the heat pump's
        high temperature.

        For temp_high it is checked whether it can be passed as
        - numeric or (1)
        - time series. (2)
        - An error is raised if temp_high is empty / NaN. (3)

        In every test, where COPs are calculated, it is checked, whether they are stored in a file
        with temp_high as characteristic value only if temp_high is constant.
        """
        # For convenience reasons of the tests, temp_low will be set to constant value
        temp_low = 10.0

        # (1) temp_high is passed as numeric
        temp_high = 35.0
        filename = os.path.join(
            self.user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
        )
        original_data = pd.read_csv(filename, header=0, index_col=0)
        data = original_data.copy()
        data["temp_high"]["heat_pump"] = temp_high
        data["temp_low"]["heat_pump"] = temp_low
        data.to_csv(filename)
        quality_grade = data["quality_grade"]["heat_pump"]

        cop_calc = hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        cop_ref = np.multiply(
            quality_grade,
            np.divide(np.add(temp_high, 273.15), np.subtract(temp_high, temp_low)),
        )
        cop_ref = np.multiply(cop_ref, np.ones(len(self.weather)))
        cop_ref = pd.Series(cop_ref, index=self.date_range)

        assert_series_equal(cop_calc, cop_ref, check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "cops_heat_pump_2017_53.2_13.2_35.0.csv",
                )
            )
            == True
        )
        original_data.to_csv(filename)

        # (2) temp_high is passed as time series
        temp_high = [35.0, 34.0, 30.0, 29.0, 31.0, 31.5]
        temp_high_df = pd.DataFrame(data={"degC": temp_high})
        temp_high_df.to_csv(
            os.path.join(
                self.user_inputs_pvcompare_directory, "temperatures_heat_pump.csv"
            )
        )

        data["temp_high"][
            "heat_pump"
        ] = "{'file_name': 'temperatures_heat_pump.csv', 'header': 'degC', 'unit': ''}"
        data["temp_low"]["heat_pump"] = temp_low
        data.to_csv(filename)

        cop_calc = hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        cop_ref = np.multiply(
            quality_grade,
            np.divide(np.add(temp_high, 273.15), np.subtract(temp_high, temp_low)),
        )
        cop_ref = np.multiply(cop_ref, np.ones(len(self.weather)))
        cop_ref = pd.Series(cop_ref, index=self.date_range)

        assert_series_equal(cop_calc, cop_ref, check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "cops_heat_pump_2017_53.2_13.2.csv",
                )
            )
            == True
        )
        original_data.to_csv(filename)

        # (3) temp_high is NaN and error is raised
        temp_high = np.nan
        data["temp_high"]["heat_pump"] = temp_high
        data["temp_low"]["heat_pump"] = temp_low
        data.to_csv(filename)

        with pytest.raises(ValueError):
            hc.calculate_cops_and_eers(
                weather=self.weather,
                lat=self.lat,
                lon=self.lon,
                temperature_col="temp_air",
                mode="heat_pump",
                user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
                user_inputs_mvs_directory=self.mvs_inputs_directory,
            )

        original_data.to_csv(filename)

        # Delete files
        filename_1 = "cops_heat_pump_2017_53.2_13.2.csv"
        filename_2 = "cops_heat_pump_2017_53.2_13.2_35.0.csv"

        files = [filename_1, filename_2]
        for file in files:
            filepath = os.path.join(self.mvs_inputs_directory, "time_series", file)
            if os.path.exists(filepath):
                if file != "file_exists.csv":
                    os.remove(filepath)

        filename_3 = "temperatures_heat_pump.csv"
        filepath_3 = os.path.join(self.user_inputs_pvcompare_directory, filename_3)
        if os.path.exists(filepath_3):
            os.remove(filepath_3)

    def test_calculate_cops_and_eers_process_temperatures_hp_temp_low(self):
        """
        This tests examine the proper processing of the heat pump's
        low temperature.

        For temp_low it is checked whether it can be passed as
        - numeric or (has been tested in test_calculate_cops_and_eers_process_temperatures_hp_temp_high() (1))
        - time series or (1)
        - empty / NaN - In this case
            - the ambient temperature should be set as temp_low of an air-air or air-water heat pump (2)
            - the mean yearly ambient temperature should be set as temp_low of a brine-water heat pump (3)


        In every test, where COPs are calculated, it is checked, whether they are stored in a file
        with temp_high as characteristic value only if temp_high is constant.
        """
        # For convenience reasons of the tests, temp-high will be set to constant value
        temp_high = 35.0

        filename = os.path.join(
            self.user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
        )
        original_data = pd.read_csv(filename, header=0, index_col=0)
        data = original_data.copy()
        quality_grade = data["quality_grade"]["heat_pump"]

        # (1) temp_low is passed as time series
        temp_low = [12.0, 11.0, 12.0, 13.0, 11.0, 9.5]
        temp_low_df = pd.DataFrame(data={"degC": temp_low})
        temp_low_df.to_csv(
            os.path.join(
                self.user_inputs_pvcompare_directory, "temperatures_heat_pump.csv"
            )
        )

        data["temp_high"]["heat_pump"] = temp_high
        data["temp_low"][
            "heat_pump"
        ] = "{'file_name': 'temperatures_heat_pump.csv', 'header': 'degC', 'unit': ''}"
        data.to_csv(filename)

        cop_calc = hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        cop_ref = np.multiply(
            quality_grade,
            np.divide(np.add(temp_high, 273.15), np.subtract(temp_high, temp_low)),
        )
        cop_ref = np.multiply(cop_ref, np.ones(len(self.weather)))
        cop_ref = pd.Series(cop_ref, index=self.date_range)

        assert_series_equal(cop_calc, cop_ref, check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "cops_heat_pump_2017_53.2_13.2_35.0.csv",
                )
            )
            == True
        )
        original_data.to_csv(filename)

        # (2) technology is air-air or air-water: temp_low is NaN and equals ambient temperature
        temp_low = np.nan
        data["temp_high"]["heat_pump"] = temp_high
        data["temp_low"]["heat_pump"] = temp_low
        data["technology"]["heat_pump"] = "air-water"
        data.to_csv(filename)

        cop_calc = hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        cop_ref = np.multiply(
            quality_grade,
            np.divide(np.add(temp_high, 273.15), np.subtract(temp_high, self.weather)),
        )

        assert_series_equal(cop_calc, cop_ref["temp_air"], check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "cops_heat_pump_2017_53.2_13.2_35.0.csv",
                )
            )
            == True
        )

        # (3) technology is brine-water: temp_low is NaN and equals mean yearly ambient temperature
        temp_low = np.nan
        data["temp_high"]["heat_pump"] = temp_high
        data["temp_low"]["heat_pump"] = temp_low
        data["technology"]["heat_pump"] = "brine-water"
        data.to_csv(filename)

        cop_calc = hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        mean_temp = np.average(self.weather)
        cop_ref = np.multiply(
            quality_grade,
            np.divide(np.add(temp_high, 273.15), np.subtract(temp_high, mean_temp)),
        )
        cop_ref = np.multiply(cop_ref, np.ones(len(self.weather)))
        cop_ref = pd.Series(cop_ref, index=self.date_range)

        assert_series_equal(cop_calc, cop_ref, check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "cops_heat_pump_2017_53.2_13.2_35.0.csv",
                )
            )
            == True
        )

        original_data.to_csv(filename)

        # Delete files
        filename_1 = "cops_heat_pump_2017_53.2_13.2.csv"
        filename_2 = "cops_heat_pump_2017_53.2_13.2_35.0.csv"

        files = [filename_1, filename_2]
        for file in files:
            filepath = os.path.join(self.mvs_inputs_directory, "time_series", file)
            if os.path.exists(filepath):
                if file != "file_exists.csv":
                    os.remove(filepath)

        filename_3 = "temperatures_heat_pump.csv"
        filepath_3 = os.path.join(self.user_inputs_pvcompare_directory, filename_3)
        if os.path.exists(filepath_3):
            os.remove(filepath_3)

    def test_calculate_cops_and_eers_process_temperatures_chiller_temp_low(self):
        """
        This tests examine the proper processing of the chiller's
        low temperature.

        For temp_low it is checked whether it can be passed as
        - numeric or (1)
        - time series. (2)
        - An error is raised if temp_low is empty / NaN. (3)

        In every test, where EERs are calculated, it is checked, whether they are stored in a file
        with temp_low as characteristic value only if temp_high is constant.
        """
        # For convenience reasons of the tests, temp_high will be set to constant value
        temp_high = 25.0

        # Weather data for chiller
        hot_weather = pd.DataFrame(
            [32, 31.5, 30, 34, 32, 33],
            columns=["temp_air"],
            index=self.date_range,
        )

        # (1) temp_low is passed as numeric
        temp_low = 15.0
        filename = os.path.join(
            self.user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
        )
        original_data = pd.read_csv(filename, header=0, index_col=0)
        data = original_data.copy()
        data["temp_high"]["chiller"] = temp_high
        data["temp_low"]["chiller"] = temp_low
        data.to_csv(filename)
        quality_grade = data["quality_grade"]["chiller"]

        eer_calc = hc.calculate_cops_and_eers(
            weather=hot_weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="chiller",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        eer_ref = np.multiply(
            quality_grade,
            np.divide(np.add(temp_low, 273.15), np.subtract(temp_high, temp_low)),
        )
        eer_ref = np.multiply(eer_ref, np.ones(len(hot_weather)))
        eer_ref = pd.Series(eer_ref, index=self.date_range)

        assert_series_equal(eer_calc, eer_ref, check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "eers_chiller_2017_53.2_13.2_15.0.csv",
                )
            )
            == True
        )
        original_data.to_csv(filename)

        # (2) temp_low is passed as time series
        temp_low = [15.0, 14.0, 14.5, 15.0, 15.5, 13.5]
        temp_low_df = pd.DataFrame(data={"degC": temp_low})
        temp_low_df.to_csv(
            os.path.join(
                self.user_inputs_pvcompare_directory, "temperatures_chiller.csv"
            )
        )

        data["temp_high"]["chiller"] = temp_high
        data["temp_low"][
            "chiller"
        ] = "{'file_name': 'temperatures_chiller.csv', 'header': 'degC', 'unit': ''}"
        data.to_csv(filename)

        eer_calc = hc.calculate_cops_and_eers(
            weather=hot_weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="chiller",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        eer_ref = np.multiply(
            quality_grade,
            np.divide(np.add(temp_low, 273.15), np.subtract(temp_high, temp_low)),
        )
        eer_ref = pd.Series(eer_ref, index=self.date_range)

        assert_series_equal(eer_calc, eer_ref, check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "eers_chiller_2017_53.2_13.2.csv",
                )
            )
            == True
        )
        original_data.to_csv(filename)

        # (3) temp_low is NaN and error is raised
        temp_low = np.nan
        data["temp_high"]["chiller"] = temp_high
        data["temp_low"]["chiller"] = temp_low
        data.to_csv(filename)

        with pytest.raises(ValueError):
            hc.calculate_cops_and_eers(
                weather=hot_weather,
                lat=self.lat,
                lon=self.lon,
                temperature_col="temp_air",
                mode="chiller",
                user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
                user_inputs_mvs_directory=self.mvs_inputs_directory,
            )

        original_data.to_csv(filename)

        # Delete files
        filename_1 = "eers_chiller_2017_53.2_13.2.csv"
        filename_2 = "eers_chiller_2017_53.2_13.2_15.0.csv"

        files = [filename_1, filename_2]
        for file in files:
            filepath = os.path.join(self.mvs_inputs_directory, "time_series", file)
            if os.path.exists(filepath):
                if file != "file_exists.csv":
                    os.remove(filepath)

        filename_3 = "temperatures_chiller.csv"
        filepath_3 = os.path.join(self.user_inputs_pvcompare_directory, filename_3)
        if os.path.exists(filepath_3):
            os.remove(filepath_3)

    def test_calculate_cops_and_eers_process_temperatures_chiller_temp_high(self):
        """
        This tests examine the proper processing of the chiller's
        high temperature.

        For temp_high it is checked whether it can be passed as
        - numeric or (has been tested in test_calculate_cops_and_eers_process_temperatures_chiller_temp_low() (1))
        - time series or (1)
        - empty / NaN - In this case the ambient temperature should be set as temp_high of an air-air chiller (2)

        In every test, where EERs are calculated, it is checked, whether they are stored in a file
        with temp_low as characteristic value only if temp_high is constant.
        """
        # For convenience reasons of the tests, temp-high will be set to constant value
        temp_low = 15.0

        # Weather data for chiller
        hot_weather = pd.DataFrame(
            [32, 31.5, 30, 34, 32, 33],
            columns=["temp_air"],
            index=self.date_range,
        )

        filename = os.path.join(
            self.user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
        )
        original_data = pd.read_csv(filename, header=0, index_col=0)
        data = original_data.copy()
        quality_grade = data["quality_grade"]["chiller"]

        # (1) temp_high is passed as time series
        temp_high = [22.0, 25.0, 28.0, 27.0, 26.5, 24.5]
        temp_high_df = pd.DataFrame(data={"degC": temp_high})
        temp_high_df.to_csv(
            os.path.join(
                self.user_inputs_pvcompare_directory, "temperatures_chiller.csv"
            )
        )

        data["temp_high"][
            "chiller"
        ] = "{'file_name': 'temperatures_chiller.csv', 'header': 'degC', 'unit': ''}"
        data["temp_low"]["chiller"] = temp_low
        data.to_csv(filename)

        eer_calc = hc.calculate_cops_and_eers(
            weather=hot_weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="chiller",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        eer_ref = np.multiply(
            quality_grade,
            np.divide(np.add(temp_low, 273.15), np.subtract(temp_high, temp_low)),
        )
        eer_ref = np.multiply(eer_ref, np.ones(len(hot_weather)))
        eer_ref = pd.Series(eer_ref, index=self.date_range)

        assert_series_equal(eer_calc, eer_ref, check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "eers_chiller_2017_53.2_13.2_15.0.csv",
                )
            )
            == True
        )
        original_data.to_csv(filename)

        # (2) temp_high is NaN and equals ambient temperature
        temp_high = np.nan
        data["temp_high"]["chiller"] = temp_high
        data["temp_low"]["chiller"] = temp_low
        data.to_csv(filename)

        eer_calc = hc.calculate_cops_and_eers(
            weather=hot_weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="chiller",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        eer_ref = np.multiply(
            quality_grade,
            np.divide(np.add(temp_low, 273.15), np.subtract(hot_weather, temp_low)),
        )

        assert_series_equal(eer_calc, eer_ref["temp_air"], check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "eers_chiller_2017_53.2_13.2_15.0.csv",
                )
            )
            == True
        )

        original_data.to_csv(filename)

        # Delete file
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "eers_chiller_2017_53.2_13.2_15.0.csv",
        )
        if os.path.exists(filename):
            os.remove(filename)

        filename_3 = "temperatures_chiller.csv"
        filepath_3 = os.path.join(self.user_inputs_pvcompare_directory, filename_3)
        if os.path.exists(filepath_3):
            os.remove(filepath_3)

    def test_calculate_cops_and_eers_numeric_quality_grade_heat_pump(self):
        """
        This test checks whether the quality grade is processed as intended
        if it is passed as numeric.
        """
        filename = os.path.join(
            self.user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
        )
        original_data = pd.read_csv(filename, header=0, index_col=0)
        data = original_data.copy()
        quality_grade = 0.48
        temp_high = data["temp_high"]["heat_pump"]
        data["quality_grade"]["heat_pump"] = 0.48
        data.to_csv(filename)

        cop_calc = hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )

        cop_exp = np.multiply(
            quality_grade,
            np.divide(np.add(temp_high, 273.15), np.subtract(temp_high, self.weather)),
        )

        assert_series_equal(cop_calc, cop_exp["temp_air"], check_names=False)

        original_data.to_csv(filename)

    def test_calculate_cops_and_eers_default_quality_grade_heat_pump(self):
        """
        With this test it is checked whether the quality grade is set to
        its default value if the technology of the heat pump is passed.
        An error is raised, if the technology and the quality grade are missing.
        This is checked as well.
        """
        filename = os.path.join(
            self.user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
        )
        original_data = pd.read_csv(filename, header=0, index_col=0)
        data = original_data.copy()

        temp_high = data["temp_high"]["heat_pump"]
        mean_temp = np.average(self.weather)

        technologies = ["air-air", "air-water", "brine-water", np.nan]
        quality_grades_of_technologies = [0.1852, 0.403, 0.53, np.nan]

        for item, technology in enumerate(technologies):
            data["quality_grade"]["heat_pump"] = np.nan
            data["technology"]["heat_pump"] = technology
            data.to_csv(filename)

            if not pd.isna(technology):
                cop_calc = hc.calculate_cops_and_eers(
                    weather=self.weather,
                    lat=self.lat,
                    lon=self.lon,
                    temperature_col="temp_air",
                    mode="heat_pump",
                    user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
                    user_inputs_mvs_directory=self.mvs_inputs_directory,
                )
                if technology == "brine-water":
                    cop_exp = np.multiply(
                        quality_grades_of_technologies[item],
                        np.divide(
                            np.add(temp_high, 273.15), np.subtract(temp_high, mean_temp)
                        ),
                    )
                    cop_exp = np.multiply(cop_exp, np.ones(len(self.weather)))
                    cop_exp = pd.Series(cop_exp, index=self.date_range)
                    assert_series_equal(cop_calc, cop_exp, check_names=False)

                else:
                    cop_exp = np.multiply(
                        quality_grades_of_technologies[item],
                        np.divide(
                            np.add(temp_high, 273.15),
                            np.subtract(temp_high, self.weather),
                        ),
                    )
                    assert_series_equal(
                        cop_calc, cop_exp["temp_air"], check_names=False
                    )

            else:
                with pytest.raises(ValueError):
                    hc.calculate_cops_and_eers(
                        weather=self.weather,
                        lat=self.lat,
                        lon=self.lon,
                        temperature_col="temp_air",
                        mode="heat_pump",
                        user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
                        user_inputs_mvs_directory=self.mvs_inputs_directory,
                    )

        original_data.to_csv(filename)

    def test_calculate_cops_and_eers_default_quality_grade_chiller(self):
        """
        With this test it is checked whether the quality grade is set to
        its default value if the technology 'air-air' of the chiller is passed.
        An error is raised, if the technology and the quality grade are missing
        or the quality grade is missing and the technology is either 'air-water'
        or 'brine-water'. These technologies have not been implemented yet.
        This is checked as well.
        """
        # Weather data for chiller
        hot_weather = pd.DataFrame(
            [32, 31.5, 30, 34, 32, 33],
            columns=["temp_air"],
            index=self.date_range,
        )

        filename = os.path.join(
            self.user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
        )
        original_data = pd.read_csv(filename, header=0, index_col=0)
        data = original_data.copy()
        temp_low = data["temp_low"]["chiller"]

        technologies = ["air-air", "air-water", "brine-water", np.nan]
        quality_grades_of_technologies = [0.3, np.nan, np.nan, np.nan]

        for item, technology in enumerate(technologies):
            data["quality_grade"]["chiller"] = np.nan
            data["technology"]["chiller"] = technology
            data.to_csv(filename)

            if not pd.isna(technology):
                if technology == "air-air":
                    eer_calc = hc.calculate_cops_and_eers(
                        weather=hot_weather,
                        lat=self.lat,
                        lon=self.lon,
                        temperature_col="temp_air",
                        mode="chiller",
                        user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
                        user_inputs_mvs_directory=self.mvs_inputs_directory,
                    )

                    eer_exp = np.multiply(
                        quality_grades_of_technologies[item],
                        np.divide(
                            np.add(temp_low, 273.15), np.subtract(hot_weather, temp_low)
                        ),
                    )
                    assert_series_equal(
                        eer_calc, eer_exp["temp_air"], check_names=False
                    )

                elif technology == "air-water" or "brine-water":
                    with pytest.raises(ValueError):
                        eer_calc = hc.calculate_cops_and_eers(
                            weather=hot_weather,
                            lat=self.lat,
                            lon=self.lon,
                            temperature_col="temp_air",
                            mode="chiller",
                            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
                            user_inputs_mvs_directory=self.mvs_inputs_directory,
                        )

            else:
                with pytest.raises(ValueError):
                    eer_calc = hc.calculate_cops_and_eers(
                        weather=hot_weather,
                        lat=self.lat,
                        lon=self.lon,
                        temperature_col="temp_air",
                        mode="chiller",
                        user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
                        user_inputs_mvs_directory=self.mvs_inputs_directory,
                    )

        original_data.to_csv(filename)

        # Delete file
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "eers_chiller_2017_53.2_13.2_16.0.csv",
        )
        if os.path.exists(filename):
            os.remove(filename)


class TestAddSectorCoupling:
    @classmethod
    def setup_class(self):
        self.weather = pd.DataFrame(
            [10.0, 5.0, 0.0, -3.0, 27.0],
            columns=["temp_air"],
            index=pd.date_range("2017", periods=5, freq="H"),
        )
        self.weather_2019 = pd.DataFrame(
            [12.0, 9.0, 0.0, -5.0, 28.0],
            columns=["temp_air"],
            index=pd.date_range("2019", periods=5, freq="H"),
        )
        self.lat = 53.2
        self.lon = 13.2
        self.mvs_inputs_directory = constants.TEST_USER_INPUTS_MVS_SECTOR_COUPLING
        self.filename_conversion = os.path.join(
            self.mvs_inputs_directory, "csv_elements", "energyConversion.csv"
        )
        self.user_inputs_pvcompare_directory = constants.TEST_USER_INPUTS_PVCOMPARE

    @pytest.fixture(scope="class", autouse=True)
    def select_conv_tech(self):
        def _select_columns(columns):
            data = pd.DataFrame(original_data[columns])
            data.to_csv(self.filename_conversion)

        original_data = pd.read_csv(self.filename_conversion, header=0, index_col=0)
        yield _select_columns
        original_data.to_csv(self.filename_conversion)

    def test_add_sector_coupling_heat_pump_file_already_exists(self, select_conv_tech):
        select_conv_tech(columns="heat_pump_file_exists")

        original_data_conversion = pd.read_csv(
            self.filename_conversion, header=0, index_col=0
        )

        hc.add_sector_coupling(
            weather=self.weather_2019,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
            overwrite_hp_parameters=False,
        )
        # no file created
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2017_53.2_13.2_50.0.csv",
        )
        assert os.path.exists(filename) == False
        # filename in energyConversion.csv does not change
        df = pd.read_csv(self.filename_conversion, header=0, index_col=0)
        assert ("file_exists.csv" in df.loc["efficiency"].heat_pump_file_exists) == True

        original_data_conversion.to_csv(self.filename_conversion, na_rep="NaN")

    def test_add_sector_coupling_heat_pump_file_already_exists_overwrite_True(
        self, select_conv_tech
    ):
        select_conv_tech(columns="heat_pump_file_exists")

        original_data_conversion = pd.read_csv(
            self.filename_conversion, header=0, index_col=0
        )

        hc.add_sector_coupling(
            weather=self.weather_2019,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
            overwrite_hp_parameters=True,
        )
        # no file created
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2019_53.2_13.2_50.0.csv",
        )
        assert os.path.exists(filename) == True
        # filename in energyConversion.csv does not change
        df = pd.read_csv(self.filename_conversion, header=0, index_col=0)
        assert (
            "cops_heat_pump_2019_53.2_13.2_50.0.csv"
            in df.loc["efficiency"].heat_pump_file_exists
        ) == True

        original_data_conversion.to_csv(self.filename_conversion, na_rep="NaN")

    def test_add_sector_coupling_heat_pump_file_created(self, select_conv_tech):
        select_conv_tech(columns="heat_pump_file_non_existent")

        original_data_conversion = pd.read_csv(
            self.filename_conversion, header=0, index_col=0
        )

        hc.add_sector_coupling(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
            overwrite_hp_parameters=False,
        )
        # file created
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2017_53.2_13.2_50.0.csv",
        )
        assert os.path.exists(filename) == True
        # filename in energyConversion.csv changed
        df = pd.read_csv(self.filename_conversion, header=0, index_col=0)
        assert (
            "cops_heat_pump_2017_53.2_13.2_50.0.csv"
            in df.loc["efficiency"].heat_pump_file_non_existent
        ) == True

        original_data_conversion.to_csv(self.filename_conversion, na_rep="NaN")

    def test_add_sector_coupling_heat_pump_constant_efficiency(self, select_conv_tech):
        select_conv_tech(columns="heat_pump_constant_eff")

        original_data_conversion = pd.read_csv(
            self.filename_conversion, header=0, index_col=0
        )

        hc.add_sector_coupling(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
            overwrite_hp_parameters=False,
        )
        # no file created
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2017_53.2_13.2_50.0.csv",
        )
        assert os.path.exists(filename) == False
        # check efficiency
        df = pd.read_csv(self.filename_conversion, header=0, index_col=0)
        assert float(df.loc["efficiency"].heat_pump_constant_eff) == 0.9

        original_data_conversion.to_csv(self.filename_conversion, na_rep="NaN")

    def test_add_sector_coupling_multiple_heat_pumps(self):
        pass

    def test_add_sector_coupling_warning_no_heat_demand_in_energy_consumption(
        self,
    ):
        pass

    def test_add_sector_coupling_no_warning(self):
        pass

    def test_add_sector_coupling_chiller_warning_no_file_created(self):
        pass

    # todo test add_sector_coupling() with other names for Electricity bus

    def teardown_method(self):
        # delete file
        filename_1 = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2017_53.2_13.2_50.0.csv",
        )
        filename_2 = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2019_53.2_13.2_50.0.csv",
        )

        files = [filename_1, filename_2]

        for file in files:
            if os.path.exists(file):
                os.remove(file)
