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

class TestBenchmarkApplyPvcompare():
    @classmethod
    def setup_class(self):
    # DEFINE USER INPUTS
        self.latitude = 52.5243700  # Madrid: 40.416775 # berlin: 52.5243700 oslo: 59.9127300 athens: 37.983810, Paris: 48.864716
        self.longitude = 13.4105300  # M: -3.703790 # berlin 13.4105300 oslo:10.7460900 	athens: 23.727539, paris: 2.349014
        self.year = 2014
        self.storeys = 5
        self.country = "Germany"
        self.scenario_name = "Scenario_A1"

        # DEFAULT PARAMETERS
        self.user_inputs_pvcompare_directory = os.path.join(
    os.path.dirname(__file__), "data_benchmark_tests/user_inputs_apply_pvcompare/pvcompare_inputs/"
)
        self.static_inputs_directory = None
        self.user_inputs_mvs_directory = os.path.join(
    os.path.dirname(__file__), "data_benchmark_tests/user_inputs_apply_pvcompare/mvs_inputs/"
)
        self.pv_setup = None
        self.outputs_directory = os.path.join(
    os.path.dirname(__file__), "data_benchmark_tests/outputs")

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
            plot=False,
            pv_setup=self.pv_setup,
            overwrite_grid_costs=True,
            overwrite_pv_parameters=True,
            )

        assert os.path.isfile(os.path.join(self.user_inputs_mvs_directory, "time_series" , "si_180_38_2014_52.52437_13.41053.csv"))

    @mock.patch("argparse.ArgumentParser.parse_args",
                return_value=argparse.Namespace())
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
            plot=False,
            pv_setup=self.pv_setup,
            overwrite_grid_costs=True,
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
        directory = os.path.join(
            self.user_inputs_mvs_directory,
            "time_series"
        )
        filelist = glob.glob(os.path.join(directory, "*.csv"))
        for f in filelist:
            os.remove(f)

        scenario_folder = os.path.join(self.outputs_directory, self.scenario_name)
        shutil.rmtree(scenario_folder)

# RUN MVS OEMOF SIMULATTION
# main.apply_mvs(
#     scenario_name=scenario_name,
#     output_directory=outputs_directory,
#     user_inputs_mvs_directory=user_inputs_mvs_directory,
# )

