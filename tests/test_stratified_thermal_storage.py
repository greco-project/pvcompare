import pytest
import pandas as pd
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

    def test_calc_strat_tes_param(self):
        (
            nominal_storage_capacity,
            loss_rate,
            fixed_losses_relative,
            fixed_losses_absolute,
        ) = sts.calc_strat_tes_param(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mvs_input_directory=TEST_DATA_HEAT,
        )

        assert loss_rate == 0.00092273109671008
        # todo: Check also other calculated values

    def test_calculate_cops_and_eers_saved_file(self):
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
                TEST_DATA_HEAT, "time_series", "fixed_losses_absolute_2018_53.2_13.2.csv"
            )
        )
        assert os.path.exists(
            os.path.join(
                TEST_DATA_HEAT, "time_series", "fixed_losses_relative_2018_53.2_13.2.csv"
            )
        )


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
            TEST_DATA_HEAT, "csv_elements", "storage_02.csv")

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
            TEST_DATA_HEAT, "time_series", "fixed_losses_absolute_2018_53.2_13.2.csv"
        )
        assert os.path.exists(filename) == True
        # filename in storage_02.csv does not change
        df = pd.read_csv(self.filename_storage_02, header=0, index_col=0)
        assert ("fixed_losses_absolute_2018_53.2_13.2.csv" in df.loc["abs_losses"].item()) == True

    def teardown_method(self):
        # delete file
        filename_1 = os.path.join(
            TEST_DATA_HEAT, "time_series", "fixed_losses_absolute_2018_53.2_13.2.csv"
        )
        filename_2 = os.path.join(
            TEST_DATA_HEAT, "time_series", "fixed_losses_relative_2018_53.2_13.2.csv"
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
            TEST_DATA_HEAT, "csv_elements", "storage_02.csv")

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
            TEST_DATA_HEAT, "time_series", "fixed_losses_absolute_2018_53.2_13.2.csv"
        )
        assert os.path.exists(filename) == False
        # filename in storage_02.csv does not change
        df = pd.read_csv(self.filename_storage_02, header=0, index_col=0)
        assert ("fixed_losses_absolute_2017_53.2_13.2.csv" in df.loc["abs_losses"].item()) == True

    def teardown_method(self):
        # delete file
        filename_1 = os.path.join(
            TEST_DATA_HEAT, "time_series", "fixed_losses_absolute_2017_53.2_13.2.csv"
        )
        filename_2 = os.path.join(
            TEST_DATA_HEAT, "time_series", "fixed_losses_relative_2017_53.2_13.2.csv"
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
            TEST_DATA_HEAT, "csv_elements", "storage_02_const_losses.csv")

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
            TEST_DATA_HEAT, "time_series", "fixed_losses_absolute_2018_53.2_13.2.csv"
        )
        assert os.path.exists(filename) == False
        # check efficiency
        df = pd.read_csv(self.filename_storage_02, header=0, index_col=0)
        assert float(df.loc["rel_losses"].item()) == 0.0016
        assert float(df.loc["abs_losses"].item()) == 0.0003
