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

    def run_scenario_RefE1(self):
        """

        :return:
        """

        scenario_name = "Scenario_RefE1"
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

    def run_scenario_RefE2(self):
        """

        :return:
        """

        scenario_name = "Scenario_RefE2"
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
        self.aahp_pvcompare_values = ["air-air", 0.1852, 38]
        self.awhp_pvcompare_values = ["air-water", 0.403, 50]
        self.bwhp_pvcompare_values = ["brine-water", 0.53, 50]

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

    ###################################################################################
    ###################################  Scenario A ###################################
    ###################################################################################

    def run_scenario_A1(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-air heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_A1"

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

    def run_scenario_A2(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-air heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_A2"

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

    def run_scenario_A3(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_A3"

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

    def run_scenario_A4(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_A4"

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

    def run_scenario_A5(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_A5"

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

    def run_scenario_A6(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_A6"

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

    def run_scenario_A7(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-air heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_A7"

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

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))


    def run_scenario_A8(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-air heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_A8"

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

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_A9(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_A9"

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

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_A10(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_A10"

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

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_A11(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_A11"

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

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_A12(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Heat demand for room heating only

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_A12"

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

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    ###################################################################################
    ###################################  Scenario B ###################################
    ###################################################################################

    def run_scenario_B1(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating
        """

        scenario_name = "Scenario_B1"

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

    def run_scenario_B2(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating
        """

        scenario_name = "Scenario_B2"

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

    def run_scenario_B3(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating
        """

        scenario_name = "Scenario_B3"

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

    def run_scenario_B4(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating
        """

        scenario_name = "Scenario_B4"

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

    def run_scenario_B5(self,facades):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_B5"

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

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_B6(self,facades):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_B6"

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

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_B7(self,facades):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_B7"

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

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        bwhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.bwhp_pvcompare_values))
        for key, value in bwhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_B8(self,facades):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - Standard Si - PV
            - Brine-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_B8"

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

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("si")

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
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    ###################################################################################
    ###################################  Scenario C ###################################
    ###################################################################################

    def run_scenario_C1(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - PeroSi - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating
        """

        scenario_name = "Scenario_C1"

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

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("psi")

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

    def run_scenario_C2(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - PeroSi - PV
            - Air-to-air heat pump
            - Heat demand for room heating
        """

        scenario_name = "Scenario_C2"

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

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("psi")

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

    def run_scenario_C3(self):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - CPV - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating
        """

        scenario_name = "Scenario_C3"

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

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("cpv")

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

    def run_scenario_C4(self):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - CPV - PV
            - air-to-air heat pump
            - Heat demand for room heating
        """

        scenario_name = "Scenario_C4"

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

        pvcompare_files_modified_list[2].at["flat_roof", "technology"] = str("cpv")

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

    def run_scenario_C5(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - PeroSi - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_C5"

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

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("psi")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_C6(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - PeroSi - PV
            - Air-to-air heat pump
            - Heat demand for room heating

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_C6"

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

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("psi")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_C7(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Germany
            - Rooftop
            - CPV - PV
            - Air-to-water heat pump
            - Stratified thermal storage
            - Heat demand for room heating

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_C7"

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

        pvcompare_files_modified_list[0].at["include warm water", "value"] = False

        awhp_pvcompare = dict(zip(self.hp_pvcompare_param, self.awhp_pvcompare_values))
        for key, value in awhp_pvcompare.items():
            pvcompare_files_modified_list[1].at["heat_pump", key] = value

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("cpv")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    def run_scenario_C8(self, facades):
        """
        Scenario description:
            - Sector-coupled
            - Spain
            - Rooftop
            - CPV - PV
            - air-to-air heat pump
            - Heat demand for room heating

            - Loop over storeys: 1 - 8
        """

        scenario_name = "Scenario_C8"

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

        if facades is True:
            pv_setup_facades = pd.DataFrame(
                data={
                    "surface_type": ["south_facade", "east_facade", "west_facade"],
                    "surface_azimuth": [180, 90, 270],
                    "surface_tilt": [90, 90, 90],
                    "technology": ["", "", ""],
                }
            )
            pv_setup_facades = pv_setup_facades.set_index("surface_type")

            pvcompare_files_modified_list[2] = pvcompare_files_modified_list[2].append(
                pv_setup_facades, ignore_index=False
            )

        for i, row in pvcompare_files_modified_list[2].iterrows():
            pvcompare_files_modified_list[2].at[i, "technology"] = str("cpv")

        # Save modified data
        scenarios_sector_coupling.save_data(
            mvs_files_modified_list, pvcompare_files_modified_list
        )

        # Begin simulation
        loop_type = "storeys"
        loop_dict = {"start": 1, "stop": 8, "step": 1}

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
        if facades is True:
            self.pv_setup_original.to_csv(os.path.join(self.user_inputs_pvcompare_directory, "py_setup.csv"))

    ###################################################################################
    ###################################  Scenario D ###################################
    ###################################################################################

    def run_scenario_D1(self):
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

        scenario_name = "Scenario_D1"

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

    def run_scenario_D2(self):
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

        scenario_name = "Scenario_D2"

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

    def run_scenario_D3(self):
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

        scenario_name = "Scenario_D3"

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

    def run_scenario_D4(self):
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

        scenario_name = "Scenario_D4"

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

    def run_scenario_D5(self):
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

        scenario_name = "Scenario_D5"

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

    def run_scenario_D6(self):
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

        scenario_name = "Scenario_D6"

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

    def run_scenario_D7(self):
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

        scenario_name = "Scenario_D7"

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

    def run_scenario_D8(self):
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

        scenario_name = "Scenario_D8"

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
                if "si" not in file and "cpv" not in file:
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

    def run_scenario_RefG1(self):
        """
        Scenario description:
            - Sector-coupled
            - Gas plant
            - Germany
            - Rooftop
            - Standard Si - PV
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_RefG1"

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

    def run_scenario_RefG2(self):
        """
        Scenario description:
            - Sector-coupled
            - Gas plant
            - Spain
            - Rooftop
            - Standard Si - PV
            - Heat demand for room heating only
        """

        scenario_name = "Scenario_RefG2"

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

    def run_scenario_RefG3(self):
        """
        Scenario description:
            - Sector-coupled
            - Gas plant
            - Germany
            - Rooftop
            - Standard Si - PV
            - Heat demand for room heating and warm water
        """

        scenario_name = "Scenario_RefG3"

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

    def run_scenario_RefG4(self):
        """
        Scenario description:
            - Sector-coupled
            - Gas plant
            - Spain
            - Rooftop
            - Standard Si - PV
            - Heat demand for room heating and warm water
        """

        scenario_name = "Scenario_RefG4"

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
                if "si" not in file or "cpv" not in file:
                    os.remove(os.path.join(time_series_path, file))


if __name__ == "__main__":

    facades = True

    scenarios = Scenarios()
    scenarios.setup_class()

    # scenarios.run_scenario_RefE1()
    # scenarios.run_scenario_RefE2()

    scenarios_sector_coupling = ScenariosSectorCoupling()
    scenarios_sector_coupling.setup_class()
    #
    # scenarios_sector_coupling.run_scenario_A1()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A2()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A3()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A4()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A5()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A6()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A7(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A8(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A9(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A10(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A11(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_A12(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_B1()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_B2()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_B3()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_B4()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_B5(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_B6(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_B7(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_B8(facades)
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_C1()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_C2()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_C3()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_C4()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_D1()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_D2()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_D3()
    # scenarios_sector_coupling.revert_inputs_changes()
    # scenarios_sector_coupling.run_scenario_D4()
    # scenarios_sector_coupling.revert_inputs_changes()

    scenarios_gas = ScenariosGas()
    scenarios_gas.setup_class()
    # scenarios_gas.run_scenario_RefG1()
    # scenarios_gas.revert_inputs_changes()
    # scenarios_gas.run_scenario_RefG2()
    # scenarios_gas.revert_inputs_changes()
    # scenarios_gas.run_scenario_RefG3()
    # scenarios_gas.revert_inputs_changes()
    # scenarios_gas.run_scenario_RefG4()
    # scenarios_gas.revert_inputs_changes()
