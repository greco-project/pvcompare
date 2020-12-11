"""
run these tests with `pytest tests/name_of_test_module.py` or `pytest tests`
or simply `pytest` pytest will look for all files starting with "test_" and run
all functions within this file starting with "test_". For basic example of
tests you can look at our workshop
https://github.com/rl-institut/workshop/tree/master/test-driven-development.
Otherwise https://docs.pytest.org/en/latest/ and
https://docs.python.org/3/library/unittest.html are also good support.
"""

import os
import pandas as pd
import pytest
import logging
from pvcompare.outputs import plot_all_flows, plot_kpi_loop
from pvcompare import constants
from pvcompare.main import apply_mvs


class TestPlotProfiles:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        self.scenario_name = "Test_scenario_main"
        self.output_directory = constants.TEST_DATA_OUTPUT
        self.mvs_output_directory = os.path.join(
            self.output_directory, self.scenario_name, "mvs_outputs"
        )
        self.mvs_input_directory = os.path.join(
            constants.TEST_DATA_DIRECTORY, "test_mvs_inputs_main"
        )

        weather_df = pd.DataFrame()
        weather_df["temp_air"] = [25, 30]
        weather_df["wind_speed"] = [2, 2.5]
        weather_df["dhi"] = [100, 120]
        weather_df["dni"] = [700, 150]
        weather_df["ghi"] = [800, 220]
        weather_df["precipitable_water"] = [1, 2]
        weather_df.index = ["2014-07-01 13:00:00+00:00", "2014-07-01 14:00:00+00:00"]
        weather_df.index = pd.to_datetime(weather_df.index, utc=True)
        self.test_mvs_directory = os.path.join(
            os.path.dirname(__file__), "test_data/test_mvs_inputs"
        )
        self.weather = weather_df

        self.population = 4600
        self.lat = 40.0
        self.lon = 5.2
        self.surface_azimuth = 180
        self.surface_tilt = 30
        self.year = 2015

    def test_apply_mvs_output_directory(self):
        """ """
        apply_mvs(
            scenario_name=self.scenario_name,
            mvs_input_directory=self.mvs_input_directory,
            mvs_output_directory=None,
            output_directory=self.output_directory,
        )

        assert os.path.exists(self.mvs_output_directory)
