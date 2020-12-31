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
        self.user_input_collection= os.path.join(
            os.path.dirname(__file__), "data/user_inputs_collection"
        )
        data_path = os.path.join(self.user_input_directory, "pv_setup.csv")
        self.pv_setup = pd.read_csv(data_path)

    def test_add_scenario_name_to_project_data(self):
        """ """
        scenario_name = "Test_scenario_check_inputs"
        # set scenario Name to None
        project_data = pd.read_csv(
            os.path.join(self.mvs_input_directory, "csv_elements/project_data.csv"),
            index_col=0,
        )
        project_data.at["scenario_name", "project_data"] = None

        add_scenario_name_to_project_data(mvs_input_directory=self.mvs_input_directory,
                                          scenario_name=scenario_name)
        # check project_data
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
            """ """
            # load project_data
            filename = os.path.join(self.mvs_input_directory,
                                    "csv_elements/project_data.csv")
            file = pd.read_csv(filename,
                               index_col=0,
                               header=0,
                               )
            file.at["country", "project_data"] = "Spain"
            file.at["latitude", "project_data"] = 40.0
            file.at["longitude", "project_data"] = 5.2

            file.to_csv(filename)

            list = add_location_and_year_to_project_data(
                mvs_input_directory=self.mvs_input_directory,
                static_input_directory=self.static_input_directory,
                latitude=None,
                longitude=None,
                country=None,
                year=None,
            )
            assert list == (40.0, 5.2, "Spain", 2014)

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
        filename = os.path.join(
            self.mvs_input_directory, "csv_elements/", "energyProviders.csv"
        )
        file = pd.read_csv(filename, index_col=0)

        file.at["energy_price", "DSO"]= 0.2403
        file.to_csv(filename)

        add_electricity_price(
            mvs_input_directory=self.mvs_input_directory,
            static_input_directory=self.static_input_directory,
        )
        # load csv
        file = pd.read_csv(filename, index_col=0)
        electricity_price = file.at["energy_price", "DSO"]

        assert float(electricity_price) == 0.2403

    def test_overwrite_mvs_energy_production_file_overwrite_is_false(self):

        file = pd.read_csv(
            os.path.join(self.mvs_input_directory,
                         "csv_elements/energyProduction.csv"),
            index_col=0,
            header=0,
        )
        file.at["latitude", "project_data"] = None
        file.to_csv(
            os.path.join(self.mvs_input_directory,
                         "csv_elements/energyProduction.csv")
        )

        with pytest.raises(ValueError):
            overwrite_mvs_energy_production_file(mvs_input_directory=self.mvs_input_directory,
                                                 user_input_directory=self.user_input_directory,
                                                 collections_mvs_input_directory=self.user_input_collection,
                                                 overwrite_pv_parameters=False)

    def test_overwrite_mvs_energy_production_file(self):
        """ """
        # load energyProduction.csv
        filename = os.path.join(self.mvs_input_directory,
                         "csv_elements/energyProduction.csv")
        file = pd.read_csv(filename,
            index_col=0,
            header=0,
        )
        #delete all columns
        file.drop(file.columns.difference(['index','unit']), 1, inplace=True)
        file.to_csv(filename)

        #load pv_setup.py
        pv_setup_filename = os.path.join(self.user_input_directory, "pv_setup.csv"
        )
        pv_setup = pd.read_csv(pv_setup_filename)

        pv_setup.at[1, "technology"] = "si"
        pv_setup.at[2, "technology"] = "cpv"
        pv_setup.at[3, "technology"] = "psi"
        pv_setup.to_csv(pv_setup_filename)

        # overwrite energyProduction.csv
        overwrite_mvs_energy_production_file(mvs_input_directory=self.mvs_input_directory,
                                             user_input_directory=self.user_input_directory,
                                             collections_mvs_input_directory=self.user_input_collection,
                                             overwrite_pv_parameters=True)
        # load energyProduction.csv
        file = pd.read_csv(filename,
            index_col=0,
            header=0,
        )

        assert set(["PV si","PV cpv","PV psi"]).issubset(file.columns)


    def test_add_parameters_to_energy_production_file(self):
        """ """

        filename = os.path.join(self.mvs_input_directory,
                         "csv_elements/energyProduction.csv")
        file = pd.read_csv(filename,
            index_col=0,
            header=0,
        )
        test_filename = "test_csv.csv"
        technology = "si"
        file.at["maximumCap", "PV " + technology] = None
        file.at["file_name", "PV " + technology] = None
        file.to_csv(filename)

        add_parameters_to_energy_production_file(
            technology, ts_filename=test_filename, nominal_value=1000, mvs_input_directory=self.mvs_input_directory)
        file2 = pd.read_csv(filename,
            index_col=0,
            header=0,
        )
        maxcap = int(file2.at["maximumCap", "PV " + technology])

        assert maxcap == 1000
        assert file2.at["file_name", "PV " + technology] == test_filename

    def test_add_file_name_to_energy_consumption_file(self):
        """ """
        filename= os.path.join(self.mvs_input_directory,
                         "csv_elements/energyConsumption.csv")
        file = pd.read_csv(filename,
            index_col=0,
            header=0,
        )
        file.at["file_name", "Electricity demand"] = None
        file.to_csv(filename)

        add_file_name_to_energy_consumption_file(
            column = "Electricity demand", ts_filename = "test_demand.csv",
            mvs_input_directory=self.mvs_input_directory
        )

        file2 = pd.read_csv(filename,
            index_col=0,
            header=0,
        )

        assert file2.at["file_name", "Electricity demand"] == "test_demand.csv"


    def test_add_evaluated_period_to_simulation_settings(self):
        """ """

        filename = os.path.join(self.mvs_input_directory, "csv_elements",
                         "simulation_settings.csv")
        file = pd.read_csv(filename,
                           index_col=0,
                           header=0,
                           )
        file.at["evaluated_period", "simulation_settings"] = None
        file.to_csv(filename)

        ts_file = os.path.join(self.mvs_input_directory, "time_series", "si_180_38_2014_52.52437_13.41053.csv")

        ts = pd.read_csv(ts_file,
                           index_col=0,
                           header=0,
                           )
        add_evaluated_period_to_simulation_settings(time_series=ts,
                                                    mvs_input_directory=self.mvs_input_directory)

        file = pd.read_csv(filename,
                           index_col=0,
                           header=0,
                           )

        assert int(file.at["evaluated_period", "simulation_settings"]) == len(ts.index)/24

