import pytest
import pandas as pd
import numpy as np
import os
from pvcompare import stratified_thermal_storage as sts
from pvcompare.constants import TEST_DATA_HEAT


class TestCalcStratTesParam:
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
        self.losses = pd.DataFrame(
            [0.00158, 0.00159, 0.0016, 0.00161, 0.00159, 0.0016],
            columns=["no_unit"],
            index=self.date_range,
        )

    def test_calc_strat_tes_param(self):
        (
            nominal_storage_capacity,
            loss_rate,
            fixed_losses_relative,
            fixed_losses_absolute,
        ) = sts.calc_strat_tes_param(
            weather=self.weather,
            temperature_col="temp_air",
            input_directory=TEST_DATA_HEAT,
            mvs_input_directory=TEST_DATA_HEAT,
        )
        results_rel_losses = [
            0.00126941,
            0.00140123,
            0.0015291,
            0.00158182,
            0.00166092,
            0.00087,
        ]
        results_abs_losses = [
            2.61418842e-05,
            2.81328884e-05,
            3.00641624e-05,
            3.08605640e-05,
            3.20551665e-05,
            2.01091417e-05,
        ]

        assert loss_rate == 0.00092273109671008
        for item, value in enumerate(fixed_losses_relative):
            assert np.round(value, 7) == np.round(results_rel_losses[item], 7)
        for item, value in enumerate(fixed_losses_absolute):
            assert np.round(value, 7) == np.round(results_abs_losses[item], 7)

    def test_calculate_losses_saved_file(self):
        sts.add_strat_tes(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            storage_csv="storage_02.csv",
            input_directory=TEST_DATA_HEAT,
            mvs_input_directory=TEST_DATA_HEAT,
        )
        assert os.path.exists(
            os.path.join(
                TEST_DATA_HEAT,
                "time_series",
                "fixed_thermal_losses_absolute_2018_53.2_13.2.csv",
            )
        )
        assert os.path.exists(
            os.path.join(
                TEST_DATA_HEAT,
                "time_series",
                "fixed_thermal_losses_relative_2018_53.2_13.2.csv",
            )
        )

    def test_save_time_dependent_values(self):
        file_name = "fixed_thermal_losses_relative_test.csv"
        file_path = os.path.join(TEST_DATA_HEAT, "time_series", file_name)
        sts.save_time_dependent_values(
            self.losses,
            "fixed_thermal_losses_relative",
            "no_unit",
            file_name,
            os.path.join(TEST_DATA_HEAT, "time_series"),
        )

        assert os.path.exists(file_path) == True

    def teardown_method(self):
        # delete file
        filename = os.path.join(
            TEST_DATA_HEAT, "time_series", "fixed_thermal_losses_relative_test.csv"
        )

        if os.path.exists(filename):
            os.remove(filename)


class TestAddStratTes:
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
        self.filename_storage_02 = os.path.join(
            TEST_DATA_HEAT, "csv_elements", "storage_02.csv"
        )

    @pytest.fixture(scope="class", autouse=True)
    def select_conv_tech(self):
        def _select_columns(columns):
            data = pd.DataFrame(original_data[columns])
            data.to_csv(self.filename_storage_02)

        original_data = pd.read_csv(self.filename_storage_02, header=0, index_col=0)
        yield _select_columns
        original_data.to_csv(self.filename_storage_02)

    def test_add_sector_coupling_strat_tes_file_already_exists(self, select_conv_tech):
        select_conv_tech(columns="storage capacity")
        sts.add_strat_tes(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            storage_csv="storage_02.csv",
            input_directory=TEST_DATA_HEAT,
            mvs_input_directory=TEST_DATA_HEAT,
        )
        # no file created
        filename = os.path.join(
            TEST_DATA_HEAT,
            "time_series",
            "fixed_thermal_losses_absolute_2018_53.2_13.2.csv",
        )
        assert os.path.exists(filename) == True
        # filename in storage_02.csv does not change
        df = pd.read_csv(self.filename_storage_02, header=0, index_col=0)
        assert (
            "fixed_thermal_losses_absolute_2018_53.2_13.2.csv"
            in df.loc["abs_thermal_losses"].item()
        ) == True

    def teardown_method(self):
        # delete file
        filename_1 = os.path.join(
            TEST_DATA_HEAT,
            "time_series",
            "fixed_thermal_losses_absolute_2018_53.2_13.2.csv",
        )
        filename_2 = os.path.join(
            TEST_DATA_HEAT,
            "time_series",
            "fixed_thermal_losses_relative_2018_53.2_13.2.csv",
        )
        if os.path.exists(filename_1):
            os.remove(filename_1)
        if os.path.exists(filename_2):
            os.remove(filename_2)


class TestAddStratTes_file_non_existent:
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
        self.filename_storage_02 = os.path.join(
            TEST_DATA_HEAT, "csv_elements", "storage_02.csv"
        )

    @pytest.fixture(scope="class", autouse=True)
    def select_conv_tech(self):
        def _select_columns(columns):
            data = pd.DataFrame(original_data[columns])
            data.to_csv(self.filename_storage_02)

        original_data = pd.read_csv(self.filename_storage_02, header=0, index_col=0)
        yield _select_columns
        original_data.to_csv(self.filename_storage_02)

    def test_add_sector_coupling_strat_tes_file_non_existent(self, select_conv_tech):
        select_conv_tech(columns="storage capacity")
        sts.add_strat_tes(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            storage_csv="storage_02.csv",
            input_directory=TEST_DATA_HEAT,
            mvs_input_directory=TEST_DATA_HEAT,
        )
        # no file created
        filename = os.path.join(
            TEST_DATA_HEAT,
            "time_series",
            "fixed_thermal_losses_absolute_2018_53.2_13.2.csv",
        )
        assert os.path.exists(filename) == False
        # filename in storage_02.csv does not change
        df = pd.read_csv(self.filename_storage_02, header=0, index_col=0)
        assert (
            "fixed_thermal_losses_absolute_2017_53.2_13.2.csv"
            in df.loc["abs_thermal_losses"].item()
        ) == True

    def teardown_method(self):
        # delete file
        filename_1 = os.path.join(
            TEST_DATA_HEAT,
            "time_series",
            "fixed_thermal_losses_absolute_2017_53.2_13.2.csv",
        )
        filename_2 = os.path.join(
            TEST_DATA_HEAT,
            "time_series",
            "fixed_thermal_losses_relative_2017_53.2_13.2.csv",
        )
        if os.path.exists(filename_1):
            os.remove(filename_1)
        if os.path.exists(filename_2):
            os.remove(filename_2)


class TestAddStratTes_file_constant_losses:
    @classmethod
    def setup_class(self):
        self.date_range = pd.date_range("2016", periods=6, freq="H")
        self.weather = pd.DataFrame(
            [11.85, 6.85, 2.0, 0.0, -3.0, 27.0],
            columns=["temp_air"],
            index=self.date_range,
        )
        self.lat = 53.2
        self.lon = 13.2
        self.filename_storage_02 = os.path.join(
            TEST_DATA_HEAT, "csv_elements", "storage_02_const_losses.csv"
        )

    @pytest.fixture(scope="class", autouse=True)
    def select_conv_tech(self):
        def _select_columns(columns):
            data = pd.DataFrame(original_data[columns])
            data.to_csv(self.filename_storage_02)

        original_data = pd.read_csv(self.filename_storage_02, header=0, index_col=0)
        yield _select_columns
        original_data.to_csv(self.filename_storage_02)

    def test_add_sector_coupling_strat_tes_file_const_losses(self, select_conv_tech):
        select_conv_tech(columns="storage capacity")
        sts.add_strat_tes(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            storage_csv="storage_02_const_losses.csv",
            input_directory=TEST_DATA_HEAT,
            mvs_input_directory=TEST_DATA_HEAT,
        )
        # no file created
        filename = os.path.join(
            TEST_DATA_HEAT,
            "time_series",
            "fixed_thermal_losses_absolute_2018_53.2_13.2.csv",
        )

        assert os.path.exists(filename) == False
        # check efficiency
        df = pd.read_csv(self.filename_storage_02, header=0, index_col=0)
        assert float(df.loc["efficiency"].item()) == 0.99907726890329
        assert float(df.loc["rel_thermal_losses"].item()) == 0.0016
        assert float(df.loc["abs_thermal_losses"].item()) == 0.0003
