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
