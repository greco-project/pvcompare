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
    create_si_timeseries
)


class TestPvTimeSeries:

    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        temperature = np.array([[5.0], [6.0]])
        pressure = np.array([[101125], [101000]])
        wind_speed_10m = np.array([[2.0], [2.5]])
        dhi = np.array([[80.0], [85.0]])
        dirhi = np.array([[0.1], [0.3]])
        ghi = np.array([[80.1], [85.3]])
        # dni = np.array([[1.0], [1.3]])
        self.weather = pd.DataFrame(
            np.hstack(
                (
                    temperature,  # temp_air
                    pressure,  # P
                    wind_speed_10m,
                    dhi,
                    dirhi,
                    ghi,
                )
            ),
            index=[0, 1],
            columns=[
                np.array(
                    [
                        "temp_air",
                        "P",
                        "wind_speed",
                        "dhi",
                        "dirhi",
                        "ghi",
                    ]
                )])

    def test_create_normalized_SI_timeseries(self):
        # time_series = create_normalized_SI_timeseries(
        #     lat=52.111130, lon=12.480622, weather=self.weather,
        #     surface_azimuth=0, surface_tilt=30)
        # todo complete after function is fixed
        print(self.weather) # todo delete this line
        pass


# # one can test that exception are raised
# def test_addition_wrong_argument_number():
#     with pytest.raises(TypeError):
#         assert addition(2) == 2  # pylint: disable=E1120
