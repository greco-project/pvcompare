import pytest
import pandas as pd
import numpy as np
import os
from pandas.util.testing import assert_series_equal

from pvcompare import heat_pump_and_chiller as hc
from pvcompare.constants import TEST_DATA_HEAT


class TestCalulateCopsAndEers:
    @classmethod
    def setup_class(self):
        self.date_range = pd.date_range("2018", periods=5, freq="H")
        self.weather = pd.DataFrame([11.85, 6.85, 0.0, -3.0, 27.0], columns=["temp_air"],
                                    index=self.date_range)
        self.lat = 53.2
        self.lon = 13.2

    def test_calculate_cops_and_eers_heat_pump_without_icing(self):
        cops = hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            input_directory=TEST_DATA_HEAT,
            mvs_input_directory=TEST_DATA_HEAT)
        cops_exp = pd.Series([4.0, 3.0, 2.234636871508378, 2.01005025125628, np.nan], index=self.date_range, name='no_unit')
        assert_series_equal(cops, cops_exp)

    def test_calculate_cops_and_eers_heat_pump_consider_icing(self):
        pass

    def test_calculate_cops_and_eers_chiller(self):
        pass

    def test_calculate_cops_and_eers_misspelled_mode(self):
        with pytest.raises(ValueError):
            cops = hc.calculate_cops_and_eers(
                weather=self.weather,
                lat=self.lat,
                lon=self.lon,
                temperature_col="temp_air",
                mode="misspelled_mode",
                input_directory=TEST_DATA_HEAT,
                mvs_input_directory=TEST_DATA_HEAT)

    def test_calculate_cops_and_eers_saved_file(self):
        hc.calculate_cops_and_eers(
            weather=self.weather,
            lat=self.lat,
            lon=self.lon,
            temperature_col="temp_air",
            mode="heat_pump",
            input_directory=TEST_DATA_HEAT,
            mvs_input_directory=TEST_DATA_HEAT)
        assert os.path.exists(os.path.join(TEST_DATA_HEAT, "time_series", "cops_heat_pump_2018_53.2_13.2.csv"))

    def teardown_class(self):
        filename = os.path.join(TEST_DATA_HEAT, "time_series", "cops_heat_pump_2018_53.2_13.2.csv")
        if os.path.exists(filename):
            os.remove(filename)


class TestAddSectorCoupling:
    @classmethod
    def setup_class(self):
        self.weather = pd.DataFrame([10.0, 5.0, 0.0, -3.0, 27.0], columns=["temp_air"],
                                    index=pd.date_range("2018", periods=5, freq="H"))

    pass
