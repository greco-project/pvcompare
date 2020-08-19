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
import pytest

from pvcompare.check_inputs import (
    check_for_valid_country_year,
    add_project_data,
    check_mvs_energy_production_file,
    add_electricity_price,
)


class TestDemandProfiles:
    @classmethod
    def setup_class(self):
        self.country = "Spain"
        self.year = 2014
        self.lat = 40.0
        self.lon = 5.2
        self.test_mvs_directory = os.path.join(
            os.path.dirname(__file__), "test_data/test_mvs_inputs"
        )

        self.test_input_directory = os.path.join(
            os.path.dirname(__file__), "test_data/test_pvcompare_inputs"
        )
        data_path = os.path.join(self.test_input_directory, "pv_setup.csv")
        self.pv_setup = pd.read_csv(data_path)

    def test_check_for_valid_country(self):
        with pytest.raises(ValueError):
            check_for_valid_country_year(
                country="Uganda",
                year=self.year,
                input_directory=self.test_input_directory,
            )

    def test_check_for_valid_year(self):
        with pytest.raises(ValueError):
            check_for_valid_country_year(
                country=self.country,
                year=2001,
                input_directory=self.test_input_directory,
            )

    def test_add_project_data(self):

        list = add_project_data(
            mvs_input_directory=self.test_mvs_directory,
            latitude=self.lat,
            longitude=self.lon,
            country=self.country,
            year=self.year,
        )
        assert list == (self.lat, self.lon, self.country, self.year)

    def test_add_project_data_in_csv(self):

        add_project_data(
            mvs_input_directory=self.test_mvs_directory,
            latitude=self.lat,
            longitude=self.lon,
            country=self.country,
            year=self.year,
        )

        project_data = pd.read_csv(
            os.path.join(self.test_mvs_directory, "csv_elements/project_data.csv"),
            index_col=0,
        )
        latitude_csv = project_data.at["latitude", "project_data"]
        longitude_csv = project_data.at["longitude", "project_data"]
        country_csv = project_data.at["country", "project_data"]

        assert (float(latitude_csv), float(longitude_csv), country_csv) == (
            self.lat,
            self.lon,
            self.country,
        )

    def test_add_project_data_with_latitude_is_none(self):

        project_data = pd.read_csv(
            os.path.join(self.test_mvs_directory, "csv_elements/project_data.csv"),
            index_col=0,
            header=0,
        )
        project_data.at["latitude", "project_data"] = None
        project_data.to_csv(
            os.path.join(self.test_mvs_directory, "csv_elements/project_data.csv")
        )

        with pytest.raises(ValueError):
            add_project_data(
                mvs_input_directory=self.test_mvs_directory,
                latitude=None,
                longitude=self.lon,
                country=self.country,
                year=self.year,
            )

    def test_add_project_data_with_year_is_none(self):

        simulation_setting = pd.read_csv(
            os.path.join(
                self.test_mvs_directory, "csv_elements/simulation_settings.csv"
            ),
            index_col=0,
            header=0,
        )
        simulation_setting.at["start_date", "simulation_settings"] = "None"
        simulation_setting.to_csv(
            os.path.join(
                self.test_mvs_directory, "csv_elements/simulation_settings.csv"
            )
        )

        with pytest.raises(ValueError):
            add_project_data(
                mvs_input_directory=self.test_mvs_directory,
                latitude=self.lat,
                longitude=self.lon,
                country=self.country,
                year=None,
            )

    def test_check_mvs_energy_production_file(self):

        with pytest.raises(ValueError):
            check_mvs_energy_production_file(
                pv_setup=self.pv_setup,
                mvs_input_directory=self.test_mvs_directory,
                overwrite=False,
            )

    def test_add_electricity_price(self):
        """
        Test to check if the function overwrites the energy_price value in the energyProviders.csv with the
        user provided value, if they are found to be different.
        """
        # set energy_price in energyProviders.csv to None
        energy_providers_filename = os.path.join(
            self.test_mvs_directory, "csv_elements/" "energyProviders.csv"
        )

        energyProviders = pd.read_csv(energy_providers_filename, index_col=0)
        energyProviders.at["energy_price", "DSO"] = None
        energyProviders.to_csv(energy_providers_filename)

        # set start_date in simulation_settings.csv to 01.01.2014
        energy_providers_filename = os.path.join(
            self.test_mvs_directory, "csv_elements/" "simulation_settings.csv"
        )

        simulation_settings = pd.read_csv(energy_providers_filename, index_col=0)
        simulation_settings.at[
            "start_date", "simulation_settings"
        ] = "2014-01-01 00:00:00"
        simulation_settings.to_csv(energy_providers_filename)

        electricity_price = add_electricity_price(
            mvs_input_directory=self.test_mvs_directory
        )

        assert electricity_price == 0.2165
