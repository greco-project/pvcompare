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
import os
from pvcompare import constants
from pvcompare.perosi.pvlib_smarts import SMARTSSpectra

from pvcompare.perosi.perosi import (
    calculate_smarts_parameters,
    create_pero_si_timeseries,
)

from pvcompare.cpv.apply_cpvlib_StaticHybridSystem import create_cpv_time_series


class TestPvtime_series:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        weather_df = pd.DataFrame()
        weather_df["temp_air"] = [4, 5]
        weather_df["wind_speed"] = [2, 2.5]
        weather_df["dhi"] = [100, 120]
        weather_df["dni"] = [120, 150]
        weather_df["ghi"] = [200, 220]
        weather_df["precipitable_water"] = [1, 2]
        weather_df.index = pd.date_range(start='2014-08-01 09:00',
                                         freq='H', periods=2, tz='Europe/Berlin')
        self.test_mvs_directory = os.path.join(
            os.path.dirname(__file__), "test_data/test_mvs_inputs"
        )
        self.weather = weather_df

        self.population = 4600
        self.lat = 40.0
        self.lon = 5.2
        self.surface_azimuth = 180
        self.surface_tilt = 30
        self.year = 2014

    def test_smarts_spectra(self):

        # def SMARTSSpectra(IOUT, YEAR, MONTH, DAY, HOUR, LATIT, LONGIT, WLMN, 'WLMX', 'TAIR', 'TDAY', 'SEASON', 'ZONE', 'TILT', and 'WAZIM')
        df = SMARTSSpectra(
            "2 3",
            str(self.year),
            "8",
            "1",
            "9",
            str(self.lat),
            str(self.lon),
            "400",
            "1200",
            "15",
            "10",
            "SUMMER",
            "1",
            str(self.surface_tilt),
            str(self.surface_azimuth),
        )

        assert df["Direct_normal_irradiance"].sum() == 750.29952

    def test_calculate_smarts_parameters(self):

        output = calculate_smarts_parameters(
            year=self.year,
            lat=self.lat,
            lon=self.lon,
            number_hours=2,
            cell_type=["Chen_pero"],
            surface_tilt=self.surface_tilt,
            surface_azimuth=self.surface_azimuth,
            atmos_data=self.weather,
            WLMN=350,
            WLMX=1200,
        )

        assert output["Jsc_Chen_pero"].sum() == 0.009034273174998176

    def test_create_perosi_timeseries(self):

        output = create_pero_si_timeseries(
            year=self.year,
            lat=self.lat,
            lon=self.lon,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            number_hours=2,
            atmos_data=self.weather,
            psi_type="Chen",
        )

        sum = output.sum()
        assert sum == 57.81695705506873

    def test_create_cpv_time_series(self):

        output = create_cpv_time_series(
            lat=self.lat,
            lon=self.lon,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
        )

        sum = output.sum()

        assert sum == 3.2195140126743436
