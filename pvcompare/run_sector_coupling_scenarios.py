import pvcompare.outputs as outputs
import pvcompare.constants as constants
import pvcompare.main as main
import os
import pandas as pd


class ScenariosSectorCoupling:
    @classmethod
    def setup_class(self):
        # DEFINE USER INPUTS
        # For scenarios in germany
        self.latitude_germany = 52.5243700
        self.longitude_germany = 13.4105300
        self.years_germany = [
            2011,
            2013,
            2016,
        ]  # 2011 (good), 2013 (bad), 2016 (medium)
        self.country_germany = "Germany"

        # For scenarios in spain
        self.latitude_spain = 40.416775
        self.longitude_spain = -3.703790
        self.years_spain = [2013, 2015, 2017]  # 2017 (good), 2013 (bad), 2015 (medium)
        self.country_spain = "Spain"

        # Building parameter
        self.storeys = 5
        self.index_include_ww = 9

        # Stratified TES storage
        self.storage_mvs_value = [
            "storage_02",
            "TES",
            "True",
            "Heat bus",
            "Heat bus",
            "storage_02.csv",
            "Heat",
            "storage",
        ]

        # Heat pumps
        self.hp_mvs_param = [
            "unit",
            "optimizeCap",
            "maximumCap",
            "installedCap",
            "age_installed",
            "lifetime",
            "development_costs",
            "specific_costs",
            "specific_costs_om",
            "dispatch_price",
            "efficiency",
            "inflow_direction",
            "outflow_direction",
            "energyVector",
            "type_oemof",
        ]
        self.aahp_mvs_values = [
            "kW",
            True,
            "None",
            0,
            0,
            12,
            0,
            450,
            42.5,
            0,
            "{'file_name': 'None', 'header': 'no_unit', 'unit': ''}",
            "Electricity bus",
            "Heat bus",
            "Heat",
            "transformer",
        ]
        self.aw_mvs_values = [
            "kW",
            True,
            "None",
            0,
            0,
            18,
            0,
            1000,
            29.1,
            0,
            "{'file_name': 'None', 'header': 'no_unit', 'unit': ''}",
            "Electricity bus",
            "Heat bus",
            "Heat",
            "transformer",
        ]
        self.bw_mvs_values = [
            "kW",
            True,
            "None",
            0,
            0,
            20,
            0,
            1600,
            29.1,
            0,
            "{'file_name': 'None', 'header': 'no_unit', 'unit': ''}",
            "Electricity bus",
            "Heat bus",
            "Heat",
            "transformer",
        ]

        self.hp_pvcompare_param = ["technology", "quality_grade", "temp_high"]
        self.aahp_pvcompare_values = ["air-air", 0.1852, 26]
        self.aw_pvcompare_values = ["air-water", 0.403, 60]
        self.bw_pvcompare_values = ["brine-water", 0.53, 65]

        # Set paths
        self.user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
        self.user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
        self.mvs_inputs_path_sector_coupling = os.path.abspath(
            os.path.join(
                self.user_inputs_mvs_directory, os.pardir, "mvs_inputs_sector_coupling"
            )
        )

        def read_data(filename, directory):
            if directory == "mvs":
                return pd.read_csv(
                    os.path.join(
                        self.mvs_inputs_path_sector_coupling, "csv_elements", filename
                    ),
                    header=0,
                    index_col=0,
                )
            elif directory == "pvcompare":
                return pd.read_csv(
                    os.path.join(self.user_inputs_pvcompare_directory, filename),
                    header=0,
                    index_col=0,
                )

        # Read mvs input data which varies depending on the scenario
        self.energy_busses_original = read_data("energyBusses.csv", "mvs")
        self.energy_conversion_original = read_data("energyConversion.csv", "mvs")
        self.energy_production_original = read_data("energyProduction.csv", "mvs")
        self.energy_providers_original = read_data("energyProviders.csv", "mvs")
        self.energy_storage_original = read_data("energyStorage.csv", "mvs")
        self.storage_xx_original = read_data("storage_02.csv", "mvs")

        # Read pvcompare input data which varies depending on the scenario
        self.building_parameters_original = read_data(
            "building_parameters.csv", "pvcompare"
        )
        self.heat_pumps_and_chillers_original = read_data(
            "heat_pumps_and_chillers.csv", "pvcompare"
        )
        self.pv_setup_original = read_data("pv_setup.csv", "pvcompare")
        self.stratified_thermal_storage_original = read_data(
            "stratified_thermal_storage.csv", "pvcompare"
        )

        self.mvs_filenames = [
            "energyBusses.csv",
            "energyConversion.csv",
            "energyProduction.csv",
            "energyProviders.csv",
            "energyStorage.csv",
            "storage_02.csv",
        ]

        self.mvs_files_original = [
            self.energy_busses_original,
            self.energy_conversion_original,
            self.energy_production_original,
            self.energy_providers_original,
            self.energy_storage_original,
            self.storage_xx_original,
        ]

        self.pvcompare_filenames = [
            "building_parameters.csv",
            "heat_pumps_and_chillers.csv",
            "pv_setup.csv",
            "stratified_thermal_storage.csv",
        ]

        self.pvcompare_files_original = [
            self.building_parameters_original,
            self.heat_pumps_and_chillers_original,
            self.pv_setup_original,
            self.stratified_thermal_storage_original,
        ]

    def get_data(self):
        """
        This function loads data, which will be modified
        depending on the scenario

        Returns
        -------
        mvs_files_modified_list : List of mvs input files
        pvcompare_files_modified_list : List of pvcompare input files
        """
        # Load data to be modified
        energy_busses = self.energy_busses_original.copy()
        energy_conversion = self.energy_conversion_original.copy()
        energy_production = self.energy_production_original.copy()
        energy_providers = self.energy_providers_original.copy()
        energy_storage = self.energy_storage_original.copy()
        storage_xx = self.storage_xx_original.copy()

        building_parameters = self.building_parameters_original.copy()
        heat_pumps_and_chillers = self.heat_pumps_and_chillers_original.copy()
        pv_setup = self.pv_setup_original.copy()
        stratified_thermal_storage = self.stratified_thermal_storage_original.copy()

        # Gather data to modify in list
        mvs_files_modified_list = [
            energy_busses,
            energy_conversion,
            energy_production,
            energy_providers,
            energy_storage,
            storage_xx,
        ]
        pvcompare_files_modified_list = [
            building_parameters,
            heat_pumps_and_chillers,
            pv_setup,
            stratified_thermal_storage,
        ]
        return mvs_files_modified_list, pvcompare_files_modified_list

    def save_data(self, mvs_files_modified_list, pvcompare_files_modified_list):
        """
        This function saves modified data

        Parameters
        ----------
        mvs_files_modified_list : List of mvs input files
        pvcompare_files_modified_list : List of pvcompare input files
        """
        mvs_files_modified = dict(zip(self.mvs_filenames, mvs_files_modified_list))
        for name, file in mvs_files_modified.items():
            file.to_csv(
                os.path.join(
                    self.mvs_inputs_path_sector_coupling, "csv_elements", name
                ),
                na_rep="NaN",
            )

        pvcompare_files_modified = dict(
            zip(self.pvcompare_filenames, pvcompare_files_modified_list)
        )
        for name, file in pvcompare_files_modified.items():
            file.to_csv(
                os.path.join(self.user_inputs_pvcompare_directory, name), na_rep="NaN"
            )

    def run_scenario_E1(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-air heat pump
            - Heat demand for room heating only

        :return:
        """

        scenario_name = "Scenario_E1"

        # Get data
        mvs_files_modified_list, pvcompare_files_modified_list = scenarios_sector_coupling.get_data()

        # Modify data
        aahp_mvs_values = dict(zip(self.hp_mvs_param, self.aahp_mvs_values))
        for key, value in aahp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        aahp_pvcompare = dict(zip(self.hp_pvcompare_param, self.aahp_pvcompare_values))
        for key, value in aahp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(mvs_files_modified_list, pvcompare_files_modified_list)

        main.apply_pvcompare(
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            year=2017,
            storeys=self.storeys,
            country=self.country_germany,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            overwrite_grid_parameters=True,
            overwrite_pv_parameters=True,
        )

        main.apply_mvs(
            scenario_name=scenario_name,
            outputs_directory=None,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
        )

    def revert_inputs_changes(self):
        mvs_files = dict(zip(self.mvs_filenames, self.mvs_files_original))
        pvcompare_files = dict(
            zip(self.pvcompare_filenames, self.pvcompare_files_original)
        )

        for name, file in mvs_files.items():
            file.to_csv(
                os.path.join(
                    self.mvs_inputs_path_sector_coupling, "csv_elements", name
                ),
            )

        for name, file in pvcompare_files.items():
            file.to_csv(
                os.path.join(self.user_inputs_pvcompare_directory, name),
            )

        time_series_path = os.path.join(self.mvs_inputs_path_sector_coupling, "time_series")
        time_series_files = os.listdir(time_series_path)

        for file in time_series_files:
            if os.path.exists(os.path.join(time_series_path, file)):
                os.remove(os.path.join(time_series_path, file))


if __name__ == "__main__":

    scenarios_sector_coupling = ScenariosSectorCoupling()
    scenarios_sector_coupling.setup_class()
    scenarios_sector_coupling.run_scenario_E1()
    scenarios_sector_coupling.revert_inputs_changes()
