"""
run these tests with `pytest tests/name_of_test_module.py` or `pytest tests`
or simply `pytest` pytest will look for all files starting with "test_" and run
all functions within this file starting with "test_". For basic example of
tests you can look at our workshop
https://github.com/rl-institut/workshop/tree/master/test-driven-development.
Otherwise https://docs.pytest.org/en/latest/ and
https://docs.python.org/3/library/unittest.html are also good support.
"""

import pandas as pd
import os

from pvcompare.demand import (
    calculate_power_demand,
    shift_working_hours,
    get_workalendar_class
)


class TestDemandProfiles:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        self.country='Spain'
        self.population=4800
        self.year=2014
        self.input_directory=\
            os.path.join(os.path.dirname(__file__), "data/inputs/")
        self.mvs_input_directory=os.path.join(
    os.path.dirname(__file__), "data/mvs_inputs/")
        self.plot=True

        ts = pd.DataFrame()
        ts['h0'] = [19052, 19052, 14289, 19052, 19052, 14289]
        ts.index = ["2014-01-01 13:30:00+00:00", "2014-01-01 14:00:00+00:00",
                    "2014-01-01 14:30:00+00:00", "2014-01-02 13:30:00+00:00",
                    "2014-01-02 14:00:00+00:00",
                    "2014-01-02 14:30:00+00:00"]
        ts.index = pd.to_datetime(ts.index)


        self.ts=ts


    # def test_calculate_power_demand(self):
    #
    #
    #     calculate_power_demand(
    #         country=self.country, population=self.population, year=self.year,
    #         input_directory=self.input_directory,
    #         mvs_input_directory=self.mvs_input_directory, plot=self.plot)


    def test_shift_working_hours(self):

        output=shift_working_hours(country=self.country, ts=self.ts)

        assert output['h0'].sum() == 109549.0


    def test_workalendar_class(self):

        cal=get_workalendar_class(self.country)

        assert cal.__class__.__name__ == 'Spain'