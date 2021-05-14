import pvcompare.analysis as outputs
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

        # general parameters
        self.storeys = 5
        self.user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )

    def run_scenario_a01(self):
        """

        :return:
        """

        scenario_name = "Scenario_A01"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        main.apply_pvcompare(
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            year=2016,
            storeys=self.storeys,
            country=self.country_germany,
        )

        main.apply_mvs(
            scenario_name=scenario_name,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
        )

    def run_scenario_a02(self):
        """

        :return:
        """

        scenario_name = "Scenario_A02"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        main.apply_pvcompare(
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            year=2015,
            storeys=self.storeys,
            country=self.country_spain,
        )

        main.apply_mvs(
            scenario_name=scenario_name,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
        )

    def run_scenario_a1(self):
        """

        :return:
        """

        scenario_name = "Scenario_A1"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            variable_name="lifetime",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=5,
            stop=25,
            step=1,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a2(self):
        """

        :return:
        """

        scenario_name = "Scenario_A2"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            variable_name="lifetime",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=5,
            stop=25,
            step=1,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a3(self):
        """

        :return:
        """

        scenario_name = "Scenario_A3"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "psi"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            variable_name="specific_costs",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=500,
            stop=1300,
            step=50,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a4(self):
        """

        :return:
        """

        scenario_name = "Scenario_A4"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "psi"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            variable_name="specific_costs",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=500,
            stop=1300,
            step=50,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a5(self):
        """

        :return:
        """

        scenario_name = "Scenario_A5"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "cpv"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            variable_name="specific_costs",
            variable_column="PV cpv",
            csv_file_variable="energyProduction.csv",
            start=500,
            stop=1200,
            step=50,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a6(self):
        """

        :return:
        """

        scenario_name = "Scenario_A6"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "cpv"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            variable_name="specific_costs",
            variable_column="PV cpv",
            csv_file_variable="energyProduction.csv",
            start=500,
            stop=1200,
            step=50,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a7(self):
        """

        :return:
        """

        scenario_name = "Scenario_A7_test"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="technology",
            loop_dict={"step1": "si"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_a8(self):
        """

        :return:
        """

        scenario_name = "Scenario_A8"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="technology",
            loop_dict={"step1": "si"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_a9(self):
        """

        :return:
        """

        scenario_name = "Scenario_A9"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            variable_name="lifetime",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=5,
            stop=25,
            step=1,
            outputs_directory=None,
            user_inputs_mvs_directory=os.path.join(
                os.path.dirname(__file__), "data/user_inputs/mvs_inputs_HP/"
            ),
            scenario_name=scenario_name,
        )

    def run_scenario_B(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)
        list = [600, 800, 900, 1000]
        for costs in list:
            scenario_name = "Scenario_B_" + str(costs)
            user_inputs_mvs_directory = (
                constants.DEFAULT_COLLECTION_MVS_INPUTS_DIRECTORY
            )
            filename = "energyProduction.csv"
            epfile = pd.read_csv(
                os.path.join(user_inputs_mvs_directory, "csv_elements", filename),
                index_col=0,
            )
            # default: 816.2
            epfile.at["specific_costs", "PV psi"] = costs
            epfile.to_csv(
                os.path.join(user_inputs_mvs_directory, "csv_elements", filename)
            )

            outputs.loop_mvs(
                latitude=self.latitude_germany,
                longitude=self.longitude_germany,
                years=[2016],
                storeys=self.storeys,
                country=self.country_germany,
                variable_name="lifetime",
                variable_column="PV psi",
                csv_file_variable="energyProduction.csv",
                start=5,
                stop=25,
                step=1,
                outputs_directory=None,
                user_inputs_mvs_directory=None,
                scenario_name=scenario_name,
            )

        # enter default value again
        epfile = pd.read_csv(
            os.path.join(user_inputs_mvs_directory, "csv_elements", filename)
        )
        # default: 816.2
        epfile.at["specific_costs", "PV psi"] = 816.2
        epfile.to_csv(os.path.join(user_inputs_mvs_directory, "csv_elements", filename))

    def run_scenario_C(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)
        list = [500, 600, 700, 800, 900, 1000, 1100]
        for costs in list:
            scenario_name = "Scenario_C_" + str(costs)
            user_inputs_mvs_directory = (
                constants.DEFAULT_COLLECTION_MVS_INPUTS_DIRECTORY
            )
            filename = "energyProduction.csv"
            epfile = pd.read_csv(
                os.path.join(user_inputs_mvs_directory, "csv_elements", filename),
                index_col=0,
            )
            # default: 816.2
            epfile.at["specific_costs", "PV psi"] = costs
            epfile.to_csv(
                os.path.join(user_inputs_mvs_directory, "csv_elements", filename)
            )

            outputs.loop_mvs(
                latitude=self.latitude_spain,
                longitude=self.longitude_spain,
                years=[2015],
                storeys=self.storeys,
                country=self.country_spain,
                variable_name="lifetime",
                variable_column="PV psi",
                csv_file_variable="energyProduction.csv",
                start=5,
                stop=25,
                step=1,
                outputs_directory=None,
                user_inputs_mvs_directory=None,
                scenario_name=scenario_name,
            )

        # enter default value again
        epfile = pd.read_csv(
            os.path.join(user_inputs_mvs_directory, "csv_elements", filename)
        )
        # default: 816.2
        epfile.at["specific_costs", "PV psi"] = 816.2
        epfile.to_csv(os.path.join(user_inputs_mvs_directory, "csv_elements", filename))

    def run_scenario_D1(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_D1"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_D2(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_D2"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_D3(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("cpv")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_D3"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_D4(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_D4"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_D5(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_D5"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_D6(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = str("cpv")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_D6"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E1(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_E1"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E2(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_E2"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E3(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("cpv")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_E3"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E4(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_E4"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E5(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_E5"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_E6(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("cpv")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_E6"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F1(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_F1"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 1, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F2(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_F2"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 1, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F3(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("cpv")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_F3"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 1, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F4(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_F4"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 1, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F5(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_F5"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 1, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_F6(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("cpv")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_F6"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 1, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )


    def run_scenario_G1(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_G1"

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 1, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_G2(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_G2_25R"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_G3(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("cpv")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_G3_25R"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_G4(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("si")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_G4_25R"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_G5(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("psi")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_G5_25R"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_G6(self):
        """

        :return:
        """
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        for i, row in pv_setup.iterrows():
            pv_setup.at[i, "technology"] = str("cpv")
        pv_setup.to_csv(data_path, index=False)

        scenario_name = "Scenario_G6_25R"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="storeys",
            loop_dict = {"start": 3, "stop": 8, "step": 1},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H1(self):
        """

        :return:
        """

        scenario_name = "Scenario_H1"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=60.192059
        longitude=24.945831
        country="Finland"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H2(self):
        """

        :return:
        """

        scenario_name = "Scenario_H2"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=56.946285
        longitude=24.105078
        country="Latvia"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H3(self):
        """

        :return:
        """

        scenario_name = "Scenario_H3"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=37.385994
        longitude=-5.998401
        country="Spain"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H4(self):
        """

        :return:
        """

        scenario_name = "Scenario_H4"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=48.864716
        longitude=2.349014
        country="France"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H5(self):
        """

        :return:
        """

        scenario_name = "Scenario_H5"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=47.497913
        longitude=19.040236
        country="Hungary"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H6(self):
        """

        :return:
        """

        scenario_name = "Scenario_H6"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=52.237049
        longitude=21.017532
        country="Poland"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H7(self):
        """

        :return:
        """

        scenario_name = "Scenario_H7"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=44.439663
        longitude=26.096306
        country="Romania"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H8(self):
        """

        :return:
        """

        scenario_name = "Scenario_H8"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=41.902782
        longitude=12.496366
        country="Italy"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H9(self):
        """

        :return:
        """

        scenario_name = "Scenario_H9"
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years = [2014, 2017]
        latitude = 37.983810
        longitude = 23.727539
        country = "Greece"

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H10(self):
        """

        :return:
        """

        scenario_name = "Scenario_H10"
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years = [2014, 2017]
        latitude = 53.483959
        longitude = -2.244644
        country = "United Kingdom"

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H11(self):
        """

        :return:
        """

        scenario_name = "Scenario_H11"
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years = [2014, 2017]
        latitude = 52.5243700
        longitude = 13.4105300
        country = "Germany"

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_H12(self):
        """

        :return:
        """

        scenario_name = "Scenario_H12"
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years = [2014, 2017]
        latitude = 40.416775
        longitude = -3.703790
        country = "Spain"

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I1(self):
        """

        :return:
        """

        scenario_name = "Scenario_I1"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=60.192059
        longitude=24.945831
        country="Finland"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I2(self):
        """

        :return:
        """

        scenario_name = "Scenario_I2"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=56.946285
        longitude=24.105078
        country="Latvia"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I3(self):
        """

        :return:
        """

        scenario_name = "Scenario_I3"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=37.385994
        longitude=-5.998401
        country="Spain"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I4(self):
        """

        :return:
        """

        scenario_name = "Scenario_I4"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=48.864716
        longitude=2.349014
        country="France"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I5(self):
        """

        :return:
        """

        scenario_name = "Scenario_I5"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=47.497913
        longitude=19.040236
        country="Hungary"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I6(self):
        """

        :return:
        """

        scenario_name = "Scenario_I6"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=52.237049
        longitude=21.017532
        country="Poland"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I7(self):
        """

        :return:
        """

        scenario_name = "Scenario_I7"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=44.439663
        longitude=26.096306
        country="Romania"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I8(self):
        """

        :return:
        """

        scenario_name = "Scenario_I8"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years=[2014, 2017]
        latitude=41.902782
        longitude=12.496366
        country="Italy"


        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I9(self):
        """

        :return:
        """

        scenario_name = "Scenario_I9"
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years = [2014, 2017]
        latitude = 37.983810
        longitude = 23.727539
        country = "Greece"

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I10(self):
        """

        :return:
        """

        scenario_name = "Scenario_I10"
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years = [2014, 2017]
        latitude = 53.483959
        longitude = -2.244644
        country = "United Kingdom"

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I11(self):
        """

        :return:
        """

        scenario_name = "Scenario_I11"
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years = [2014, 2017]
        latitude = 52.5243700
        longitude = 13.4105300
        country = "Germany"

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_I12(self):
        """

        :return:
        """

        scenario_name = "Scenario_I12"
        data_path = os.path.join(self.user_inputs_pvcompare_directory,
                                 "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        years = [2014, 2017]
        latitude = 40.416775
        longitude = -3.703790
        country = "Spain"

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=latitude,
            longitude=longitude,
            years=years,
            storeys=self.storeys,
            country=country,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "psi", "step3": "cpv"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

if __name__ == "__main__":

    scenarios = Scenarios()
    scenarios.setup_class()
    #    scenarios.run_scenario_a3()
    #    scenarios.run_scenario_a4()
    #scenarios.run_scenario_a5()
    #scenarios.run_scenario_a6()
    #scenarios.run_scenario_a7()
    #    scenarios.run_scenario_a01()
    #    scenarios.run_scenario_a02()
    #    scenarios.run_scenario_C()
    #scenarios.run_scenario_D1()
    #scenarios.run_scenario_D2()
    #scenarios.run_scenario_D3()
    #scenarios.run_scenario_D4()
    #scenarios.run_scenario_D5()
    #scenarios.run_scenario_D6()

    #scenarios.run_scenario_E1()
    #scenarios.run_scenario_E2()
    #scenarios.run_scenario_E3()
    #scenarios.run_scenario_E4()
    #scenarios.run_scenario_E5()
    #scenarios.run_scenario_E6()

#    scenarios.run_scenario_F1()
#    scenarios.run_scenario_F2()
#    scenarios.run_scenario_F3()
#    scenarios.run_scenario_F4()
#    scenarios.run_scenario_F5()
    scenarios.run_scenario_F6()

#    scenarios.run_scenario_G1()
    # scenarios.run_scenario_G2()
    # scenarios.run_scenario_G3()
    # scenarios.run_scenario_G4()
    # scenarios.run_scenario_G5()
    # scenarios.run_scenario_G6()

    # scenarios.run_scenario_H1()
    # scenarios.run_scenario_H2()
    # scenarios.run_scenario_H3()
    # scenarios.run_scenario_H4()
    # scenarios.run_scenario_H5()
    # scenarios.run_scenario_H6()
    # scenarios.run_scenario_H7()
    # scenarios.run_scenario_H8()
    # scenarios.run_scenario_H9()
    # scenarios.run_scenario_H10()
    # scenarios.run_scenario_H11()
    # scenarios.run_scenario_H12()

    # scenarios.run_scenario_I1()
    # scenarios.run_scenario_I2()
    # scenarios.run_scenario_I3()
    # scenarios.run_scenario_I4()
    # scenarios.run_scenario_I5()
    # scenarios.run_scenario_I6()
    # scenarios.run_scenario_I7()
    # scenarios.run_scenario_I8()
    # scenarios.run_scenario_I9()
    # scenarios.run_scenario_I10()
    # scenarios.run_scenario_I11()
    # scenarios.run_scenario_I12()