import pytest
import pandas as pd
import numpy as np
import os
import pvcompare.constants as constants
import pvcompare.main as main
import argparse
import mock
import shutil
from pvcompare import stratified_thermal_storage as sts
from pvcompare.constants import TEST_USER_INPUTS_MVS
from pvcompare.constants import TEST_USER_INPUTS_PVCOMPARE

EXECUTE_TESTS_ON = os.environ.get("EXECUTE_TESTS_ON", "skip")
EXECUTE_TESTS_ON = "master"
TESTS_ON_MASTER = "master"


class TestTES:
    @classmethod
    def setup_class(self):
        self.country = "Germany"
        self.year = 2017
        self.lat = 53.2
        self.lon = 13.2
        self.storeys = 5
        self.user_inputs_mvs_directory = constants.TEST_USER_INPUTS_MVS
        self.user_inputs_pvcompare_directory = constants.TEST_USER_INPUTS_PVCOMPARE
        self.static_inputs_directory = constants.TEST_STATIC_INPUTS
        self.outputs_directory = constants.TEST_OUTPUTS_DIRECTORY
        self.scenario_name = "Test_Scenario_TES"
        self.scenario_name_with_TES_bus = "Test_Scenario_TES_with_TES_bus"

        self.pv_setup = pd.read_csv(
            os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv"),
            header=0,
            index_col="technology",
        )
        try:
            self.pv_setup = self.pv_setup.drop(["cpv", "psi"])
            self.pv_setup.reset_index(drop=False, inplace=True)
        except KeyError:
            print(
                "Please check the format of pv_setup.csv file. The tests might not run correctly."
            )

        # Save original states of csvs
        self.mvs_csv_inputs_path = os.path.join(
            self.user_inputs_mvs_directory, "csv_elements"
        )
        self.energy_production_original = pd.read_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyProduction.csv"),
            header=0,
            index_col=0,
        )
        self.energy_storage_original = pd.read_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyStorage.csv"),
            header=0,
            index_col=0,
        )
        self.storage_xx_original = pd.read_csv(
            os.path.join(self.mvs_csv_inputs_path, "storage_TES.csv"),
            header=0,
            index_col=0,
        )
        self.energy_conversion_original = pd.read_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyConversion.csv"),
            header=0,
            index_col=0,
        )
        self.energy_busses_original = pd.read_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyBusses.csv"),
            header=0,
            index_col=0,
        )

    # # this ensure that the test is only ran if explicitly executed, ie not when the `pytest` command
    # # alone is called
    @pytest.mark.skipif(
        EXECUTE_TESTS_ON not in (TESTS_ON_MASTER),
        reason="Benchmark test deactivated, set env variable "
        "EXECUTE_TESTS_ON to 'master' to run this test",
    )
    @mock.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace())
    def test_implementations_tes(self, margs):
        """
        This test checks if the results of two different ways of implementing a stratified
        thermal storage match.
        You can include a stratified thermal storage in the model using two ways:

        1. With storage component with `inflow_direction` and `outflow_direction` to the heat bus
        2. With a storage bus, a storage component and `inflow_direction` and `outflow_direction`
            as Transformer feeding in and from that bus
            Please note that the cost parameters of `inflow_direction` and `outflow_direction` of
            the Transformer should be set to zero, since they cannot be assigned to a real plant
            component with cost parameters
        Parameters
        ----------
        margs

        """
        # Simulation of first way of implementation
        main.apply_pvcompare(
            storeys=self.storeys,
            country=self.country,
            latitude=self.lat,
            longitude=self.lon,
            year=self.year,
            static_inputs_directory=self.static_inputs_directory,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            plot=False,
            pv_setup=self.pv_setup,
            overwrite_grid_costs=True,
            overwrite_pv_parameters=True,
        )

        # RUN MVS OEMOF SIMULATTION
        main.apply_mvs(
            scenario_name=self.scenario_name,
            outputs_directory=self.outputs_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
        )

        # Read results of simulation with first way of implementation
        results_storage_heat_bus = pd.read_excel(
            os.path.join(
                self.outputs_directory,
                self.scenario_name,
                "mvs_outputs",
                "timeseries_all_busses.xlsx",
            ),
            sheet_name="Heat bus",
        )

        # Revert changes made in storage_xx.csv file
        self.storage_xx_original.to_csv(
            os.path.join(self.mvs_csv_inputs_path, "storage_TES.csv"), na_rep="NaN"
        )

        # Calculated files in time_series directory need to be deleted to ensure
        # the next simulation is run completely
        time_series_directory = os.path.join(
            self.user_inputs_mvs_directory, "time_series"
        )
        time_series = os.listdir(time_series_directory)
        for file_name in time_series:
            if file_name != "file_exists.csv":
                os.remove(os.path.join(time_series_directory, file_name))

        # Modify mvs csv input data as a preparation for the simulation of
        # the second way of implementation (see below)

        # Add "TES bus" to busses
        energy_busses = self.energy_busses_original.copy()
        energy_busses["TES bus"] = "Heat"
        energy_busses.to_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyBusses.csv"), na_rep="NaN"
        )
        # Add TES input and output converter to transformers
        energy_conversion = self.energy_conversion_original.copy()
        energy_conversion["TES converter in"] = [
            "kW",
            "True",
            "None",
            0,
            0,
            30,
            0,
            0,
            0,
            0,
            1,
            "Heat bus",
            "TES bus",
            "Heat",
            "transformer",
        ]
        energy_conversion["TES converter out"] = [
            "kW",
            "True",
            "None",
            0,
            0,
            30,
            0,
            0,
            0,
            0,
            1,
            "TES bus",
            "Heat bus",
            "Heat",
            "transformer",
        ]
        energy_conversion.to_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyConversion.csv"), na_rep="NaN"
        )
        # Adapt inflow and outflow direction of storage to "TES bus"
        energy_storage = self.energy_storage_original.copy()
        energy_storage.at["inflow_direction", "storage_TES"] = "TES bus"
        energy_storage.at["outflow_direction", "storage_TES"] = "TES bus"
        energy_storage.to_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyStorage.csv"), na_rep="NaN"
        )

        # Simulation of second way of implementation
        main.apply_pvcompare(
            storeys=self.storeys,
            country=self.country,
            latitude=self.lat,
            longitude=self.lon,
            year=self.year,
            static_inputs_directory=self.static_inputs_directory,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            plot=False,
            pv_setup=self.pv_setup,
            overwrite_grid_costs=True,
            overwrite_pv_parameters=True,
        )

        # RUN MVS OEMOF SIMULATTION
        main.apply_mvs(
            scenario_name=self.scenario_name_with_TES_bus,
            outputs_directory=self.outputs_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
        )

        # Read results of simulation with second way of implementation
        results_storage_tes_bus = pd.read_excel(
            os.path.join(
                self.outputs_directory,
                self.scenario_name_with_TES_bus,
                "mvs_outputs",
                "timeseries_all_busses.xlsx",
            ),
            sheet_name="Heat bus",
        )

        # Assert that results of both implementations match
        assert (
            results_storage_heat_bus["TES input power"].values.all()
            == results_storage_tes_bus["TES converter in"].values.all()
        )
        assert (
            results_storage_heat_bus["TES output power"].values.all()
            == results_storage_tes_bus["TES converter out"].values.all()
        )

        # Revert changes made in mvs csv input files
        self.storage_xx_original.to_csv(
            os.path.join(self.mvs_csv_inputs_path, "storage_TES.csv"), na_rep="NaN"
        )
        self.energy_busses_original.to_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyBusses.csv"), na_rep="NaN"
        )
        self.energy_conversion_original.to_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyConversion.csv"), na_rep="NaN"
        )
        self.energy_storage_original.to_csv(
            os.path.join(self.mvs_csv_inputs_path, "energyStorage.csv"), na_rep="NaN"
        )

    def teardown_method(self):
        # delete directory
        scenarios = [self.scenario_name, self.scenario_name_with_TES_bus]
        for scenario in scenarios:
            outputs_directory = os.path.join(self.outputs_directory, scenario)
            if os.path.exists(outputs_directory):
                shutil.rmtree(outputs_directory)


class TestCalcStratTesParam:
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
            user_inputs_pvcompare_directory=TEST_USER_INPUTS_PVCOMPARE,
            user_inputs_mvs_directory=TEST_USER_INPUTS_MVS,
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
            user_inputs_pvcompare_directory=TEST_USER_INPUTS_PVCOMPARE,
            user_inputs_mvs_directory=TEST_USER_INPUTS_MVS,
        )
        assert os.path.exists(
            os.path.join(
                TEST_USER_INPUTS_MVS,
                "time_series",
                "fixed_thermal_losses_absolute_2017_53.2_13.2_95.0.csv",
            )
        )
        assert os.path.exists(
            os.path.join(
                TEST_USER_INPUTS_MVS,
                "time_series",
                "fixed_thermal_losses_relative_2017_53.2_13.2_95.0.csv",
            )
        )

    def test_save_time_dependent_values(self):
        file_name = "fixed_thermal_losses_relative_test.csv"
        file_path = os.path.join(TEST_USER_INPUTS_MVS, "time_series", file_name)
        sts.save_time_dependent_values(
            self.losses,
            "fixed_thermal_losses_relative",
            "no_unit",
            file_name,
            os.path.join(TEST_USER_INPUTS_MVS, "time_series"),
        )

        assert os.path.exists(file_path) == True

    def teardown_method(self):
        # delete file
        filename = os.path.join(
            TEST_USER_INPUTS_MVS,
            "time_series",
            "fixed_thermal_losses_relative_test.csv",
        )

        if os.path.exists(filename):
            os.remove(filename)


class TestAddStratTes:
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
        self.filename_storage_xx = os.path.join(
            TEST_USER_INPUTS_MVS, "csv_elements", "storage_TES.csv"
        )

    @pytest.fixture(scope="class", autouse=True)
    def select_conv_tech(self):
        def _select_columns(columns):
            data = pd.DataFrame(original_data[columns])
            data.to_csv(self.filename_storage_xx, na_rep="NaN")

        original_data = pd.read_csv(self.filename_storage_xx, header=0, index_col=0)
        yield _select_columns
        original_data.to_csv(self.filename_storage_xx, na_rep="NaN")

    def test_add_sector_coupling_strat_tes_file_already_exists(self, select_conv_tech):
        select_conv_tech(columns="storage capacity")
        sts.add_strat_tes(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=TEST_USER_INPUTS_PVCOMPARE,
            user_inputs_mvs_directory=TEST_USER_INPUTS_MVS,
        )
        # no file created
        filename = os.path.join(
            TEST_USER_INPUTS_MVS,
            "time_series",
            "fixed_thermal_losses_absolute_2017_53.2_13.2_95.0.csv",
        )
        assert os.path.exists(filename) == True
        # filename in storage_TES.csv does not change
        df = pd.read_csv(self.filename_storage_xx, header=0, index_col=0)
        assert (
            "fixed_thermal_losses_absolute_2017_53.2_13.2_95.0.csv"
            in df.loc["fixed_thermal_losses_absolute"].item()
        ) == True

    def teardown_method(self):
        # delete file
        filename_1 = os.path.join(
            TEST_USER_INPUTS_MVS,
            "time_series",
            "fixed_thermal_losses_absolute_2017_53.2_13.2_95.0.csv",
        )
        filename_2 = os.path.join(
            TEST_USER_INPUTS_MVS,
            "time_series",
            "fixed_thermal_losses_relative_2017_53.2_13.2_95.0.csv",
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
        self.filename_storage_xx = os.path.join(
            TEST_USER_INPUTS_MVS, "csv_elements", "storage_TES.csv"
        )

    @pytest.fixture(scope="class", autouse=True)
    def select_conv_tech(self):
        def _select_columns(columns):
            data = pd.DataFrame(original_data[columns])
            data.to_csv(self.filename_storage_xx, na_rep="NaN")

        original_data = pd.read_csv(self.filename_storage_xx, header=0, index_col=0)
        yield _select_columns
        original_data.to_csv(self.filename_storage_xx, na_rep="NaN")

    def test_add_sector_coupling_strat_tes_file_non_existent(self, select_conv_tech):
        select_conv_tech(columns="storage capacity")
        sts.add_strat_tes(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=TEST_USER_INPUTS_PVCOMPARE,
            user_inputs_mvs_directory=TEST_USER_INPUTS_MVS,
        )
        # no file created
        filename = os.path.join(
            TEST_USER_INPUTS_MVS,
            "time_series",
            "fixed_thermal_losses_absolute_2018_53.2_13.2_95.0.csv",
        )
        assert os.path.exists(filename) == False
        # filename in storage_TES.csv does not change
        df = pd.read_csv(self.filename_storage_xx, header=0, index_col=0)
        assert (
            "fixed_thermal_losses_absolute_2017_53.2_13.2_95.0.csv"
            in df.loc["fixed_thermal_losses_absolute"].item()
        ) == True

    def teardown_method(self):
        # delete file
        filename_1 = os.path.join(
            TEST_USER_INPUTS_MVS,
            "time_series",
            "fixed_thermal_losses_absolute_2017_53.2_13.2_95.0.csv",
        )
        filename_2 = os.path.join(
            TEST_USER_INPUTS_MVS,
            "time_series",
            "fixed_thermal_losses_relative_2017_53.2_13.2_95.0.csv",
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
        self.filename_storage_TES = os.path.join(
            TEST_USER_INPUTS_MVS, "csv_elements", "storage_TES_const_losses.csv"
        )

    @pytest.fixture(scope="class", autouse=True)
    def select_conv_tech(self):
        def _select_columns(columns):
            data = pd.DataFrame(original_data[columns])
            data.to_csv(self.filename_storage_TES, na_rep="NaN")

        original_data = pd.read_csv(self.filename_storage_TES, header=0, index_col=0)
        yield _select_columns
        original_data.to_csv(self.filename_storage_TES, na_rep="NaN")

    def test_add_sector_coupling_strat_tes_file_const_losses(self, select_conv_tech):
        energy_storage_file_path = os.path.join(
            TEST_USER_INPUTS_MVS, "csv_elements", "energyStorage.csv"
        )
        energy_storage_original = pd.read_csv(
            energy_storage_file_path, header=0, index_col=0
        )
        energy_storage = energy_storage_original.copy()
        energy_storage.at[
            "storage_filename", "storage_TES"
        ] = "storage_TES_const_losses.csv"
        energy_storage.to_csv(energy_storage_file_path, na_rep="NaN")
        select_conv_tech(columns="storage capacity")
        sts.add_strat_tes(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            user_inputs_pvcompare_directory=TEST_USER_INPUTS_PVCOMPARE,
            user_inputs_mvs_directory=TEST_USER_INPUTS_MVS,
        )
        # no file created
        filename = os.path.join(
            TEST_USER_INPUTS_MVS,
            "time_series",
            "fixed_thermal_losses_absolute_2017_53.2_13.2_95.0.csv",
        )

        assert os.path.exists(filename) == False
        # check efficiency
        df = pd.read_csv(self.filename_storage_TES, header=0, index_col=0)
        assert float(df.loc["efficiency"].item()) == 0.99907726890329
        assert float(df.loc["fixed_thermal_losses_relative"].item()) == 0.0016
        assert float(df.loc["fixed_thermal_losses_absolute"].item()) == 0.0003

        energy_storage_original.to_csv(energy_storage_file_path, na_rep="NaN")
