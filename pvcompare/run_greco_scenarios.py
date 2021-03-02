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

        scenario_name = "Scenario_A5_1"
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
            stop=700,
            step=50,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a6(self):
        """

        :return:
        """

        scenario_name = "Scenario_A6_1"
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
            stop=700,
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

        scenario_name = "Scenario_D1"
        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="technology",
            loop_dict={"step1": "si", "step2": "cpv", "step3": "psi"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )


if __name__ == "__main__":

    scenarios = Scenarios()
    scenarios.setup_class()
    #    scenarios.run_scenario_a3()
    #    scenarios.run_scenario_a4()
    #    scenarios.run_scenario_a5()
    #    scenarios.run_scenario_a6()
    scenarios.run_scenario_a7()
    #    scenarios.run_scenario_a01()
    #    scenarios.run_scenario_a02()
    #    scenarios.run_scenario_C()
    scenarios.run_scenario_D1()
