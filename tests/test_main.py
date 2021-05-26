"""
run these tests with `pytest tests/name_of_test_module.py` or `pytest tests`
or simply `pytest` pytest will look for all files starting with "test_" and run
all functions within this file starting with "test_". For basic example of
tests you can look at our workshop
https://github.com/rl-institut/workshop/tree/master/test-driven-development.
Otherwise https://docs.pytest.org/en/latest/ and
https://docs.python.org/3/library/unittest.html are also good support.
"""

import pvcompare.main as main
import os
import glob
import argparse
import mock
import shutil
import pytest
import pandas as pd

import pvcompare.constants as constants

TESTS_ON_MASTER = "master"
EXECUTE_TESTS_ON = os.environ.get("EXECUTE_TESTS_ON", "skip")


class TestMain:
    @classmethod
    def setup_class(self):
        # DEFINE USER INPUTS
        self.latitude = 52.5243700  # Madrid: 40.416775 # berlin: 52.5243700 oslo: 59.9127300 athens: 37.983810, Paris: 48.864716
        self.longitude = 13.4105300  # M: -3.703790 # berlin 13.4105300 oslo:10.7460900 	athens: 23.727539, paris: 2.349014
        self.year = 2017
        self.storeys = 5
        self.country = "Germany"
        self.scenario_name = "Scenario_MAIN"

        # DEFAULT PARAMETERS
        self.user_inputs_pvcompare_directory = os.path.join(
            os.path.dirname(__file__), "data_test_main/user_inputs/pvcompare_inputs/"
        )
        self.static_inputs_directory = constants.DEFAULT_STATIC_INPUTS_DIRECTORY
        self.test_static_inputs_directory = os.path.join(
            os.path.dirname(__file__), "data/static_inputs/"
        )
        self.user_inputs_mvs_directory = os.path.join(
            os.path.dirname(__file__), "data_test_main/user_inputs/mvs_inputs/"
        )
        self.outputs_directory = os.path.join(
            os.path.dirname(__file__), "data_test_main/outputs"
        )
        self.user_inputs_collection_mvs = os.path.join(
            os.path.dirname(__file__), "data/user_inputs_collection/mvs_inputs/"
        )

    # RUN PVCOMPARE PRE-CALCULATIONS:
    # - calculate PV timeseries
    # - if sectorcoupling: calculate heat pump generation
    # - calculate electricity and heat demand

    def test_apply_pvcompare(self):

        main.apply_pvcompare(
            storeys=self.storeys,
            country=self.country,
            latitude=self.latitude,
            longitude=self.longitude,
            year=self.year,
            static_inputs_directory=self.static_inputs_directory,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            collections_mvs_inputs_directory=self.user_inputs_collection_mvs,
            plot=False,
            pv_setup=None,
            overwrite_grid_parameters=True,
            overwrite_pv_parameters=True,
        )

        assert os.path.isfile(
            os.path.join(
                self.user_inputs_mvs_directory,
                "time_series",
                "si_180_38_2017_52.52437_13.41053.csv",
            )
        )

    def test_apply_pvcompare_add_weather_file(self):
        # delete file
        directory = os.path.join(self.user_inputs_mvs_directory, "time_series")
        filelist = glob.glob(os.path.join(directory, "*.csv"))
        for f in filelist:
            os.remove(f)

        weather_file = os.path.join(
            self.test_static_inputs_directory, "weatherdata_53.2_13.2_2017.csv"
        )

        main.apply_pvcompare(
            storeys=self.storeys,
            country=self.country,
            latitude=self.latitude,
            longitude=self.longitude,
            year=self.year,
            static_inputs_directory=self.static_inputs_directory,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            collections_mvs_inputs_directory=self.user_inputs_collection_mvs,
            plot=False,
            pv_setup=None,
            overwrite_grid_parameters=True,
            overwrite_pv_parameters=True,
            add_weather_file=weather_file,
        )

        assert os.path.isfile(
            os.path.join(
                self.user_inputs_mvs_directory,
                "time_series",
                "si_180_38_2017_52.52437_13.41053.csv",
            )
        )

    def test_apply_pvcompare_add_demands(self):
        # delete file
        directory = os.path.join(self.user_inputs_mvs_directory, "time_series")
        filelist = glob.glob(os.path.join(directory, "*.csv"))
        for f in filelist:
            os.remove(f)

        filename_electricity_demand = os.path.join(
            self.user_inputs_mvs_directory,
            "predefined_time_series/electricity_load_2015_France_5.csv",
        )

        main.apply_pvcompare(
            storeys=self.storeys,
            country=self.country,
            latitude=self.latitude,
            longitude=self.longitude,
            year=self.year,
            static_inputs_directory=self.static_inputs_directory,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            collections_mvs_inputs_directory=self.user_inputs_collection_mvs,
            plot=False,
            pv_setup=None,
            overwrite_grid_parameters=True,
            overwrite_pv_parameters=True,
            add_heat_demand=None,
            add_electricity_demand=filename_electricity_demand,
        )

        energyConsumption = pd.read_csv(
            os.path.join(
                self.user_inputs_mvs_directory, "csv_elements/energyConsumption.csv"
            ),
            index_col=0,
            header=0,
        )
        assert (
            energyConsumption.at["file_name", "Electricity demand"]
            == filename_electricity_demand
        )

    def test_apply_pvcompare_add_pv_timeseries(self):

        filename_pv_timeseries = os.path.join(
            self.user_inputs_mvs_directory,
            "predefined_time_series/si_180_38_2012_52.52437_13.41053.csv",
        )

        main.apply_pvcompare(
            storeys=self.storeys,
            country=self.country,
            latitude=self.latitude,
            longitude=self.longitude,
            year=self.year,
            static_inputs_directory=self.static_inputs_directory,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            collections_mvs_inputs_directory=self.user_inputs_collection_mvs,
            plot=False,
            pv_setup=None,
            overwrite_grid_parameters=True,
            overwrite_pv_parameters=False,
            add_pv_timeseries={
                "si": {
                    "filename": filename_pv_timeseries,
                    "module_size": 1,
                    "module_peak_power": 50,
                    "surface_type": "flat_roof",
                }
            },
        )

        energyProduction = pd.read_csv(
            os.path.join(
                self.user_inputs_mvs_directory, "csv_elements/energyProduction.csv"
            ),
            index_col=0,
            header=0,
        )
        assert energyProduction.at["file_name", "PV si"] == filename_pv_timeseries

    def test_apply_pvcompare_add_sam_si_module(self):

        main.apply_pvcompare(
            storeys=self.storeys,
            country=self.country,
            latitude=self.latitude,
            longitude=self.longitude,
            year=self.year,
            static_inputs_directory=self.static_inputs_directory,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            collections_mvs_inputs_directory=self.user_inputs_collection_mvs,
            plot=False,
            pv_setup=None,
            overwrite_grid_parameters=True,
            overwrite_pv_parameters=False,
            add_sam_si_module={"cecmod": "Advance_Solar_Hydro_Wind_Power_API_180"},
        )

        energyProduction = pd.read_csv(
            os.path.join(
                self.user_inputs_mvs_directory, "csv_elements/energyProduction.csv"
            ),
            index_col=0,
            header=0,
        )
        assert float(energyProduction.at["maximumCap", "PV si"]) == 27790.992

    # this ensures that the test is only run if explicitly executed, i.e. not when the
    # `pytest` command alone is called
    @pytest.mark.skipif(
        EXECUTE_TESTS_ON not in (TESTS_ON_MASTER),
        reason="Benchmark test deactivated, set env variable "
        "EXECUTE_TESTS_ON to 'master' to run this test",
    )
    @mock.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace())
    def test_apply_mvs(self, margs):
        """ """

        main.apply_pvcompare(
            storeys=self.storeys,
            country=self.country,
            latitude=self.latitude,
            longitude=self.longitude,
            year=self.year,
            static_inputs_directory=self.static_inputs_directory,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            collections_mvs_inputs_directory=self.user_inputs_collection_mvs,
            plot=False,
            pv_setup=None,
            overwrite_grid_parameters=True,
            overwrite_pv_parameters=True,
        )

        main.apply_mvs(
            scenario_name=self.scenario_name,
            outputs_directory=self.outputs_directory,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
        )

        assert os.path.isdir(os.path.join(self.outputs_directory, self.scenario_name))

    def teardown_method(self):
        # delete file
        directory = os.path.join(self.user_inputs_mvs_directory, "time_series")
        filelist = glob.glob(os.path.join(directory, "*.csv"))
        for f in filelist:
            os.remove(f)

        scenario_folder = os.path.join(self.outputs_directory, self.scenario_name)
        if os.path.exists(scenario_folder):
            shutil.rmtree(scenario_folder, ignore_errors=True)
