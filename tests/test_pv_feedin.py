"""
run these tests with `pytest tests/name_of_test_module.py` or `pytest tests`
or simply `pytest` pytest will look for all files starting with "test_" and run
all functions within this file starting with "test_". For basic example of
tests you can look at our workshop
https://github.com/rl-institut/workshop/tree/master/test-driven-development.
Otherwise https://docs.pytest.org/en/latest/ and
https://docs.python.org/3/library/unittest.html are also good support.
"""

import pytest
import pandas as pd
import numpy as np

from pvcompare.pv_feedin import (
    create_si_timeseries,
    nominal_values_pv,
    create_cpv_timeseries,
    get_optimal_pv_angle,
)


class TestPvTimeSeries:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        weather_df = pd.DataFrame()
        weather_df["temp_air"] = [4, 5]
        weather_df["wind_speed"] = [2, 2.5]
        weather_df["dhi"] = [100, 120]
        weather_df["dni"] = [120, 150]
        weather_df["ghi"] = [200, 220]
        weather_df.index = ["2014-01-01 13:00:00+00:00", "2014-01-01 14:00:00+00:00"]
        weather_df.index = pd.to_datetime(weather_df.index)
        self.weather = weather_df

        self.lat = 40.0
        self.lon = 5.2
        self.surface_azimuth = 180
        self.surface_tilt = 30

    def test_create_si_timeseries(self):

        ts = create_si_timeseries(
            lat=self.lat,
            lon=self.lon,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalized=True,
        )
        output = ts.sum()

        assert output == 0.4477100404694223

    def test_nominal_values_pv(self):

        technology = "si"
        area = 1000

        nominal_value = nominal_values_pv(
            technology=technology,
            area=area,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            cpvtype="m300"
        )

        assert nominal_value == 129.134

    def test_create_cpv_timeseries(self):


        ts = create_cpv_timeseries(lat=self.lat, lon=self.lon,
                                   weather=self.weather,
                              surface_azimuth=self.surface_azimuth,
                              surface_tilt=self.surface_tilt, normalized=True,
                                   cpvtype="m300")
        output = ts.sum()
        assert output == 0.1351719011687128

    def test_get_optimal_pv_angle(self):

        output= get_optimal_pv_angle(self.lat)

        assert output == 25


# # one can test that exception are raised
# def test_addition_wrong_argument_number():
#     with pytest.raises(TypeError):
#         assert addition(2) == 2  # pylint: disable=E1120
