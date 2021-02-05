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
        self.date_range = pd.date_range("2018", periods=6, freq="H")
        self.weather = pd.DataFrame(
            [11.85, 6.85, 2.0, 0.0, -3.0, 27.0],
            columns=["temp_air"],
            index=self.date_range,
        )
        self.lat = 53.2
        self.lon = 13.2
        self.mvs_inputs_directory = constants.TEST_USER_INPUTS_MVS
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
                4.65885529157667388489,
                3.83134991119005308136,
                3.26825757575757558371,
                3.08149999999999968381,
                2.83822368421052617649,
                13.48156249999999900524,
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
                4.658855291576674,
                3.831349911190053,
                3.268257575757576,
                2.465199999999999,
                2.270578947368421,
                13.481562499999999,
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
                "cops_heat_pump_2018_53.2_13.2_35.0.csv",
            )
        )

    def teardown_method(self):
        # delete file
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2018_53.2_13.2_35.0.csv",
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
                    "cops_heat_pump_2018_53.2_13.2_35.0.csv",
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
                    "cops_heat_pump_2018_53.2_13.2.csv",
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
        filename_1 = "cops_heat_pump_2018_53.2_13.2.csv"
        filename_2 = "cops_heat_pump_2018_53.2_13.2_35.0.csv"

        files = [filename_1, filename_2]
        for file in files:
            filepath = os.path.join(self.mvs_inputs_directory, "time_series", file)
            if os.path.exists(filepath):
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
        - empty / NaN - In this case the ambient temperature should
          be set as temp_low (2)

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
                    "cops_heat_pump_2018_53.2_13.2_35.0.csv",
                )
            )
            == True
        )
        original_data.to_csv(filename)

        # (2) temp_low is NaN and equals ambient temperature
        temp_low = np.nan
        data["temp_high"]["heat_pump"] = temp_high
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
            np.divide(np.add(temp_high, 273.15), np.subtract(temp_high, self.weather)),
        )

        assert_series_equal(cop_calc, cop_ref["temp_air"], check_names=False)
        assert (
            os.path.exists(
                os.path.join(
                    self.mvs_inputs_directory,
                    "time_series",
                    "cops_heat_pump_2018_53.2_13.2_35.0.csv",
                )
            )
            == True
        )

        original_data.to_csv(filename)

        # Delete files
        filename_1 = "cops_heat_pump_2018_53.2_13.2.csv"
        filename_2 = "cops_heat_pump_2018_53.2_13.2_35.0.csv"

        files = [filename_1, filename_2]
        for file in files:
            filepath = os.path.join(self.mvs_inputs_directory, "time_series", file)
            if os.path.exists(filepath):
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
            [32, 31.5, 30, 34, 32, 33], columns=["temp_air"], index=self.date_range,
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
                    "eers_chiller_2018_53.2_13.2_15.0.csv",
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
                    "eers_chiller_2018_53.2_13.2.csv",
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
        filename_1 = "eers_chiller_2018_53.2_13.2.csv"
        filename_2 = "eers_chiller_2018_53.2_13.2_15.0.csv"

        files = [filename_1, filename_2]
        for file in files:
            filepath = os.path.join(self.mvs_inputs_directory, "time_series", file)
            if os.path.exists(filepath):
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
        - empty / NaN - In this case the ambient temperature should
          be set as temp_high (2)

        In every test, where EERs are calculated, it is checked, whether they are stored in a file
        with temp_low as characteristic value only if temp_high is constant.
        """
        # For convenience reasons of the tests, temp-high will be set to constant value
        temp_low = 15.0

        # Weather data for chiller
        hot_weather = pd.DataFrame(
            [32, 31.5, 30, 34, 32, 33], columns=["temp_air"], index=self.date_range,
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
                    "eers_chiller_2018_53.2_13.2_15.0.csv",
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
                    "eers_chiller_2018_53.2_13.2_15.0.csv",
                )
            )
            == True
        )

        original_data.to_csv(filename)

        # Delete file
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "eers_chiller_2018_53.2_13.2_15.0.csv",
        )
        if os.path.exists(filename):
            os.remove(filename)

        filename_3 = "temperatures_chiller.csv"
        filepath_3 = os.path.join(self.user_inputs_pvcompare_directory, filename_3)
        if os.path.exists(filepath_3):
            os.remove(filepath_3)


class TestAddSectorCoupling:
    @classmethod
    def setup_class(self):
        self.weather = pd.DataFrame(
            [10.0, 5.0, 0.0, -3.0, 27.0],
            columns=["temp_air"],
            index=pd.date_range("2018", periods=5, freq="H"),
        )
        self.lat = 53.2
        self.lon = 13.2
        self.mvs_inputs_directory = constants.TEST_USER_INPUTS_MVS
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
        hc.add_sector_coupling(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )
        # no file created
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2018_53.2_13.2_35.0.csv",
        )
        assert os.path.exists(filename) == False
        # filename in energyConversion.csv does not change
        df = pd.read_csv(self.filename_conversion, header=0, index_col=0)
        assert ("file_exists.csv" in df.loc["efficiency"].heat_pump_file_exists) == True

    def test_add_sector_coupling_heat_pump_file_created(self, select_conv_tech):
        select_conv_tech(columns="heat_pump_file_non_existent")
        hc.add_sector_coupling(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )
        # file created
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2018_53.2_13.2_35.0.csv",
        )
        assert os.path.exists(filename) == True
        # filename in energyConversion.csv changed
        df = pd.read_csv(self.filename_conversion, header=0, index_col=0)
        assert (
            "cops_heat_pump_2018_53.2_13.2_35.0.csv"
            in df.loc["efficiency"].heat_pump_file_non_existent
        ) == True

    def test_add_sector_coupling_heat_pump_constant_efficiency(self, select_conv_tech):
        select_conv_tech(columns="heat_pump_constant_eff")
        hc.add_sector_coupling(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.mvs_inputs_directory,
        )
        # no file created
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2018_53.2_13.2_35.0.csv",
        )
        assert os.path.exists(filename) == False
        # check efficiency
        df = pd.read_csv(self.filename_conversion, header=0, index_col=0)
        assert float(df.loc["efficiency"].heat_pump_constant_eff) == 0.9

    def test_add_sector_coupling_multiple_heat_pumps(self):
        pass

    def test_add_sector_coupling_warning_no_heat_demand_in_energy_consumption(self,):
        pass

    def test_add_sector_coupling_no_warning(self):
        pass

    def test_add_sector_coupling_chiller_warning_no_file_created(self):
        pass

    # todo test add_sector_coupling() with other names for Electricity bus

    def teardown_method(self):
        # delete file
        filename = os.path.join(
            self.mvs_inputs_directory,
            "time_series",
            "cops_heat_pump_2018_53.2_13.2_35.0.csv",
        )
        if os.path.exists(filename):
            os.remove(filename)
