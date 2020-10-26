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
from pvcompare.pv_feedin import (
    create_pv_components,
    create_si_time_series,
    create_psi_time_series,
    nominal_values_pv,
    create_cpv_time_series,
    get_optimal_pv_angle,
    calculate_NREA_peak,
    get_peak,
)


class TestPvtime_series:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
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

    def test_nominal_values_pv(self):

        technology = "si"
        area = 1000

        nominal_value = nominal_values_pv(
            technology=technology,
            area=area,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            psi_type="Chen",
        )

        assert nominal_value == 170.337

    def test_create_si_times_eries(self):

        ts = create_si_time_series(
            lat=self.lat,
            lon=self.lon,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalization=None,
        )
        output = round(ts.values.sum(), 3)
        assert output == 0.216

    def test_create_si_times_eries__NREF_normalization(self):

        ts = create_si_time_series(
            lat=self.lat,
            lon=self.lon,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalization="NREF",
        )
        output = round(ts.values.sum(), 3)
        assert output == 0.773

    def test_create_si_times_eries__NREA_normalization(self):

        ts = create_si_time_series(
            lat=self.lat,
            lon=self.lon,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalization="NREA",
        )
        output = round(ts.values.sum(), 3)
        assert output == 1.011

    def test_create_cpv_time_series(self):

        ts = create_cpv_time_series(
            lat=self.lat,
            lon=self.lon,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalization=None,
        )
        output = ts.sum()
        assert round(output, 2) == 0.02

    def test_create_cpv_time_series_NREF_normalization(self):

        ts = create_cpv_time_series(
            lat=self.lat,
            lon=self.lon,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalization="NREF",
        )
        output = ts.sum()
        assert round(output, 2) == 0.61

    def test_create_cpv_time_series_NREA_normalization(self):

        ts = create_cpv_time_series(
            lat=self.lat,
            lon=self.lon,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalization="NREA",
        )
        output = ts.sum()
        assert round(output, 2) == 0.81

    def test_get_optimal_pv_angle(self):

        output = get_optimal_pv_angle(self.lat)

        assert output == 25

    def test_create_psi_time_series(self):
        ts = create_psi_time_series(
            lat=self.lat,
            lon=self.lon,
            year=self.year,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalization=None,
            psi_type="Chen",
        )
        output = ts.sum()
        assert round(output, 1) == 0.2

    def test_create_psi_time_series_NREF_normalization(self):
        ts = create_psi_time_series(
            lat=self.lat,
            lon=self.lon,
            year=self.year,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalization="NREF",
            psi_type="Chen",
        )
        output = ts.sum()
        assert round(output, 1) == 0.6

    def test_create_psi_time_series_NREA_normalization(self):
        ts = create_psi_time_series(
            lat=self.lat,
            lon=self.lon,
            year=self.year,
            weather=self.weather,
            surface_azimuth=self.surface_azimuth,
            surface_tilt=self.surface_tilt,
            normalization="NREA",
            psi_type="Chen",
        )
        output = ts.sum()
        assert round(output, 1) == 0.9

    def test_create_create_pv_components_column_missing_in_pvsetup(self):
        pv_setup_filename = os.path.join(
            constants.DUMMY_TEST_DATA, "test_pv_setup_missing_column.csv"
        )
        pv_setup = pd.read_csv(pv_setup_filename)

        with pytest.raises(ValueError):
            create_pv_components(
                self.lat,
                self.lon,
                self.weather,
                self.population,
                pv_setup=pv_setup,
                plot=False,
                input_directory=constants.DUMMY_TEST_DATA,
                mvs_input_directory=self.test_mvs_directory,
                directory_energy_production=None,
                normalization="NREA",
                year=self.year,
            )

    def test_create_create_pv_components_wrong_technology_in_pvsetup(self):
        pv_setup_filename = os.path.join(
            constants.DUMMY_TEST_DATA, "test_pv_setup_wrong_technology.csv"
        )
        pv_setup = pd.read_csv(pv_setup_filename)

        with pytest.raises(ValueError):
            create_pv_components(
                self.lat,
                self.lon,
                self.weather,
                self.population,
                pv_setup=pv_setup,
                plot=False,
                input_directory=constants.DUMMY_TEST_DATA,
                mvs_input_directory=self.test_mvs_directory,
                directory_energy_production=None,
                normalization="NREA",
                year=self.year,
            )

    def test_create_create_pv_components_wrong_surface_type_in_pvsetup(self):
        pv_setup_filename = os.path.join(
            constants.DUMMY_TEST_DATA, "test_pv_setup_wrong_surface_type.csv"
        )
        pv_setup = pd.read_csv(pv_setup_filename)

        with pytest.raises(ValueError):
            create_pv_components(
                self.lat,
                self.lon,
                self.weather,
                self.population,
                pv_setup=pv_setup,
                plot=False,
                input_directory=constants.DUMMY_TEST_DATA,
                mvs_input_directory=self.test_mvs_directory,
                directory_energy_production=None,
                year=self.year,
            )


def test_calculate_NREA_peak_si():

    peak1 = calculate_NREA_peak(technology="si")

    assert round(peak1, 2) == 213.9


def test_calculate_NREA_peak_cpv():

    peak2 = calculate_NREA_peak(technology="cpv")

    assert round(peak2, 2) == 25.73


def test_calculate_NREA_peak_psi():

    peak3 = calculate_NREA_peak(technology="psi")

    assert round(peak3, 2) == 261.26


# # one can test that exception are raised
# def test_addition_wrong_argument_number():
#     with pytest.raises(TypeError):
#         assert addition(2) == 2  # pylint: disable=E1120
