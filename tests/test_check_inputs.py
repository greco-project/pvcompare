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
    add_scenario_name_to_project_data,
    add_location_and_year_to_project_data,
    check_for_valid_country_year,
    add_electricity_price,
    overwrite_mvs_energy_production_file,
    add_parameters_to_energy_production_file,
    add_file_name_to_energy_consumption_file,
    add_evaluated_period_to_simulation_settings,
    add_parameter_to_mvs_file,
    load_parameter_from_mvs_file,
)


class TestDemandProfiles:
    @classmethod
    def setup_class(self):
        self.country = "Spain"
        self.year = 2014
        self.lat = 40.0
        self.lon = 5.2
        self.mvs_input_directory = os.path.join(
            os.path.dirname(__file__), "data/user_inputs/mvs_inputs"
        )
        self.user_input_directory = os.path.join(
            os.path.dirname(__file__), "data/user_inputs/pvcompare_inputs"
        )
        self.static_input_directory = os.path.join(
            os.path.dirname(__file__), "data/static_inputs/"
        )
        self.check_inputs_directory = os.path.join(
            os.path.dirname(__file__), "test_data/inputs_for_check_inputs/"
        )
        self.user_input_collection= os.path.join(
            os.path.dirname(__file__), "data/user_inputs_collection"
        )
        data_path = os.path.join(self.user_input_directory, "pv_setup.csv")
        self.pv_setup = pd.read_csv(data_path)

    def test_add_scenario_name_to_project_data(self):
        """ """
        scenario_name = "Test_scenario_check_inputs"
        add_scenario_name_to_project_data(mvs_input_directory=self.mvs_input_directory,
                                          scenario_name=scenario_name)
        project_data = pd.read_csv(
            os.path.join(self.mvs_input_directory, "csv_elements/project_data.csv"),
            index_col=0,
        )
        mvs_scenario_name = project_data.at["scenario_name", "project_data"]

        assert mvs_scenario_name == scenario_name

    def test_add_location_and_year_to_project_data(self):
            list = add_location_and_year_to_project_data(
                mvs_input_directory=self.mvs_input_directory,
                static_input_directory=self.static_input_directory,
                latitude=self.lat,
                longitude=self.lon,
                country=self.country,
                year=self.year,
            )
            assert list == (self.lat, self.lon, self.country, self.year)

    def test_add_location_and_year_to_project_data_set_location(self):
            list = add_location_and_year_to_project_data(
                mvs_input_directory=self.check_inputs_directory,
                static_input_directory=self.static_input_directory,
                latitude=None,
                longitude=None,
                country=None,
                year=None,
            )
            lat = 40.0
            lon=5.2
            country="Spain"
            year = 2014
            assert list == (lat, lon, country, year)

    def test_check_for_valid_country(self):
        with pytest.raises(ValueError):
            check_for_valid_country_year(
                country="Uganda",
                year=self.year,
                static_input_directory=self.static_input_directory,
            )

    def test_check_for_valid_year(self):
        with pytest.raises(ValueError):
            check_for_valid_country_year(
                country=self.country,
                year=2001,
                static_input_directory=self.static_input_directory,
            )

    def test_add_project_data_with_latitude_is_none(self):

        project_data = pd.read_csv(
            os.path.join(self.mvs_input_directory, "csv_elements/project_data.csv"),
            index_col=0,
            header=0,
        )
        project_data.at["latitude", "project_data"] = None
        project_data.to_csv(
            os.path.join(self.mvs_input_directory, "csv_elements/project_data.csv")
        )

        with pytest.raises(ValueError):
            add_location_and_year_to_project_data(
                mvs_input_directory=self.mvs_input_directory,
                static_input_directory=self.static_input_directory,
                latitude=None,
                longitude=self.lon,
                country=self.country,
                year=self.year,
            )

    def test_add_electricity_price(self):
        """ """
        add_electricity_price(
            mvs_input_directory=self.check_inputs_directory,
            static_input_directory=self.static_input_directory,
        )
        # load csv
        filename1 = os.path.join(
            self.mvs_input_directory, "csv_elements/", "energyProviders.csv"
        )
        energyProviders = pd.read_csv(filename1, index_col=0)
        electricity_price = energyProviders.at["energy_price", "DSO"]

        assert float(electricity_price) == 0.2403

    def test_overwrite_mvs_energy_production_file_overwrite_is_false(self):

        file = pd.read_csv(
            os.path.join(self.check_inputs_directory,
                         "csv_elements/energyProduction.csv"),
            index_col=0,
            header=0,
        )
        file.at["latitude", "project_data"] = None
        file.to_csv(
            os.path.join(self.mvs_input_directory,
                         "csv_elements/project_data.csv")
        )

        with pytest.raises(ValueError):
            overwrite_mvs_energy_production_file(mvs_input_directory=self.check_inputs_directory,
                                                 user_input_directory=self.check_inputs_directory,
                                                 collections_mvs_input_directory=self.user_input_collection,
                                                 overwrite_pv_parameters=False)

    def test_overwrite_mvs_energy_production_file(self):
        """ """
        overwrite_mvs_energy_production_file(mvs_input_directory=self.check_inputs_directory,
                                             user_input_directory=self.check_inputs_directory,
                                             collections_mvs_input_directory=self.user_input_collection,
                                             overwrite_pv_parameters=True)



