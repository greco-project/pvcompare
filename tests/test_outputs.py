"""
run these tests with `pytest tests/name_of_test_module.py` or `pytest tests`
or simply `pytest` pytest will look for all files starting with "test_" and run
all functions within this file starting with "test_". For basic example of
tests you can look at our workshop
https://github.com/rl-institut/workshop/tree/master/test-driven-development.
Otherwise https://docs.pytest.org/en/latest/ and
https://docs.python.org/3/library/unittest.html are also good support.
"""

import os
import pytest
import logging
from pvcompare.outputs import plot_all_flows, plot_kpi_loop, loop_mvs
from pvcompare import constants
import shutil


class TestPlotProfiles:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        self.scenario_name = "Test_Scenario"
        self.output_directory = constants.TEST_DATA_OUTPUT
        self.mvs_output_directory = os.path.join(
            self.output_directory, self.scenario_name, "mvs_outputs"
        )
        self.timeseries_directory = os.path.join(
            self.mvs_output_directory, "/timeseries/"
        )

    def test_plot_all_flows_year(self):
        """ """
        timeseries_name = "timeseries_all_busses.xlsx"
        period = "year"
        scenario_name = "Test_Scenario"

        timeseries_directory = os.path.join(
            self.output_directory, scenario_name, "mvs_outputs_loop_specific_costs_500"
        )
        filename = os.path.join(
            timeseries_directory, f"plot_{timeseries_name[:-5]}_{period}.png"
        )
        if os.path.exists(filename):
            os.remove(filename)

        plot_all_flows(
            output_directory=self.output_directory,
            timeseries_directory=timeseries_directory,
            timeseries_name=timeseries_name,
            month=None,
            calendar_week=None,
            weekday=None,
        )

        assert os.path.exists(filename)

    def test_plot_all_flows_week(self):
        """ """
        timeseries_name = "timeseries_all_busses.xlsx"
        month = None
        calendar_week = 25
        weekday = None
        period = "caldendar_week_" + str(calendar_week)
        scenario_name = "Test_Scenario"

        timeseries_directory = os.path.join(
            self.output_directory, scenario_name, "mvs_outputs_loop_specific_costs_500"
        )
        filename = os.path.join(
            timeseries_directory, f"plot_{timeseries_name[:-5]}_{period}.png"
        )
        if os.path.exists(filename):
            os.remove(filename)

        plot_all_flows(
            output_directory=self.output_directory,
            timeseries_directory=timeseries_directory,
            timeseries_name=timeseries_name,
            month=None,
            calendar_week=calendar_week,
            weekday=None,
        )

        assert os.path.exists(filename)

    def test_plot_all_flows_day(self):
        """ """
        timeseries_name = "timeseries_all_busses.xlsx"
        month = None
        calendar_week = 25
        weekday = 6
        period = "day_" + str(calendar_week) + "_" + str(weekday)
        scenario_name = "Test_Scenario"

        timeseries_directory = os.path.join(
            self.output_directory, scenario_name, "mvs_outputs_loop_specific_costs_500"
        )
        filename = os.path.join(
            timeseries_directory, f"plot_{timeseries_name[:-5]}_{period}.png"
        )
        if os.path.exists(filename):
            os.remove(filename)

        plot_all_flows(
            output_directory=self.output_directory,
            timeseries_directory=timeseries_directory,
            timeseries_name=timeseries_name,
            month=month,
            calendar_week=calendar_week,
            weekday=weekday,
        )

        assert os.path.exists(filename)

    def test_plot_kpi_loop(self):
        """ """
        variable_name = "specific_costs"
        scenario_name = "Test_Scenario"
        loop_output_directory = os.path.join(
            self.output_directory, scenario_name, "loop_outputs_" + str(variable_name)
        )

        filename = os.path.join(
            loop_output_directory, "plot_scalars_" + str(variable_name) + ".png"
        )
        if os.path.exists(filename):
            os.remove(filename)

        plot_kpi_loop(
            scenario_name=scenario_name,
            variable_name=variable_name,
            kpi=["costs total PV", "Degree of autonomy"],
            output_directory=self.output_directory,
        )

        assert os.path.exists(filename)

    # def test_loop_mvs(self):
    #     """ """
    #
    #     latitude = 52.5243700
    #     longitude = 13.4105300
    #     year = 2014  # a year between 2011-2013!!!
    #     population = 48000
    #     country = "Germany"
    #     scenario_name = "Test_loop_mvs"
    #     output_directory = constants.TEST_DATA_OUTPUT
    #     mvs_input_directory = os.path.join(constants.TEST_DATA_DIRECTORY,
    #                                        "test_inputs_loop_mvs")
    #     variable_name = "specific_costs"
    #
    #     scenario_folder = os.path.join(self.output_directory, scenario_name)
    #     loop_output_directory = os.path.join(scenario_folder,
    #                                          "test_loop_mvs_outputs_" + str(
    #                                              variable_name))
    #     if os.path.isdir(scenario_folder):
    #         shutil.rmtree(scenario_folder)
    #
    #
    #     loop_mvs(
    #         latitude=latitude,
    #         longitude=longitude,
    #         year=year,
    #         population=population,
    #         country=country,
    #         variable_name="specific_costs",
    #         variable_column="pv_plant_01",
    #         csv_file_variable="energyProduction.csv",
    #         start=500,
    #         stop=600,
    #         step=100,
    #         output_directory=output_directory,
    #         mvs_input_directory=mvs_input_directory,
    #         scenario_name=scenario_name,
    #     )
    #
    #     assert os.path.exists(loop_output_directory)
