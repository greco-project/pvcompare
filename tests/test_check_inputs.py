import pandas as pd
import os

from pvcompare.check_inputs import (
    check_for_valid_country_year,
    add_project_data,
    check_mvs_energy_production_file)

from pvcompare import constants


class TestDemandProfiles:
    @classmethod
    def setup_class(self):
        self.country="Spain"
        self.year=2014
        self.lat = 40.0
        self.lon = 5.2
        self.input_directory = constants.DEFAULT_INPUT_DIRECTORY
        self.test_mvs_directory = os.path.join(os.path.dirname(__file__),
                                               "test_data/test_mvs_inputs")
        data_path = os.path.join(self.input_directory, "pv_setup.csv")
        self.pv_setup = pd.read_csv(data_path)

    def test_check_for_valid_country(self):
        try:
            check_for_valid_country_year(country="Uganda",
                                         year=self.year,
                                         input_directory=self.input_directory)
        except ValueError:
            # The exception was raised as expected
            pass
        else:
            # If we get here, then the ValueError was not raised
            # raise an exception so that the test fails
            raise AssertionError("ValueError was not raised")

    def test_check_for_valid_year(self):
        try:
            check_for_valid_country_year(country=self.country,
                                         year=2001,
                                         input_directory=self.input_directory)
        except ValueError:
            # The exception was raised as expected
            pass
        else:
            # If we get here, then the ValueError was not raised
            # raise an exception so that the test fails
            raise AssertionError("ValueError was not raised")

    def test_add_project_data(self):

        list = add_project_data(
            mvs_input_directory=self.test_mvs_directory,
            latitude=self.lat,
            longitude=self.lon,
            country=self.country,
            year=self.year)
        assert list == (self.lat, self.lon, self.country, self.year)

    def test_add_project_data_in_csv(self):

        add_project_data(
            mvs_input_directory=self.test_mvs_directory,
            latitude=self.lat,
            longitude=self.lon,
            country=self.country,
            year=self.year)

        project_data = pd.read_csv(os.path.join(self.test_mvs_directory,
                                                "csv_elements/project_data.csv"),
                                   index_col=0)
        latitude_csv=project_data.at["latitude", "project_data"]
        longitude_csv = project_data.at["longitude", "project_data"]
        country_csv = project_data.at["country", "project_data"]

        assert (float(latitude_csv), float(longitude_csv), country_csv) == \
               (self.lat, self.lon, self.country)

    def test_check_mvs_energy_production_file(self):

        try:
            check_mvs_energy_production_file(
                pv_setup=self.pv_setup,
                mvs_input_directory=self.test_mvs_directory,
                overwrite=False
            )
        except ValueError:
            # The exception was raised as expected
            pass
        else:
            # If we get here, then the ValueError was not raised
            # raise an exception so that the test fails
            raise AssertionError("ValueError was not raised")

