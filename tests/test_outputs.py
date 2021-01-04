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
from pvcompare.outputs import plot_all_flows, plot_kpi_loop, loop_mvs
from pvcompare import constants


class TestPlotProfiles:
    @classmethod
    def setup_class(self):
        """Setup variables for all tests in this class"""
        self.scenario_name = "Test_Scenario"
        self.output_directory = constants.TEST_OUTPUT_DIRECTORY
        self.mvs_output_directory = os.path.join(
            self.output_directory, self.scenario_name, "mvs_outputs"
        )
        self.timeseries_directory = os.path.join(
            self.mvs_output_directory, "/timeseries/"
        )
        self.storeys = 5

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
