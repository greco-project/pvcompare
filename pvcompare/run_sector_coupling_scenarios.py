import pvcompare.analysis as analysis
import pvcompare.constants as constants
import pvcompare.main as main
import os
import pandas as pd


class Scenarios:
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

        # Set paths
        self.user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
        self.user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY

    def run_scenario_a1(self):
        """

        :return:
        """

        scenario_name = "Scenario_A1"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_a2(self):
        """

        :return:
        """

        scenario_name = "Scenario_A2"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.user_inputs_mvs_directory,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )


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
        self.awhp_mvs_values = [
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
        self.bwhp_mvs_values = [
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
        self.awhp_pvcompare_values = ["air-water", 0.403, 60]
        self.bwhp_pvcompare_values = ["brine-water", 0.53, 65]

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
        """

        scenario_name = "Scenario_E1"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

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
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        # Make an output directory for results of scenario
        # os.mkdir(os.path.join(constants.DEFAULT_OUTPUTS_DIRECTORY, scenario_name))
        #
        # for year in self.years_germany:
        #
        #     output_dir = os.path.join(constants.DEFAULT_OUTPUTS_DIRECTORY, scenario_name,
        #                               "mvs_outputs_loop_" + str(year))
        #
        #     main.apply_pvcompare(
        #         latitude=self.latitude_germany,
        #         longitude=self.longitude_germany,
        #         year=year,
        #         storeys=self.storeys,
        #         country=self.country_germany,
        #         user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
        #         overwrite_grid_parameters=True,
        #         overwrite_pv_parameters=True,
        #     )
        #
        #     main.apply_mvs(
        #         scenario_name=scenario_name,
        #         mvs_output_directory=output_dir,
        #         user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
        #     )

        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E2(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-air heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_E2"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

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
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        # Make an output directory for results of scenario
        # os.mkdir(os.path.join(constants.DEFAULT_OUTPUTS_DIRECTORY, scenario_name))
        #
        # for year in self.years_spain:
        #     output_dir = os.path.join(constants.DEFAULT_OUTPUTS_DIRECTORY, scenario_name,
        #                               "mvs_outputs_loop_" + str(year))
        #
        #     main.apply_pvcompare(
        #         latitude=self.latitude_spain,
        #         longitude=self.longitude_spain,
        #         year=year,
        #         storeys=self.storeys,
        #         country=self.country_spain,
        #         user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
        #         overwrite_grid_parameters=True,
        #         overwrite_pv_parameters=True,
        #     )
        #
        #     main.apply_mvs(
        #         scenario_name=scenario_name,
        #         mvs_output_directory=output_dir,
        #         user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
        #     )

        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E3(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_E3"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        awhp_mvs_values = dict(zip(self.hp_mvs_param, self.awhp_mvs_values))
        for key, value in awhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E4(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_E4"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        awhp_mvs_values = dict(zip(self.hp_mvs_param, self.awhp_mvs_values))
        for key, value in awhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E5(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_E5"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        bwhp_mvs_values = dict(zip(self.hp_mvs_param, self.bwhp_mvs_values))
        for key, value in bwhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        bwhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.bwhp_pvcompare_values))
        for key, value in bwhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E6(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_E6"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        bwhp_mvs_values = dict(zip(self.hp_mvs_param, self.bwhp_mvs_values))
        for key, value in bwhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        bwhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.bwhp_pvcompare_values))
        for key, value in bwhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E7(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-air heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_E7"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

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
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E8(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-air heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_E8"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

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
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E9(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_E9"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        awhp_mvs_values = dict(zip(self.hp_mvs_param, self.awhp_mvs_values))
        for key, value in awhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E10(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_E10"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        awhp_mvs_values = dict(zip(self.hp_mvs_param, self.awhp_mvs_values))
        for key, value in awhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E11(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_E11"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        bwhp_mvs_values = dict(zip(self.hp_mvs_param, self.bwhp_mvs_values))
        for key, value in bwhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        bwhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.bwhp_pvcompare_values))
        for key, value in bwhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E12(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_E12"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        bwhp_mvs_values = dict(zip(self.hp_mvs_param, self.bwhp_mvs_values))
        for key, value in bwhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        bwhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.bwhp_pvcompare_values))
        for key, value in bwhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F1(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating and warm water
        """

        scenario_name = "Scenario_F1"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        awhp_mvs_values = dict(zip(self.hp_mvs_param, self.awhp_mvs_values))
        for key, value in awhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        energyStorage = mvs_files_modified_list[4]
        strat_tes_data = pd.DataFrame(
            data={"": energyStorage.index, "storage_02": self.storage_mvs_value}
        )
        strat_tes_data = strat_tes_data.set_index("")
        energyStorage = energyStorage.join(strat_tes_data)
        mvs_files_modified_list[4] = energyStorage

        pvcompare_files_modified_list[0].at["include warm water", "value"] = True

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F2(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating and warm water
        """

        scenario_name = "Scenario_F2"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        awhp_mvs_values = dict(zip(self.hp_mvs_param, self.awhp_mvs_values))
        for key, value in awhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        energyStorage = mvs_files_modified_list[4]
        strat_tes_data = pd.DataFrame(
            data={"": energyStorage.index, "storage_02": self.storage_mvs_value}
        )
        strat_tes_data = strat_tes_data.set_index("")
        energyStorage = energyStorage.join(strat_tes_data)
        mvs_files_modified_list[4] = energyStorage

        pvcompare_files_modified_list[0].at["include warm water", "value"] = True

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F3(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating and warm water
        """

        scenario_name = "Scenario_F3"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        bwhp_mvs_values = dict(zip(self.hp_mvs_param, self.bwhp_mvs_values))
        for key, value in bwhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        energyStorage = mvs_files_modified_list[4]
        strat_tes_data = pd.DataFrame(
            data={"": energyStorage.index, "storage_02": self.storage_mvs_value}
        )
        strat_tes_data = strat_tes_data.set_index("")
        energyStorage = energyStorage.join(strat_tes_data)
        mvs_files_modified_list[4] = energyStorage

        pvcompare_files_modified_list[0].at["include warm water", "value"] = True

        bwhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.bwhp_pvcompare_values))
        for key, value in bwhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F4(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating and warm water
        """

        scenario_name = "Scenario_F4"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        bwhp_mvs_values = dict(zip(self.hp_mvs_param, self.bwhp_mvs_values))
        for key, value in bwhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        energyStorage = mvs_files_modified_list[4]
        strat_tes_data = pd.DataFrame(
            data={"": energyStorage.index, "storage_02": self.storage_mvs_value}
        )
        strat_tes_data = strat_tes_data.set_index("")
        energyStorage = energyStorage.join(strat_tes_data)
        mvs_files_modified_list[4] = energyStorage

        pvcompare_files_modified_list[0].at["include warm water", "value"] = True

        bwhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.bwhp_pvcompare_values))
        for key, value in bwhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F5(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating and warm water

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_F5"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        awhp_mvs_values = dict(zip(self.hp_mvs_param, self.awhp_mvs_values))
        for key, value in awhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        energyStorage = mvs_files_modified_list[4]
        strat_tes_data = pd.DataFrame(
            data={"": energyStorage.index, "storage_02": self.storage_mvs_value}
        )
        strat_tes_data = strat_tes_data.set_index("")
        energyStorage = energyStorage.join(strat_tes_data)
        mvs_files_modified_list[4] = energyStorage

        pvcompare_files_modified_list[0].at["include warm water", "value"] = True

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F6(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating and warm water

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_F6"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        awhp_mvs_values = dict(zip(self.hp_mvs_param, self.awhp_mvs_values))
        for key, value in awhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        energyStorage = mvs_files_modified_list[4]
        strat_tes_data = pd.DataFrame(
            data={"": energyStorage.index, "storage_02": self.storage_mvs_value}
        )
        strat_tes_data = strat_tes_data.set_index("")
        energyStorage = energyStorage.join(strat_tes_data)
        mvs_files_modified_list[4] = energyStorage

        pvcompare_files_modified_list[0].at["include warm water", "value"] = True

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F7(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating and warm water

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_F7"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        bwhp_mvs_values = dict(zip(self.hp_mvs_param, self.bwhp_mvs_values))
        for key, value in bwhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        energyStorage = mvs_files_modified_list[4]
        strat_tes_data = pd.DataFrame(
            data={"": energyStorage.index, "storage_02": self.storage_mvs_value}
        )
        strat_tes_data = strat_tes_data.set_index("")
        energyStorage = energyStorage.join(strat_tes_data)
        mvs_files_modified_list[4] = energyStorage

        pvcompare_files_modified_list[0].at["include warm water", "value"] = True

        bwhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.bwhp_pvcompare_values))
        for key, value in bwhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F8(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating and warm water

            - Loop over storeys: 1 - 5
        """

        scenario_name = "Scenario_F8"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_sector_coupling.get_data()

        # Modify data
        bwhp_mvs_values = dict(zip(self.hp_mvs_param, self.bwhp_mvs_values))
        for key, value in bwhp_mvs_values.items():
            mvs_files_modified_list[1].at[key, "Heat pump"] = value

        energyStorage = mvs_files_modified_list[4]
        strat_tes_data = pd.DataFrame(
            data={"": energyStorage.index, "storage_02": self.storage_mvs_value}
        )
        strat_tes_data = strat_tes_data.set_index("")
        energyStorage = energyStorage.join(strat_tes_data)
        mvs_files_modified_list[4] = energyStorage

        pvcompare_files_modified_list[0].at["include warm water", "value"] = True

        bwhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.bwhp_pvcompare_values))
        for key, value in bwhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_sector_coupling,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
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
            file.to_csv(os.path.join(self.user_inputs_pvcompare_directory, name),)

        time_series_path = os.path.join(
            self.mvs_inputs_path_sector_coupling, "time_series"
        )
        time_series_files = os.listdir(time_series_path)

        for file in time_series_files:
            if os.path.exists(os.path.join(time_series_path, file)):
                os.remove(os.path.join(time_series_path, file))


class ScenariosGas:
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

        # Set paths
        self.user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
        self.user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
        self.mvs_inputs_path_gas = os.path.abspath(
            os.path.join(
                self.user_inputs_mvs_directory,
                os.pardir,
                "mvs_inputs_sector_coupling_gas",
            )
        )

        def read_data(filename, directory):
            if directory == "mvs":
                return pd.read_csv(
                    os.path.join(self.mvs_inputs_path_gas, "csv_elements", filename),
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
        self.energy_providers_original = read_data("energyProviders.csv", "mvs")

        # Read pvcompare input data which varies depending on the scenario
        self.building_parameters_original = read_data(
            "building_parameters.csv", "pvcompare"
        )
        self.pv_setup_original = read_data("pv_setup.csv", "pvcompare")

        self.mvs_filenames = [
            "energyProviders.csv",
        ]

        self.mvs_files_original = [
            self.energy_providers_original,
        ]

        self.pvcompare_filenames = [
            "building_parameters.csv",
            "pv_setup.csv",
        ]

        self.pvcompare_files_original = [
            self.building_parameters_original,
            self.pv_setup_original,
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
        energy_providers = self.energy_providers_original.copy()

        building_parameters = self.building_parameters_original.copy()
        pv_setup = self.pv_setup_original.copy()

        # Gather data to modify in list
        mvs_files_modified_list = [
            energy_providers,
        ]
        pvcompare_files_modified_list = [
            building_parameters,
            pv_setup,
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
                os.path.join(self.mvs_inputs_path_gas, "csv_elements", name),
                na_rep="NaN",
            )

        pvcompare_files_modified = dict(
            zip(self.pvcompare_filenames, pvcompare_files_modified_list)
        )
        for name, file in pvcompare_files_modified.items():
            file.to_csv(
                os.path.join(self.user_inputs_pvcompare_directory, name), na_rep="NaN"
            )

    def run_scenario_G1(self):
        """
        Scenario description:
            - Sector-coupled
            - Gas plant
            - Germany
            - Rooftop
            - Standard Si - PV
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_G1"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_gas.get_data()

        # Modify data
        pvcompare_files_modified_list[0].at["include warm water", "value"] = False
        pvcompare_files_modified_list[1].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_gas.save_data(mvs_files_modified_list, pvcompare_files_modified_list)

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_gas,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_G2(self):
        """
        Scenario description:
            - Sector-coupled
            - Gas plant
            - Spain
            - Rooftop
            - Standard Si - PV
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_G2"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_gas.get_data()

        # Modify data
        pvcompare_files_modified_list[0].at["include warm water", "value"] = False
        pvcompare_files_modified_list[1].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_gas.save_data(mvs_files_modified_list, pvcompare_files_modified_list)

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_gas,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_G3(self):
        """
        Scenario description:
            - Sector-coupled
            - Gas plant
            - Germany
            - Rooftop
            - Standard Si - PV
            - Heat demand for room heating and warm water
        """

        scenario_name = "Scenario_G3"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_gas.get_data()

        # Modify data
        pvcompare_files_modified_list[0].at["include warm water", "value"] = True
        pvcompare_files_modified_list[1].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_gas.save_data(mvs_files_modified_list, pvcompare_files_modified_list)

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_gas,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_G4(self):
        """
        Scenario description:
            - Sector-coupled
            - Gas plant
            - Spain
            - Rooftop
            - Standard Si - PV
            - Heat demand for room heating and warm water
        """

        scenario_name = "Scenario_G4"

        # Get data
        (
            mvs_files_modified_list,
            pvcompare_files_modified_list,
        ) = scenarios_gas.get_data()

        # Modify data
        pvcompare_files_modified_list[0].at["include warm water", "value"] = True
        pvcompare_files_modified_list[1].at["flat_roof", "technology"] = str("si")

        # Save modified data
        scenarios_gas.save_data(mvs_files_modified_list, pvcompare_files_modified_list)

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 5, "stop": 5, "step": 1}

        analysis.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type=loop_type,
            loop_dict=loop_dict,
            user_inputs_mvs_directory=self.mvs_inputs_path_gas,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def revert_inputs_changes(self):
        mvs_files = dict(zip(self.mvs_filenames, self.mvs_files_original))
        pvcompare_files = dict(
            zip(self.pvcompare_filenames, self.pvcompare_files_original)
        )

        for name, file in mvs_files.items():
            file.to_csv(os.path.join(self.mvs_inputs_path_gas, "csv_elements", name),)

        for name, file in pvcompare_files.items():
            file.to_csv(os.path.join(self.user_inputs_pvcompare_directory, name),)

        time_series_path = os.path.join(self.mvs_inputs_path_gas, "time_series")
        time_series_files = os.listdir(time_series_path)

        for file in time_series_files:
            if os.path.exists(os.path.join(time_series_path, file)):
                os.remove(os.path.join(time_series_path, file))


if __name__ == "__main__":

    scenarios = Scenarios()
    scenarios.setup_class()

    # scenarios.run_scenario_a1()
    # scenarios.run_scenario_a2()

    scenarios_sector_coupling = ScenariosSectorCoupling()
    scenarios_sector_coupling.setup_class()
    #
    # scenarios_sector_coupling.run_scenario_E1()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_E2()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_E3()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_E4()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_E5()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_E6()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_F1()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_F2()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_F3()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_F4()
    # scenarios_sector_coupling.revert_inputs_changes()

    scenarios_gas = ScenariosGas()
    scenarios_gas.setup_class()
    # scenarios_gas.run_scenario_G1()
    # scenarios_gas.revert_inputs_changes()
    # scenarios_gas.run_scenario_G2()
    # scenarios_gas.revert_inputs_changes()
    scenarios_gas.run_scenario_G3()
    scenarios_gas.revert_inputs_changes()
    scenarios_gas.run_scenario_G4()
    scenarios_gas.revert_inputs_changes()
