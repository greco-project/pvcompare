"""
run these tests with `pytest tests/name_of_test_module.py` or `pytest tests`
or simply `pytest` pytest will look for all files starting with "test_" and run
all functions within this file starting with "test_". For basic example of
tests you can look at our workshop
https://github.com/rl-institut/workshop/tree/master/test-driven-development.
Otherwise https://docs.pytest.org/en/latest/ and
https://docs.python.org/3/library/unittest.html are also good support.

These tests check if the examples of pvcompare run through
"""
import pytest
import argparse
import mock
import os
import pvcompare.constants as constants
import shutil

EXECUTE_TESTS_ON = os.environ.get("EXECUTE_TESTS_ON", "skip")
TESTS_ON_MASTER = "master"


class TestExamples:
    @classmethod
    def setup_class(self):
        self.outputs_directory = constants.EXAMPLE_OUTPUTS_DIRECTORY
        self.elec_sector_path = os.path.join(
            constants.EXAMPLE_DIRECTORY, "run_pvcompare_example_electricity_sector.py"
        )
        self.elec_sector_scenario_name = "Scenario_example_electricity_sector"

        self.coupled_sector_path = os.path.join(
            constants.EXAMPLE_DIRECTORY, "run_pvcompare_example_sector_coupling.py"
        )
        self.coupled_sector_scenario_name = "Scenario_example_sector_coupling"

        self.coupled_sector_gas_path = os.path.join(
            constants.EXAMPLE_DIRECTORY, "run_pvcompare_example_sector_coupling_gas.py"
        )
        self.coupled_sector_gas_scenario_name = (
            "Scenario_example_sector_coupling_gas_heating"
        )

    def teardown_method(self):
        scenarios = [
            self.elec_sector_scenario_name,
            self.coupled_sector_scenario_name,
            self.coupled_sector_gas_scenario_name,
        ]
        # Delete example output directories of all tests they existing
        for scenario in scenarios:
            dir_name = os.path.join(
                self.outputs_directory, scenario + "_test_run_through",
            )
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name, ignore_errors=True)

    # this ensures that the test is only run if explicitly executed, i.e. not when the `pytest` command
    # alone is called
    @pytest.mark.skipif(
        EXECUTE_TESTS_ON not in (TESTS_ON_MASTER),
        reason="Test deactivated, set env variable "
        "EXECUTE_TESTS_ON to 'master' to run this test",
    )
    @mock.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace())
    def test_run_pvcompare_example_electricity_sector(self, margs):
        exit_code = 1
        scenario_name = self.elec_sector_scenario_name
        # Read run_pvcompare_example_electricity_sector.py
        elec_sector = open(self.elec_sector_path).read()

        # Modify the name of the scenario to ensure it will run through for the test
        # also if the user already has it in the examples output folder
        elec_sector_modified_string = elec_sector.replace(
            scenario_name, scenario_name + "_test_run_through"
        )

        # Open example file in write modus and save the version
        # with changed scenrario name
        elec_sector_modified = open(self.elec_sector_path, "w")
        elec_sector_modified.write(elec_sector_modified_string)
        elec_sector_modified.close()

        # Run example with os.system("python <filename_of_example.py>") and check if
        # result is 0. In this case the script runs through with exit code 0
        # In case the example errors out with exit code 1
        # os.system("python <filename_of_example.py>") returns 256:
        # 256 in 16 bits -> binary number: 00000001 00000000 -> 1
        if os.system("python " + self.elec_sector_path) == 0:
            exit_code = 0

        assert exit_code == 0

        # Revert changes made in the example file
        elec_sector_modified = open(self.elec_sector_path, "w")
        elec_sector_modified.write(elec_sector)
        elec_sector_modified.close()

        # Delete example output directory of this test
        TestExamples.teardown_method(self)

    # this ensures that the test is only run if explicitly executed, i.e. not when the `pytest` command
    # alone is called
    @pytest.mark.skipif(
        EXECUTE_TESTS_ON not in (TESTS_ON_MASTER),
        reason="Test deactivated, set env variable "
        "EXECUTE_TESTS_ON to 'master' to run this test",
    )
    @mock.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace())
    def test_run_pvcompare_example_sector_coupling(self, margs):
        exit_code = 1
        scenario_name = self.coupled_sector_scenario_name
        # Read run_pvcompare_example_sector_coupling.py
        coupled_sector = open(self.coupled_sector_path).read()

        # Modify the name of the scenario to ensure it will run through for the test
        # if the user already has it in the examples output folder
        coupled_sector_modified_string = coupled_sector.replace(
            scenario_name, scenario_name + "_test_run_through"
        )

        # Open example file in write modus and save the version
        # with changed scenrario name
        coupled_sector_modified = open(self.coupled_sector_path, "w")
        coupled_sector_modified.write(coupled_sector_modified_string)
        coupled_sector_modified.close()

        # Run example with os.system("python <filename_of_example.py>") and check if
        # result is 0. In this case the script runs through with exit code 0
        # In case the example errors out with exit code 1
        # os.system("python <filename_of_example.py>") returns 256:
        # 256 in 16 bits -> binary number: 00000001 00000000 -> 1
        if os.system("python " + self.coupled_sector_path) == 0:
            exit_code = 0

        assert exit_code == 0

        # Revert changes made in the example file
        coupled_sector_modified = open(self.coupled_sector_path, "w")
        coupled_sector_modified.write(coupled_sector)
        coupled_sector_modified.close()

        # Delete example output directory of this test
        TestExamples.teardown_method(self)

    # this ensures that the test is only run if explicitly executed, i.e. not when the `pytest` command
    # alone is called
    @pytest.mark.skipif(
        EXECUTE_TESTS_ON not in (TESTS_ON_MASTER),
        reason="Test deactivated, set env variable "
        "EXECUTE_TESTS_ON to 'master' to run this test",
    )
    @mock.patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace())
    def test_run_pvcompare_example_sector_coupling_gas(self, margs):
        exit_code = 1
        scenario_name = self.coupled_sector_gas_scenario_name
        # Read run_pvcompare_example_sector_coupling_gas.py
        coupled_sector_gas = open(self.coupled_sector_gas_path).read()

        # Modify the name of the scenario to ensure it will run through for the test
        # if the user already has it in the examples output folder
        coupled_sector_gas_modified_string = coupled_sector_gas.replace(
            scenario_name, scenario_name + "_test_run_through"
        )

        # Open example file in write modus and save the version
        # with changed scenrario name
        coupled_sector_gas_modified = open(self.coupled_sector_gas_path, "w")
        coupled_sector_gas_modified.write(coupled_sector_gas_modified_string)
        coupled_sector_gas_modified.close()

        # Run example with os.system("python <filename_of_example.py>") and check if
        # result is 0. In this case the script runs through with exit code 0
        # In case the example errors out with exit code 1
        # os.system("python <filename_of_example.py>") returns 256:
        # 256 in 16 bits -> binary number: 00000001 00000000 -> 1
        if os.system("python " + self.coupled_sector_gas_path) == 0:
            exit_code = 0

        assert exit_code == 0

        # Revert changes made in the example file
        coupled_sector_gas_modified = open(self.coupled_sector_gas_path, "w")
        coupled_sector_gas_modified.write(coupled_sector_gas)
        coupled_sector_gas_modified.close()

        # Delete example output directory of this test
        TestExamples.teardown_method(self)
