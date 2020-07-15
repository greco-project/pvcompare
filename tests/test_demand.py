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
    get_workalendar_class,
    calculate_heat_demand,
)
from pvcompare import constants


class TestDemandProfiles:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        self.country = "Spain"
        self.population = 4800
        self.year = 2014
        self.input_directory = constants.DEFAULT_INPUT_DIRECTORY
        self.test_mvs_directory = os.path.join(
            os.path.dirname(__file__), "test_data/test_mvs_inputs"
        )

        ts = pd.DataFrame()
        ts["h0"] = [19052, 19052, 14289, 19052, 19052, 14289]
        ts.index = [
            "2014-01-01 13:30:00+00:00",
            "2014-01-01 14:00:00+00:00",
            "2014-01-01 14:30:00+00:00",
            "2014-01-01 15:00:00+00:00",
            "2014-01-01 15:30:00+00:00",
            "2014-01-01 16:00:00+00:00",
        ]
        ts.index = pd.to_datetime(ts.index)
        self.ts = ts

        weather_df = pd.DataFrame()
        weather_df["temp_air"] = [4, 5]
        weather_df["wind_speed"] = [2, 2.5]
        weather_df["dhi"] = [100, 120]
        weather_df["dni"] = [120, 150]
        weather_df["ghi"] = [200, 220]
        weather_df.index = [
            "2014-01-01 13:00:00+00:00",
            "2014-01-01 14:00:00+00:00",
        ]
        weather_df.index = pd.to_datetime(weather_df.index)
        self.weather = weather_df

    def test_power_demand_exists(self):

        if os.path.exists(
            os.path.join(
                self.test_mvs_directory, "time_series/electricity_load.csv"
            )
        ):
            os.remove(
                os.path.join(
                    self.test_mvs_directory, "time_series/electricity_load.csv"
                )
            )
        calculate_power_demand(
            country=self.country,
            population=self.population,
            year=self.year,
            input_directory=self.input_directory,
            mvs_input_directory=self.test_mvs_directory,
        )
        assert os.path.exists(
            os.path.join(
                self.test_mvs_directory, "time_series/electricity_load.csv"
            )
        )

    def test_calculate_power_demand(self):

        a = calculate_power_demand(
            country=self.country,
            population=self.population,
            year=self.year,
            input_directory=self.input_directory,
            mvs_input_directory=self.test_mvs_directory,
        )

        assert a["h0"].sum() == 17.65950917551695

    def test_heat_demand_exists(self):

        if os.path.exists(
            os.path.join(self.test_mvs_directory, "time_series/heat_load.csv")
        ):
            os.remove(
                os.path.join(
                    self.test_mvs_directory, "time_series/heat_load.csv"
                )
            )

        calculate_heat_demand(
            country=self.country,
            population=self.population,
            year=self.year,
            input_directory=self.input_directory,
            weather=self.weather,
            mvs_input_directory=self.test_mvs_directory,
        )
        assert os.path.exists(
            os.path.join(self.test_mvs_directory, "time_series/heat_load.csv")
        )

    def test_calculate_heat_demand(self):

        a = calculate_heat_demand(
            country=self.country,
            population=self.population,
            year=self.year,
            input_directory=self.input_directory,
            weather=self.weather,
            mvs_input_directory=self.test_mvs_directory,
        )

        assert a["h0"].sum() == 5.474071970330192

    def test_shift_working_hours(self):

        output = shift_working_hours(country=self.country, ts=self.ts)

        a = output["h0"].sum()

        assert output["h0"].sum() == 104786

    def test_workalendar_class(self):

        cal = get_workalendar_class(self.country)

        assert cal.__class__.__name__ == "Spain"
