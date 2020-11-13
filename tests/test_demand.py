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
import numpy as np

from pvcompare.demand import (
    calculate_power_demand,
    shift_working_hours,
    get_workalendar_class,
    calculate_heat_demand,
    adjust_heat_demand,
)


class TestDemandProfiles:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        self.country = "France"
        self.population = 4800
        self.year = 2015
        self.test_input_directory = os.path.join(
            os.path.dirname(__file__), "test_data/test_pvcompare_inputs"
        )
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
        weather_df.index = ["2014-01-01 13:00:00+00:00", "2014-01-01 14:00:00+00:00"]
        weather_df.index = pd.to_datetime(weather_df.index)
        self.weather = weather_df

        bp = pd.read_csv(
            os.path.join(self.test_input_directory, "building_parameters.csv"),
            index_col=0,
        )
        self.heating_lim_temp = pd.to_numeric(
            bp.at["heating limit temperature", "value"], errors="coerce"
        )
        self.include_ww = eval(bp.at["include warm water", "value"])

        heating = pd.DataFrame()
        periods = 48
        heating["Time"] = pd.date_range("1/1/2020", periods=periods, freq="H")
        heating["Load"] = np.random.choice(np.arange(10000, 90000, 10), periods)
        temp_low = np.ones(int(periods / 2)) * (self.heating_lim_temp - 1)
        temp_high = np.ones(int(periods / 2)) * self.heating_lim_temp
        heating["temp_air"] = np.append(temp_low, temp_high)
        self.heating = heating

    def test_power_demand_exists(self):

        filename = f"electricity_load_{self.country}_{self.population}_{self.year}.csv"
        if os.path.exists(
            os.path.join(self.test_mvs_directory, "time_series", filename)
        ):
            os.remove(os.path.join(self.test_mvs_directory, "time_series", filename))
        calculate_power_demand(
            country=self.country,
            population=self.population,
            year=self.year,
            input_directory=self.test_input_directory,
            mvs_input_directory=self.test_mvs_directory,
            column="demand_01",
        )
        assert os.path.exists(
            os.path.join(self.test_mvs_directory, "time_series", filename)
        )

    def test_calculate_power_demand(self):

        a = calculate_power_demand(
            country=self.country,
            population=self.population,
            year=self.year,
            input_directory=self.test_input_directory,
            mvs_input_directory=self.test_mvs_directory,
            column="demand_01",
        )

        assert a["kWh"].sum() == 32666542.239902988

    def test_heat_demand_exists(self):

        filename = f"heat_load_{self.country}_{self.population}_{self.year}.csv"
        if os.path.exists(
            os.path.join(self.test_mvs_directory, "time_series", filename)
        ):
            os.remove(os.path.join(self.test_mvs_directory, "time_series", filename))

        calculate_heat_demand(
            country=self.country,
            population=self.population,
            year=self.year,
            input_directory=self.test_input_directory,
            weather=self.weather,
            mvs_input_directory=self.test_mvs_directory,
            column="demand_02",
        )
        assert os.path.exists(
            os.path.join(self.test_mvs_directory, "time_series", filename)
        )

    def test_calculate_heat_demand(self):

        a = calculate_heat_demand(
            country=self.country,
            population=self.population,
            year=self.year,
            input_directory=self.test_input_directory,
            weather=self.weather,
            mvs_input_directory=self.test_mvs_directory,
            column="demand_02",
        )

        if not self.include_ww:
            assert a["kWh"].sum() == 10969639.113628691
        else:
            assert a["kWh"].sum() == 11984233.752677418

    def test_adjust_heat_demand(self):

        result = adjust_heat_demand(
            temperature=self.heating["temp_air"],
            heating_limit_temp=self.heating_lim_temp,
            demand=self.heating["Load"],
        )

        assert result.sum() == self.heating["Load"].sum()
        assert result.iloc[24:].sum() == 0

    def test_shift_working_hours(self):

        output = shift_working_hours(country=self.country, ts=self.ts)

        assert output["h0"].sum() == 104786

    def test_workalendar_class(self):

        cal = get_workalendar_class(self.country)

        assert cal.__class__.__name__ == "France"
