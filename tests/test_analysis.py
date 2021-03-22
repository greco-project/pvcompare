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
from pvcompare.analysis import loop_mvs
from pvcompare import constants
import glob
import shutil


class TestPlotProfiles:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        self.scenario_name = "Test_Scenario"
        self.outputs_directory = constants.TEST_OUTPUTS_DIRECTORY
        self.mvs_output_directory = os.path.join(
            self.outputs_directory, self.scenario_name, "mvs_outputs"
        )
        self.timeseries_directory = os.path.join(
            self.mvs_output_directory, "/timeseries/"
        )
        self.storeys = 5
