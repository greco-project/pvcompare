from pvcompare import check_inputs
import pvcompare.main as main
import pvcompare.constants as constants
import os
import pandas as pd
import shutil
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import logging
import numpy as np
import seaborn as sns

sns.set()


def plot_all_flows(
    scenario_name=None,
    outputs_directory=None,
    timeseries_directory=None,
    timeseries_name="timeseries_all_busses.xlsx",
    month=None,
    calendar_week=None,
    weekday=None,
):
    """
    Plots all flows of the energy system for a given period of time.

    Parameters
    ----------
    scenario_name: str
        Name of the Scenario. The name should follow the scheme:
        "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    outputs_directory: str or None
        Path to the directory in which the plot should be saved.
        Default: None.
        If None: `outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY`
    timeseries_directory: str or None
        Path to the timeseries directory.
        If None: `timeseries_directory = outputs_directory`.
        Default: None.
    timeseries_name: str or None
        Default: timeseries_all_busses.xlsx
    month: int
        Number of month that should be plotted.
        Only fill in a number here, if you want to plot over one month.
        If None: will plot over week, weekday or the whole year. Default: None
    calendar_week: int
        the week (number in calender weeks) that should be plotted.
        Only fill in a number here, if you want to plot over one a week or a weekday.
        if None: will plot over one month or the whole year. Default: None
    weekday: int
        The day of the caldendar_week (from 0-6 with 0 : Monday and 6: Sunday.
        If None: the next greater period is plotted. Default: None

    Returns
    -------
        None
        Saves figure into outputs_directory
    -------
    """
    # check if weekday is a valid day
    if weekday not in range(0, 6, 1):
        logging.error(
            "The weekday is not valid. Please choose a number "
            "between 0-6 with 0:Monaday and 6:Sunday."
        )

    # read timeseries
    # check if scenario is specified or the timeseries directory is given
    if timeseries_directory is None:
        if outputs_directory == None:
            outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
        scenario_folder = os.path.join(outputs_directory, scenario_name)
        if timeseries_directory == None:
            timeseries_directory = os.path.join(scenario_folder, "mvs_outputs")
        if not os.path.isdir(timeseries_directory):
            logging.warning(
                "The timeseries directory does not exist. Please check "
                "the scenario name or specify the timeseries directory."
            )
    df = pd.read_excel(
        os.path.join(timeseries_directory, timeseries_name),
        sheet_name="Electricity bus",
        index_col=0,
    )
    try:
        df_heat = pd.read_excel(
            os.path.join(timeseries_directory, timeseries_name),
            sheet_name="Heat bus",
            index_col=0,
        )
    except:
        df_heat = pd.DataFrame(
            data={"Heat pump": [0], "TES input power": [0], "TES output power": [0]}
        )

    df_pv = pd.read_excel(
        os.path.join(timeseries_directory, timeseries_name),
        sheet_name="PV bus",
        index_col=0,
    )
    # Converting the index as date
    df.index = pd.to_datetime(df.index)
    df_heat.index = pd.to_datetime(df_heat.index)
    df_pv.index = pd.to_datetime(df_pv.index)

    # define period for the plot
    if month is None:
        if calendar_week is None:
            period = "year"
            pass
            if weekday is not None:
                logging.error(
                    "If you want to create a plot over one weekday, please "
                    "define a caldendar_week as well. Otherwise set"
                    " weekday to 'None'."
                )
        else:
            if weekday is not None:
                df = df[df.index.week == calendar_week]
                df_heat = df_heat[df_heat.index.week == calendar_week]
                df_pv = df_pv[df_heat.index.week == calendar_week]
                df = df[df.index.weekday == weekday]
                df_heat = df_heat[df_heat.index.weekday == weekday]
                df_pv = df_pv[df_pv.index.weekday == weekday]
                period = "day_" + str(calendar_week) + "_" + str(weekday)
            else:
                df = df[df.index.week == calendar_week]
                df_heat = df_heat[df_heat.index.week == calendar_week]
                df_pv = df_pv[df_pv.index.week == calendar_week]
                period = "caldendar_week_" + str(calendar_week)
    else:
        if calendar_week is not None:
            if weekday is None:
                logging.warning(
                    "You inserted a month and a week. In this case the "
                    "plot will cover one caldendar_week. If you want to plot "
                    "over one month please set the calendar_week to 'None'"
                )
                df = df[df.index.week == calendar_week]
                df_heat = df_heat[df_heat.index.week == calendar_week]
                df_pv = df_pv[df_heat.index.week == calendar_week]
                period = "week_" + str(calendar_week)
            else:
                logging.warning(
                    "You inserted a month, a caldendar_week and a weekday. In this case the "
                    "plot will cover one weekday only. If you want to plot "
                    "over one month please set the caldendar_week and weekday to 'None'"
                )
                df = df[df.index.week == calendar_week]
                df_heat = df_heat[df_heat.index.week == calendar_week]
                df_pv = df_pv[df_pv.index.week == calendar_week]
                df = df[df.index.weekday == weekday]
                df_heat = df_heat[df_heat.index.weekday == weekday]
                df_pv = df_pv[df_pv.index.weekday == weekday]
                period = "day_" + str(calendar_week) + "_" + str(weekday)
        else:
            df = df[df.index.month == month]
            df_heat = df_heat[df_heat.index.month == month]
            df_pv = df_pv[df_pv.index.month == month]
            period = "month_" + str(month)

    # plot
    df_plot = df.copy().drop(
        [
            # "Charge Contoller ESS Li-Ion (discharge)",
            # "storage_charge_controller_in",
            # "storage_charge_controller_out",
            # "Heat pump",
            #'Solar inverter',
            # "Electricity grid_consumption_period",
            # "Charge Contoller ESS Li-Ion (charge)",
            # "Electricity bus_excess_sink",
            #'Electricity demand',
            #'Electricity grid_feedin_sink_sink'
        ],
        axis=1,
    )

    # df_pv_plot = df_pv.copy().drop(
    #     [
    #         "PV si",
    #         "Solar inverter"
    #     ],
    #     axis=1
    # )
    # df_plot = pd.concat([df_plot, df_pv_plot], axis=1)

    try:
        df_heat_plot = df_heat.copy().drop(
            [
                "Heat bus_excess_sink",
                "Heat demand",
                "TES (2386.3kWh) SOC",
                "Heat pump",
            ],
            axis=1,
        )
        df_plot = pd.concat([df_plot, df_heat_plot], axis=1)
    except (KeyError):
        print("TES not installed, flow won't be printed")

    df_plot.rename(
        columns={"Electricity grid_feedin_sink_sink": "Electricity grid feed-in"},
        inplace="True",
    )
    switch_german = False

    if switch_german:
        parameters_timeseries = {
            "Electricity grid_consumption_period": "Netzbezug (el)",
            "Solar inverter": "Wechselrichter Austritt (el)",
            "Electricity bus_excess_sink": "Überschuss (el)",
            "Electricity demand": "Bedarf (el)",
            "Electricity grid_feedin_sink_sink": "Netzeinspeisung (el)",
            "Heat pump": "Bedarf WP (el)",
            "TES output power": "TES Austritt (therm)",
            "TES input power": "TES Eintritt (therm)",
            "PV bus_excess_sink": "Überschuss PV (el)",
        }

        for key, param in parameters_timeseries.items():
            if key in df_plot.columns.values:
                df_plot.rename(columns={key: param}, inplace="True")

    plt.title("Battery, heat pump and grid feed-in flows", color="black")
    df_plot.plot(figsize=(4, 2), alpha=0.6).legend(
        bbox_to_anchor=(0.6, -0.6),
        ncol=1,
        # mode="expand",
        facecolor="white",
        framealpha=0,
    )
    if switch_german:
        plt.xlabel("Zeit")
    else:
        plt.xlabel("Time")
    plt.ylabel("kW")
    plt.ylim(-1000, 1500)
    plt.grid(b=True, which="major", axis="both", color="white", linestyle="-")
    plt.minorticks_on()
    plt.grid(b=True, which="minor", axis="both", color="white", linestyle=":")
    # plt.tight_layout(rect=(0.02, 0.12, 1, 1))
    # plt.show()

    # save plot into output directory
    plt.savefig(
        os.path.join(timeseries_directory, f"plot_{timeseries_name[:-5]}_{period}.pdf"),
        bbox_inches="tight",
    )


def plot_psi_matrix(scenario_dict, variable_name, outputs_directory, basis_value):
    """
    :param scenario_dict:
    :return:
    """
    LCOE = pd.DataFrame()
    INSTCAP = pd.DataFrame()
    TOTALCOSTS = pd.DataFrame()
    for scenario_name in scenario_dict.keys():
        sc_step = scenario_name.split("_")[::-1][0]
        if outputs_directory == None:
            outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
            scenario_folder = os.path.join(outputs_directory, scenario_name)
        else:
            scenario_folder = os.path.join(outputs_directory, scenario_name)
            if not os.path.isdir(scenario_folder):
                logging.warning(f"The scenario folder {scenario_name} does not exist.")
        loop_output_directory = os.path.join(
            scenario_folder, "loop_outputs_" + str(variable_name)
        )
        if not os.path.isdir(loop_output_directory):
            logging.warning(
                f"The loop output folder {loop_output_directory} does not exist. "
                f"Please check the variable_name"
            )
        # parse through scalars folder and read in all excel sheets
        for filepath in list(
            glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
        ):

            file_sheet1 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="cost_matrix1"
            )
            file_sheet2 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="scalar_matrix1"
            )
            file_sheet3 = pd.read_excel(
                filepath, header=0, index_col=0, sheet_name="scalars1"
            )

            # get variable value from filepath
            split_path = filepath.split("_")
            get_step = split_path[::-1][0]
            lt_step = int(get_step.split(".")[0])

            # get LCOE pv and installed capacity
            index = lt_step
            column = str(sc_step)
            #            LCOE.loc[index, "step"] = int(step)
            INSTCAP.loc[index, column] = file_sheet2.at["PV psi", "optimizedAddCap"]
            LCOE.loc[index, column] = file_sheet1.at[
                "PV psi", "levelized_cost_of_energy_of_asset"
            ]
            TOTALCOSTS.loc[index, column] = file_sheet1.at["PV psi", "costs_total"]

    LCOE.sort_index(ascending=False, inplace=True)
    INSTCAP.sort_index(ascending=False, inplace=True)
    TOTALCOSTS.sort_index(ascending=False, inplace=True)
    # select values close to basis value
    basis = pd.DataFrame()
    for column in LCOE.columns:
        value = LCOE[column].iloc[(LCOE[column] - basis_value).abs().argsort()[:1]]
        if value.index[0] is not None:
            basis.loc[column, "lifetime"] = int(value.index[0])

    # plot LCOE
    f, (ax1, ax3) = plt.subplots(1, 2, figsize=(20, 9))
    plt.tick_params(bottom="on")
    sns.set_style("whitegrid", {"axes.grid": True})
    ax1 = plt.subplot(121)
    ax1 = sns.heatmap(
        LCOE, cmap="YlGnBu", cbar_kws={"label": "LCOE in EUR/kWh"}, vmin=0.07
    )
    ax1.set_ylabel("lifetime in years")
    ax1.set_xlabel("specific_costs in EUR")
    #    sns.lineplot(basis.columns, basis[0], ax = ax1)
    ax2 = ax1.twinx()
    ax2.plot(basis.index, basis["lifetime"], color="darkorange", label="SI")
    ax2.set_ylim(5, 25.5)
    ax2.axis("off")

    ax1.set_xticklabels([500, 600, 700, 800, 900, 1000, 1100], minor=False)
    # Create offset transform by 5 points in x direction
    dx = 40 / 72.0
    dy = 0 / 72.0
    offset = mpl.transforms.ScaledTranslation(dx, dy, f.dpi_scale_trans)

    # apply offset transform to all x ticklabels.
    for label in ax1.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)
    for label in ax2.xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)

    ax3 = plt.subplot(122)
    ax3 = sns.heatmap(
        TOTALCOSTS, cmap="YlGnBu", cbar_kws={"label": "Total costs in EUR"}
    )
    ax3.set_ylabel("lifetime in years")
    ax3.set_xlabel("specific costs in EUR")

    plt.tight_layout()

    f.savefig(os.path.join(outputs_directory, f"plot_{scenario_name}_matrix.png",))


def compare_weather_years(
    latitude,
    longitude,
    country,
    static_inputs_directory=None,
    outputs_directory=None,
    user_inputs_mvs_directory=None,
):
    """
    Bar plot that shows yearly aggregated weather parameters: ghi, dni, dhi and temperature.

    Parameters
    ----------
    latitude: float
        latitude of the location
    longitude: float
        longitude of the location
    country: str
        country of simulation
    static_inputs_directory: str
        if None: 'constants.DEFAULT_STATIC_INPUTS_DIRECTORY'
    outputs_directory: str
        if None: 'constants.DEFAULT_OUTPUTS_DIRECTORY
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
        Default: None.
    Returns
    -------
        None
        The plot is saved into the `output_directory`.
    -------
    """

    if static_inputs_directory == None:
        static_inputs_directory = constants.DEFAULT_STATIC_INPUTS_DIRECTORY
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    timeseries_directory = os.path.join(user_inputs_mvs_directory, "time_series")
    if outputs_directory == None:
        outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY

    ghi = pd.DataFrame()
    temp = pd.DataFrame()
    dni = pd.DataFrame()
    dhi = pd.DataFrame()
    electricity_demand = pd.DataFrame()
    heat_demand = pd.DataFrame()

    for file in os.listdir(static_inputs_directory):
        if file.startswith("weatherdata_" + str(latitude) + "_" + str(longitude)):
            year = file.split(".")[2].split("_")[1]
            weatherdata = pd.read_csv(
                os.path.join(static_inputs_directory, file), header=0
            )
            ghi[year] = weatherdata["ghi"]
            temp[year] = weatherdata["temp_air"]
            dni[year] = weatherdata["dni"]
            dhi[year] = weatherdata["dhi"]

    for file in os.listdir(timeseries_directory):
        if file.startswith("electricity_load_"):
            if file.endswith(str(country) + "_5.csv"):
                year = int(file.split(".")[0].split("_")[2])
                electricity_load = pd.read_csv(
                    os.path.join(timeseries_directory, file), header=0
                )
                electricity_demand[year] = electricity_load["kWh"]
        elif file.startswith("heat_load_"):
            if file.endswith(str(country) + "_5.csv"):
                year = int(file.split(".")[0].split("_")[2])
                heat_load = pd.read_csv(
                    os.path.join(timeseries_directory, file), header=0
                )
                heat_demand[year] = heat_load["kWh"]

    ghi = ghi.reindex(sorted(ghi.columns), axis=1)
    temp = temp.reindex(sorted(temp.columns), axis=1)
    dni = dni.reindex(sorted(dni.columns), axis=1)
    dhi = dhi.reindex(sorted(dhi.columns), axis=1)
    electricity_demand = electricity_demand.reindex(
        sorted(electricity_demand.columns), axis=1
    )
    heat_demand = heat_demand.reindex(sorted(electricity_demand.columns), axis=1)

    ghi_sum = ghi.sum(axis=0)
    temp_sum = temp.sum(axis=0)
    dni_sum = dni.sum(axis=0)
    dhi_sum = dhi.sum(axis=0)
    el_sum = electricity_demand.sum(axis=0)
    he_sum = heat_demand.sum(axis=0)

    # data to plot
    n_groups = len(ghi.columns)

    # create plot
    fig = plt.figure(figsize=(11, 7))  # Create matplotlib figure
    ax = fig.add_subplot(111)  # Create matplotlib axes
    bar_width = 0.15
    opacity = 0.8

    ax2 = ax.twinx()

    ghi_sum.plot(
        kind="bar",
        color="tab:orange",
        ax=ax,
        alpha=opacity,
        width=bar_width,
        label="ghi",
        position=3,
    )
    dni_sum.plot(
        kind="bar",
        color="gold",
        ax=ax,
        alpha=opacity,
        width=bar_width,
        label="dni",
        position=2,
    )
    dhi_sum.plot(
        kind="bar",
        color="tab:green",
        ax=ax,
        alpha=opacity,
        width=bar_width,
        label="dhi",
        position=1,
    )
    el_sum.plot(
        kind="bar",
        color="tab:blue",
        ax=ax2,
        alpha=opacity,
        width=bar_width,
        label="electricity load",
        position=0,
    )
    #    he_sum.plot(kind='bar', color = "purple", ax=ax2, alpha = opacity,width=bar_width, label="heat load", position = 0)

    plt.xlabel("year")
    ax.set_ylabel("Irradiance in kW/year")
    ax2.set_ylabel("Demand in kWh/year")
    #    plt.title("yearly energy yield")
    #    plt.xticks(index + bar_width, (ghi.columns))
    ax.set_xlim(ax.get_xlim()[0] - 0.5, ax.get_xlim()[1] + 0.1)
    # Put a legend to the right of the current axis
    ax.legend(loc="lower right", bbox_to_anchor=(-0.05, 0))
    ax2.legend(loc="lower left", bbox_to_anchor=(1.05, 0))
    #    plt.tight_layout()

    # save plot into output directory
    plt.savefig(
        os.path.join(
            outputs_directory, f"plot_compare_weatherdata_{latitude}_{longitude}.png"
        ),
        bbox_inches="tight",
    )


def plot_kpi_loop(
    variable_name, kpi, scenario_dict, outputs_directory=None,
):

    """
    Plots KPI's from the 'mvs_output/scalars_**.xlsx' files in `loop_outputs`
    for a loop over one variable.
    The plot is saved into the `loop_output_directory`.
    Parameters
    ----------
    variable_name: str
        Name of the variable that is changed each loop. Please do not enter
        white spaces within the string.
    kpi: list of str
        List of KPI's to be plotted.
        Possible entries:
            "Degree of NZE"
            "Total costs PV",
            "Installed capacity PV",
            "Total renewable energy use",
            "Renewable share",
            "LCOE PV",
            "self consumption",
            "self sufficiency",
            "Degree of autonomy",
            "Total non-renewable energy use",
            "Total costs",
            "Total annual production"
    scenario_dict: dictionary
        dictionary with the scenario names that should be compared as keys and
        a label for the scenario as value. e.g.: {"Scenario_A1" : "si", "Scenario_A2": "cpv"}
         Notice: all scenarios you want to compare, need to include the
         loop-outputs for the same variable / steps. The scenario names
         should follow the scheme: "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    outputs_directory: str
        Path to output directory.
        Default: constants.DEFAULT_OUTPUTS_DIRECTORY
    Returns
    -------
        None
        saves figure into `loop_output_directory`
    -------
    """
    output_dict = {}
    for scenario_name in scenario_dict.keys():
        if outputs_directory == None:
            outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
            scenario_folder = os.path.join(outputs_directory, scenario_name)
        else:
            scenario_folder = os.path.join(outputs_directory, scenario_name)
            if not os.path.isdir(scenario_folder):
                logging.warning(f"The scenario folder {scenario_name} does not exist.")
        loop_output_directory = os.path.join(
            scenario_folder, "loop_outputs_" + str(variable_name)
        )
        if not os.path.isdir(loop_output_directory):
            logging.warning(
                f"The loop output folder {loop_output_directory} does not exist. "
                f"Please check the variable_name"
            )

        # parse through scalars folder and read in all excel sheets
        output = pd.DataFrame()
        for filepath in list(
            glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
        ):

            file_sheet1 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="cost_matrix1"
            )
            file_sheet2 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="scalar_matrix1"
            )
            file_sheet3 = pd.read_excel(
                filepath, header=0, index_col=0, sheet_name="scalars1"
            )

            # get variable value from filepath
            split_path = filepath.split("_")
            get_step = split_path[::-1][0]
            get_year = split_path[::-1][1]
            step = int(get_step.split(".")[0])
            year = int(split_path[::-1][1])

            # get variable value from filepath
            ending = str(get_year) + "_" + str(get_step)

            for filepath_t in list(
                glob.glob(os.path.join(loop_output_directory, "timeseries", "*.xlsx"))
            ):
                if filepath_t.endswith(ending) is True:
                    timeseries = pd.read_excel(filepath_t, sheet_name="Electricity bus")
                    if "Heat pump" in timeseries.columns:
                        total_hp_electricity_demand = abs(sum(timeseries["Heat pump"]))
                    else:
                        total_hp_electricity_demand = 0

            # get all different pv assets
            csv_directory = os.path.join(
                scenario_folder,
                "mvs_outputs_loop_"
                + str(variable_name)
                + "_"
                + str(year)
                + "_"
                + str(step),
                "inputs",
                "csv_elements",
            )
            energyProduction = pd.read_csv(
                os.path.join(csv_directory, "energyProduction.csv"), index_col=0
            )
            energyProduction = energyProduction.drop(["unit"], axis=1)
            pv_labels = energyProduction.columns
            # get total costs pv and installed capacity
            index = str(year) + "_" + str(step)
            output.loc[index, "step"] = int(step)
            output.loc[index, "year"] = int(year)
            output.loc[index, "Total costs PV"] = 0
            output.loc[index, "Total annual production"] = 0
            output.loc[index, "Installed capacity PV"] = 0
            counter = 1
            for pv in pv_labels:
                output.loc[index, "Total costs PV"] = (
                    output.loc[index, "Total costs PV"]
                    + file_sheet1.at[pv, "costs_total"]
                )
                output.loc[index, "Installed capacity PV"] = (
                    output.loc[index, "Installed capacity PV"]
                    + file_sheet2.at[pv, "optimizedAddCap"]
                )
                output.loc[index, "ESS Li-Ion storage capacity"] = file_sheet2.at[
                    "ESS Li-Ion storage capacity", "optimizedAddCap"
                ]
                output.loc[index, "Total flow ESS Li-Ion storage"] = file_sheet2.at[
                    "ESS Li-Ion storage capacity", "total_flow"
                ]
                output.loc[index, "Total renewable energy"] = file_sheet3.at[
                    "Total renewable energy use", 0
                ]
                output.loc[index, "Renewable factor"] = file_sheet3.at[
                    "Renewable factor", 0
                ]
                if counter == 1:
                    output.loc[index, "LCOE PV"] = file_sheet1.at[
                        pv, "levelized_cost_of_energy_of_asset"
                    ]
                output.loc[index, "Self consumption"] = file_sheet3.at[
                    "Onsite energy fraction", 0
                ]
                output.loc[index, "Self sufficiency"] = file_sheet3.at[
                    "Onsite energy matching", 0
                ]
                output.loc[index, "Degree of autonomy"] = file_sheet3.at[
                    "Degree of autonomy", 0
                ]
                output.loc[index, "Total_feedinElectricity"] = file_sheet3.at[
                    "Total_feedinElectricity", 0
                ]
                output.loc[index, "Total_excessElectricity"] = file_sheet3.at[
                    "Total_excessElectricity", 0
                ]
                output.loc[
                    index, "Total_consumption_from_energy_providerElectricity"
                ] = file_sheet3.at[
                    "Total_consumption_from_energy_providerElectricity", 0
                ]
                if "Installed capacity per heat pump" in file_sheet3.index:
                    output.loc[
                        index, "Installed capacity per heat pump"
                    ] = file_sheet3.at["Installed capacity per heat pump", 0]
                    output.loc[index, "Total costs heat pump"] = file_sheet1.at[
                        "Heat pump", "costs_total"
                    ]
                else:
                    output.loc[index, "Installed capacity per heat pump"] = 0
                    output.loc[index, "Total costs heat pump"] = 0
                output.loc[
                    index, "Total electricity demand heat pump"
                ] = total_hp_electricity_demand
                if "Heat pump" in file_sheet2.index:
                    output.loc[index, "Installed heat pump capacity"] = file_sheet2.at[
                        "Heat pump", "optimizedAddCap"
                    ]
                else:
                    output.loc[index, "Installed heat pump capacity"] = 0
                if "TES storage capacity" in file_sheet2.index:
                    output.loc[index, "Installed TES capacity"] = file_sheet2.at[
                        "TES storage capacity", "optimizedAddCap"
                    ]
                    output.loc[index, "Total costs TES"] = file_sheet1.at[
                        "TES storage capacity", "costs_total"
                    ]
                else:
                    output.loc[index, "Installed TES capacity"] = 0
                    output.loc[index, "Total costs TES"] = 0
                output.loc[index, "Renewable factor"] = file_sheet3.at[
                    "Renewable factor", 0
                ]
                output.loc[index, "Total emissions"] = file_sheet3.at[
                    "Total emissions", 0
                ]
                output.loc[index, "Total non-renewable energy"] = file_sheet3.at[
                    "Total non-renewable energy use", 0
                ]
                output.loc[index, "Degree of NZE"] = file_sheet3.at["Degree of NZE", 0]
                output.loc[index, "Total costs"] = file_sheet3.at["costs_total", 0]
                output.loc[index, "Total annual production"] = (
                    output.loc[index, "Total annual production"]
                    + file_sheet2.at[pv, "annual_total_flow"]
                )
                counter += 1

            output_dict_column = output.to_dict()
            output_dict[scenario_dict[scenario_name]] = output_dict_column

    # define y labels
    y_title = {
        "Total costs": "Total costs \n in EUR",
        "Total costs PV": "Costs total PV \n in EUR",
        "Installed capacity PV": "Installed capacity \nPV in kWp",
        "ESS Li-Ion storage capacity": "Installed capacity \nESS Li-Ion in kW",
        "Total flow ESS Li-Ion storage": "Total annual flow \nESS Li-Ion in kW",
        "Total renewable energy": "Total renewable \nenergy in kWh",
        "Renewable factor": "Renewable factor \nin %",
        "LCOE PV": "LCOE PV \nin EUR/kWh",
        "Self consumption": "Self consumption \nin %",
        "Self sufficiency": "Self sufficiency \nin %",
        "Degree of autonomy": "Degree of \nautonomy in %",
        "Total emissions": "Total emissions \nin kgCO2eq/kWh",
        "Total non-renewable energy": "Total non-renewable \n energy in kWh",
        "Degree of NZE": "Degree of NZE \n in %",
        "Total_feedinElectricity": "Total grid \nfeed-in in kW",
        "Total annual production": "Total annual \n production in kWh",
        "Total_excessElectricity": "Total excess \nelectricity \n in kW",
        "Total_consumption_from_grid": "Total \nconsumption from \ngrid in kW",
        "Installed TES capacity": "Installed TES \ncapacity in kWh",
        "Installed heat pump capacity": "Installed HP \ncapacity in kW",
        "Total electricity demand heat pump": "Total electricity \ndemand HP in kW",
        "Installed capacity per heat pump": "Installed \ncapacity per HP \nin kW",
        "Total costs heat pump": "Total costs HP \nin EUR",
        "Total costs TES": "Total costs TES \nin EUR",
    }

    output.sort_index(inplace=True)

    # plot
    hight = len(kpi) * 2
    fig = plt.figure(figsize=(7, hight))
    rows = len(kpi)
    num = (
        rows * 100 + 11
    )  # the setting for number of rows | number of columns | row number
    for i in kpi:
        ax = fig.add_subplot(num)
        num = num + 1
        for key in output_dict.keys():
            if "Reference" not in key:
                x_min = min(output_dict[key]["step"].values())
                x_max = max(output_dict[key]["step"].values())
        counter = 1
        color_list = [
            "#66c2a5",
            "#fc8d62",
            "#8da0cb",
            "#e78ac3",
            "#a6d854",
            "#ffd92f",
            "#e5c494",
            "#b3b3b3",
        ]
        for key in output_dict.keys():
            color_plot = color_list[list(output_dict.keys()).index(key)]
            df = pd.DataFrame()
            df = df.from_dict(output_dict[key])
            if "Reference" in key and len(df) <= 3:
                for index in df.index:
                    if counter == 1:
                        color = "tab:blue"
                    if counter == 2:
                        color = "orange"
                    data = float(df.at[index, i])
                    base = pd.Series(
                        data=data, index=list(range(int(x_min), int(x_max) + 1))
                    )
                    #                   ax.hlines(y=float(row[i]), xmin=x_min, xmax=x_max, label = key, linestyle='--', color = "orange")
                    base.plot(
                        color=color,
                        style="--",
                        ax=ax,
                        label=str(key),
                        legend=False,
                        sharex=True,
                    )
                counter += 1
            else:
                style_plot = ["+", ".", "*"]
                count = 0
                years = []
                for df_year in df.year:
                    if df_year not in years:
                        years.append(df_year)

                number_of_loops = len(df.step) / len(years)

                try:
                    for pos_year_in_loop in np.arange(0, len(df.step), number_of_loops):
                        df_plot = df.copy()
                        for pos, index in enumerate(df.index):
                            if pos not in np.arange(
                                pos_year_in_loop, pos_year_in_loop + number_of_loops
                            ):
                                df_plot = df_plot.drop(index)

                        df_plot.plot(
                            x="step",
                            y=i,
                            style=style_plot[count],
                            ax=ax,
                            color=color_plot,
                            label=key + " " + str(int(years[count])),
                            legend=False,
                            sharex=True,
                            xticks=df.step,
                        )
                        count += 1
                    ax.set_ylabel(y_title[i])
                    ax.set_xlabel(variable_name)
                    ax.get_yaxis().set_label_coords(-0.13, 0.5)
                    ax.set_xticks(df.step)
                    ax.set_xlim(ax.get_xlim()[0] - 0.5, ax.get_xlim()[1] + 0.5)
                except:
                    pass

    plt.tight_layout(rect=(0.07, 0.16, 1, 1))

    plt.xticks(rotation=45)

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    fig.legend(
        ncol=3,
        handles=by_label.values(),
        labels=by_label.keys(),
        loc="lower center",
        # mode="expand",
        facecolor="white",
        framealpha=0,
    )

    #    handles, labels = ax.get_legend_handles_labels()
    #    fig.legend(
    #        handles, labels, loc="lower left", mode="expand",
    #    )

    name = ""
    for scenario_name in scenario_dict.keys():
        name = name + "_" + str(scenario_name)

    fig.savefig(
        os.path.join(
            outputs_directory,
            "plot_scalars" + str(name) + "_" + str(variable_name) + ".png",
        )
    )


def plot_facades(
    variable_name, kpi, scenario_name, outputs_directory=None,
):

    """
    Plots KPI's from the 'mvs_output/scalars_**.xlsx' files in `loop_outputs`
    for a loop over one variable.
    The plot is saved into the `loop_output_directory`.
    Parameters
    ----------
    variable_name: str
        Name of the variable that is changed each loop. Please do not enter
        white spaces within the string.
    kpi: list of str
        List of KPI's to be plotted.
        Possible entries:
            "Costs total PV",
            "LCOE PV",
            "Installed capacity PV",
    scenario_name: str
        The scenario names
         should follow the scheme: "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    outputs_directory: str
        Path to output directory.
        Default: constants.DEFAULT_OUTPUTS_DIRECTORY
    Returns
    -------
        None
        saves figure into `loop_output_directory`
    -------
    """
    if outputs_directory == None:
        outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
        scenario_folder = os.path.join(outputs_directory, scenario_name)
    else:
        scenario_folder = os.path.join(outputs_directory, scenario_name)
        if not os.path.isdir(scenario_folder):
            logging.warning(f"The scenario folder {scenario_name} does not exist.")
    loop_output_directory = os.path.join(
        scenario_folder, "loop_outputs_" + str(variable_name)
    )
    if not os.path.isdir(loop_output_directory):
        logging.warning(
            f"The loop output folder {loop_output_directory} does not exist. "
            f"Please check the variable_name"
        )
    # parse through scalars folder and read in all excel sheets
    d = {}
    i = 0
    for filepath in list(
        glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
    ):

        file_sheet1 = pd.read_excel(
            filepath, header=0, index_col=1, sheet_name="cost_matrix1"
        )
        file_sheet2 = pd.read_excel(
            filepath, header=0, index_col=1, sheet_name="scalar_matrix1"
        )
        file_sheet3 = pd.read_excel(
            filepath, header=0, index_col=0, sheet_name="scalars1"
        )

        # get variable value from filepath
        split_path = filepath.split("_")
        get_step = split_path[::-1][0]
        step = get_step.split(".")[0]
        year = int(split_path[::-1][1])
        # get all different pv assets
        csv_directory = os.path.join(
            scenario_folder,
            "mvs_outputs_loop_"
            + str(variable_name)
            + "_"
            + str(year)
            + "_"
            + str(step),
            "inputs",
            "csv_elements",
        )
        energyProduction = pd.read_csv(
            os.path.join(csv_directory, "energyProduction.csv"), index_col=0
        )
        energyProduction = energyProduction.drop(["unit"], axis=1)
        pv_labels = energyProduction.columns
        # get total costs pv and installed capacity
        index = str(year)  # + "_" + str(step)
        #            output.loc[index, "step"] = int(step)
        #            output.loc[index, "year"] = int(year)
        #            costs_total=0
        #            LCOE_total=0
        #            installed_capa_total = 0
        for pv in pv_labels:
            if i == 0:
                d["costs_total"] = pd.DataFrame()
                d["LCOE"] = pd.DataFrame()
                d["installedCap"] = pd.DataFrame()
                d["production"] = pd.DataFrame()

            d["costs_total"].loc[index, pv] = int(year)
            d["costs_total"].loc[index, pv] = file_sheet1.at[pv, "costs_total"]
            d["LCOE"].loc[index, pv] = file_sheet1.at[
                pv, "levelized_cost_of_energy_of_asset"
            ]
            d["installedCap"].loc[index, pv] = file_sheet2.at[pv, "optimizedAddCap"]
            d["production"].loc[index, pv] = file_sheet2.at[pv, "annual_total_flow"]

        i += 1

    output_min = {}
    output_diff = {}
    output_max = {}
    for key in d.keys():
        output_min[key] = pd.DataFrame()
        output_diff[key] = pd.DataFrame()
        output_max[key] = pd.DataFrame()
        for c in d[key].columns:
            if c.endswith("1"):
                facade = "rooftop"
            elif c.endswith("2"):
                facade = "south facade"
            elif c.endswith("3"):
                facade = "east facade"
            elif c.endswith("4"):
                facade = "west facade"
            output_min[key].loc[facade, str(c)[:-1]] = d[key][c].min()
            output_diff[key].loc[facade, str(c)[:-1]] = (
                d[key][c].max() - d[key][c].min()
            )
            output_max[key].loc[facade, str(c)[:-1]] = d[key][c].max()

    # define y labels
    y_title = {
        "Costs total PV": "Costs total PV \n in EUR",
        "Installed capacity PV": "Installed capacity \nPV in kWp",
        "LCOE PV": "LCOE PV \nin EUR/kWh",
        "Total annual production": "Total annual \n production in kWh",
    }

    #    output.sort_index(inplace=True)
    # plot
    hight = len(d.keys()) * 2
    fig = plt.figure(figsize=(7, hight))
    fig.subplots_adjust(bottom=0.2)
    rows = len(d.keys())
    num = (
        rows * 100 + 11
    )  # the setting for number of rows | number of columns | row number

    color_1 = sns.color_palette()
    color_2 = sns.color_palette("pastel")
    counter = 1
    for key in output_min.keys():
        ax = fig.add_subplot(num)
        num = num + 1
        df_min = pd.DataFrame()
        df_diff = pd.DataFrame()
        df_max = pd.DataFrame()
        df_min = df_min.from_dict(output_min[key])
        df_diff = df_diff.from_dict(output_diff[key])
        df_max = df_max.from_dict(output_max[key])

        df_max.plot(
            kind="bar",
            ax=ax,
            legend=False,
            label=str(),
            sharex=True,
            color=color_2,
            linewidth=0.5,
        )

        df_min.plot(
            kind="bar",
            ax=ax,
            label=key,
            legend=False,
            sharex=True,
            color=color_1,
            linewidth=0.5,
        )

        ax.set_ylabel(str(key))
        ax.set_xlabel("facades")
        ax.get_yaxis().set_label_coords(-0.15, 0.5)
        ax.set_xlim(ax.get_xlim()[0] - 0.5, ax.get_xlim()[1] + 0.5)
        ax.grid(b=True, which="major", axis="both", color="w", linewidth=1.0)
        ax.grid(b=True, which="minor", axis="both", color="w", linewidth=0.5)
    plt.tight_layout(rect=(0.02, 0.03, 1, 1))

    plt.xticks(rotation=45)
    fig.legend(
        df_min.columns, loc="lower left", mode="expand",
    )

    fig.savefig(
        os.path.join(
            outputs_directory,
            "plot_facades_" + str(scenario_name) + "_" + str(variable_name) + ".png",
        )
    )


def plot_compare_scenarios(variable_name, kpi, scenario_list, outputs_directory=None):
    """
    kpi: list of str
        List of KPI's to be plotted.
        Possible entries:
            "Degree of NZE"
            "Costs total PV",
            "Installed capacity PV",
            "Total renewable energy use",
            "Renewable share",
            "LCOE PV",
            "self consumption",
            "self sufficiency",
            "Degree of autonomy",
            "Total non-renewable energy use"
    scenario_list: list
        List with the scenario names that should be compared
         Notice: all scenarios you want to compare, need to include the
         loop-outputs for the same variable / steps. The scenario names
         should follow the scheme: "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    outputs_directory: str
        Path to output directory.
        Default: constants.DEFAULT_OUTPUTS_DIRECTORY
    Returns
    -------
        None
        saves figure into `loop_output_directory`
    -------
    """
    # height = len(kpi) * 2
    # fig = plt.figure(figsize=(7, height))

    output_dict = {}
    for scenario_name in scenario_list:
        if outputs_directory == None:
            outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
            scenario_folder = os.path.join(outputs_directory, scenario_name)
        else:
            scenario_folder = os.path.join(outputs_directory, scenario_name)
            if not os.path.isdir(scenario_folder):
                logging.warning(f"The scenario folder {scenario_name} does not exist.")
        loop_output_directory = os.path.join(
            scenario_folder, "loop_outputs_" + str(variable_name)
        )
        if not os.path.isdir(loop_output_directory):
            logging.warning(
                f"The loop output folder {loop_output_directory} does not exist. "
                f"Please check the variable_name"
            )
        # parse through scalars folder and read in all excel sheets
        output = pd.DataFrame()
        for filepath_s in list(
            glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
        ):
            file_sheet1 = pd.read_excel(
                filepath_s, header=0, index_col=1, sheet_name="cost_matrix1"
            )
            file_sheet2 = pd.read_excel(
                filepath_s, header=0, index_col=1, sheet_name="scalar_matrix1"
            )
            file_sheet3 = pd.read_excel(
                filepath_s, header=0, index_col=0, sheet_name="scalars1"
            )

            # get variable value from filepath
            split_path = filepath_s.split("_")
            get_step = split_path[::-1][0]
            get_year = split_path[::-1][1]
            step = int(get_step.split(".")[0])
            year = int(split_path[::-1][1])

            # get variable value from filepath
            ending = str(get_year) + "_" + str(get_step)

            for filepath_t in list(
                glob.glob(os.path.join(loop_output_directory, "timeseries", "*.xlsx"))
            ):
                if filepath_t.endswith(ending) is True:
                    timeseries = pd.read_excel(filepath_t, sheet_name="Electricity bus")
                    if "Heat pump" in timeseries.columns:
                        total_hp_electricity_demand = abs(sum(timeseries["Heat pump"]))
                    else:
                        total_hp_electricity_demand = 0

            # get all different pv assets
            csv_directory = os.path.join(
                scenario_folder,
                "mvs_outputs_loop_"
                + str(variable_name)
                + "_"
                + str(year)
                + "_"
                + str(step),
                "inputs",
                "csv_elements",
            )
            energyProduction = pd.read_csv(
                os.path.join(csv_directory, "energyProduction.csv"), index_col=0
            )
            energyProduction = energyProduction.drop(["unit"], axis=1)
            pv_labels = energyProduction.columns
            # get total costs pv and installed capacity
            index = str(year) + "_" + str(step)
            output.loc[index, "step"] = int(step)
            output.loc[index, "year"] = int(year)
            output.loc[index, "Total annual production PV"] = 0
            output.loc[index, "Installed capacity PV"] = 0
            output.loc[index, "Total costs PV"] = 0
            counter = 1
            for pv in pv_labels:
                output.loc[index, "Total costs PV"] = (
                    output.loc[index, "Total costs PV"]
                    + file_sheet1.at[pv, "costs_total"]
                )
                output.loc[index, "Total costs"] = file_sheet3.at["costs_total", 0]
                output.loc[index, "Installed capacity PV"] = (
                    output.loc[index, "Installed capacity PV"]
                    + file_sheet2.at[pv, "optimizedAddCap"]
                )
                output.loc[index, "Total renewable energy"] = file_sheet3.at[
                    "Total renewable energy use", 0
                ]
                output.loc[index, "Total demand electricity"] = file_sheet3.at[
                    "Total_demandElectricity", 0
                ]
                output.loc[index, "Total_excessElectricity"] = file_sheet3.at[
                    "Total_excessElectricity", 0
                ]
                output.loc[index, "Total_feedinElectricity"] = file_sheet3.at[
                    "Total_feedinElectricity", 0
                ]
                output.loc[index, "Total_consumption_from_grid"] = file_sheet3.at[
                    "Total_consumption_from_energy_providerElectricity", 0
                ]
                try:
                    output.loc[index, "ESS Li-Ion storage capacity"] = file_sheet2.at[
                        "ESS Li-Ion storage capacity", "optimizedAddCap"
                    ]
                    output.loc[index, "Total flow ESS Li-Ion storage"] = file_sheet2.at[
                        "ESS Li-Ion storage capacity", "total_flow"
                    ]
                    output.loc[
                        index, "Total costs of ESS Li-Ion storage"
                    ] = file_sheet1.at["ESS Li-Ion storage capacity", "costs_total"]
                except KeyError:
                    output.loc[index, "ESS Li-Ion storage capacity"] = 0
                    output.loc[index, "Total flow ESS Li-Ion storage"] = 0
                    output.loc[index, "Total costs of ESS Li-Ion storage"] = 0

                if "Installed capacity per heat pump" in file_sheet3.index:
                    output.loc[
                        index, "Installed capacity per heat pump"
                    ] = file_sheet3.at["Installed capacity per heat pump", 0]
                    output.loc[index, "Total costs heat pump"] = file_sheet1.at[
                        "Heat pump", "costs_total"
                    ]
                else:
                    output.loc[index, "Installed capacity per heat pump"] = 0
                    output.loc[index, "Total costs heat pump"] = 0
                output.loc[
                    index, "Total electricity demand heat pump"
                ] = total_hp_electricity_demand
                if "Heat pump" in file_sheet2.index:
                    output.loc[index, "Installed heat pump capacity"] = file_sheet2.at[
                        "Heat pump", "optimizedAddCap"
                    ]
                else:
                    output.loc[index, "Installed heat pump capacity"] = 0
                if "TES storage capacity" in file_sheet2.index:
                    output.loc[index, "Installed TES capacity"] = file_sheet2.at[
                        "TES storage capacity", "optimizedAddCap"
                    ]
                    output.loc[index, "Total costs TES"] = file_sheet1.at[
                        "TES storage capacity", "costs_total"
                    ]
                else:
                    output.loc[index, "Installed TES capacity"] = 0
                    output.loc[index, "Total costs TES"] = 0
                output.loc[index, "Renewable factor"] = file_sheet3.at[
                    "Renewable factor", 0
                ]
                if counter == 1:
                    output.loc[index, "LCOE PV"] = file_sheet1.at[
                        pv, "levelized_cost_of_energy_of_asset"
                    ]
                output.loc[
                    index, "Total costs Electricity grid_consumption_source"
                ] = file_sheet1.at["Electricity grid_consumption_source", "costs_total"]
                output.loc[index, "Total costs solar inverter"] = file_sheet1.at[
                    "Solar inverter", "costs_total"
                ]
                output.loc[
                    index, "Total costs electricity grid_feedin"
                ] = file_sheet1.at["Electricity grid_feedin_sink_sink", "costs_total"]
                output.loc[index, "Self consumption"] = (
                    file_sheet3.at["Onsite energy fraction", 0] * 100
                )
                output.loc[index, "Self sufficiency"] = (
                    file_sheet3.at["Onsite energy matching", 0] * 100
                )
                output.loc[index, "Degree of autonomy"] = (
                    file_sheet3.at["Degree of autonomy", 0] * 100
                )
                output.loc[index, "Total emissions"] = file_sheet3.at[
                    "Total emissions", 0
                ]
                output.loc[index, "Total non-renewable energy"] = file_sheet3.at[
                    "Total non-renewable energy use", 0
                ]
                output.loc[index, "Degree of NZE"] = (
                    file_sheet3.at["Degree of NZE", 0] * 100
                )
                output.loc[index, "Total costs"] = file_sheet3.at["costs_total", 0]
                output.loc[index, "Total annual production PV"] = (
                    output.loc[index, "Total annual production PV"]
                    + file_sheet2.at[pv, "annual_total_flow"]
                )
                output.loc[
                    index, "Total annual production solar inverter"
                ] = file_sheet2.at["Solar inverter", "annual_total_flow"]
                counter += 1

            output_dict_column = output.to_dict()
            output_dict[scenario_name] = output_dict_column
    # define y labels

    switch_german = False

    if switch_german:
        y_title = {
            "Total costs": "Gesamtkosten \nin EUR",
            "Total costs PV": "Gesamtkosten PV \n in EUR",
            "Installed capacity PV": "Installierte \nLeistung PV \nin kWp",
            "Total renewable energy": "Gesamte \nerneurbare \nEnergiemenge \nin kWh",
            "Total demand electricity": "Gesamter \elektrischer \nBedarf in kWh",
            "Renewable factor": "Erneuerbarer \nFaktor in %",
            "LCOE PV": "LCOE PV \nin EUR/kWh",
            "Total costs Electricity grid_consumption_source": "Gesamtkosten des \nNetzbezugs \nin EUR",
            "Total costs solar inverter": "Gesamtkosten des \nWechselrichters \nin EUR",
            "Total costs electricity grid_feedin": "Gesamtkosten der \nNetzeinspeisung\n in EUR",
            "ESS Li-Ion storage capacity": "Installierte \nLeistung \nESS Li-Ion in kWh",
            "Total flow ESS Li-Ion storage": "Gesamte jährliche \nLeistung ESS \nLi-Ion in kWh",
            "Total costs of ESS Li-Ion storage": "Gesamtkosten der \nESS Li-Ion in EUR",
            "Self consumption": "Eigenverbrauch \nin %",
            "Self sufficiency": "Grad der \nSelbstversorgung \nin %",
            "Degree of autonomy": "Autarkiegrad in %",
            "Total emissions": "Gesamte \nTHG-Emissionen \nin kgCO2eq/kWh",
            "Total non-renewable energy": "Gesamte \nnicht-erneurbare \n Energiemenge in kWh",
            "Degree of NZE": "Grad der NZE \n in %",
            "Total annual production PV": "Gesamte \ngenerierte \nEnergiemenge PV \nin kWh",
            "Total annual production solar inverter": "Gesamte \nAC-Energiemenge \nWechselrichter \n in kWh",
            "Total_excessElectricity": "Gesamter \nelektrischer \nÜberschuss \n in kWh",
            "Total_feedinElectricity": "Gesamte \neingespeiste \nEnergiemenge \nin kWh",
            "Total_consumption_from_grid": "Gesamter \nNetzbezug in kWh",
            "Installed TES capacity": "Installierte TES \nKapazität in kWh",
            "Installed heat pump capacity": "Installierte WP \nKapazität in kWh",
            "Total electricity demand heat pump": "Gesamter \nelektrischer \nBedarf WP in kWh",
            "Installed capacity per heat pump": "Installierte \nKapazität pro WP \nin kWh",
            "Total costs heat pump": "Gesamtkosten WP \nin EUR",
            "Total costs TES": "Gesamtkosten TES \nin EUR",
        }
    else:
        y_title = {
            "Total costs": "Total costs \nin EUR",
            "Total costs PV": "Total costs PV \n in EUR",
            "Installed capacity PV": "Installed \ncapacity PV \nin kWp",
            "Total renewable energy": "Total renewable \nenergy in kWh",
            "Total demand electricity": "Total demand \nelectricity in kWh",
            "Renewable factor": "Renewable factor \nin %",
            "LCOE PV": "LCOE PV \nin EUR/kWh",
            "Total costs Electricity grid_consumption_source": "Total costs of grid \nconsumption in EUR",
            "Total costs solar inverter": "Total costs of \nsolar inverter \nin EUR",
            "Total costs electricity grid_feedin": "Total costs of grid \nfeed-in in EUR",
            "ESS Li-Ion storage capacity": "Installed capacity \nESS Li-Ion in kWh",
            "Total flow ESS Li-Ion storage": "Total annual flow \nESS Li-Ion in kWh",
            "Total costs of ESS Li-Ion storage": "Total costs of \nESS Li-Ion in EUR",
            "Self consumption": "Self consumption \nin %",
            "Self sufficiency": "Self sufficiency \nin %",
            "Degree of autonomy": "Degree of \nautonomy in %",
            "Total emissions": "Total emissions \nin kgCO2eq/kWh",
            "Total non-renewable energy": "Total \nnon-renewable \n energy in kWh",
            "Degree of NZE": "Degree of NZE \n in %",
            "Total annual production PV": "Total electricity \nproduction PV \nin kWh",
            "Total annual production solar inverter": "Total electricity \noutput solar inverter \n in kWh",
            "Total_excessElectricity": "Total excess \nelectricity \n in kWh",
            "Total_feedinElectricity": "Total grid \nfeed-in in kWh",
            "Total_consumption_from_grid": "Total \nconsumption from \ngrid in kWh",
            "Installed TES capacity": "Installed TES \ncapacity in kWh",
            "Installed heat pump capacity": "Installed HP \ncapacity in kWh",
            "Total electricity demand heat pump": "Total electricity \ndemand HP in kWh",
            "Installed capacity per heat pump": "Installed \ncapacity per HP \nin kWh",
            "Total costs heat pump": "Total costs HP \nin EUR",
            "Total costs TES": "Total costs TES \nin EUR",
        }

    output.sort_index(inplace=True)

    # plot
    height = len(kpi) * 2.5
    fig = plt.figure(figsize=(4, height))
    color_1 = sns.color_palette()
    color_2 = sns.color_palette("pastel")
    rows = len(kpi)
    num = (
        rows * 100 + 11
    )  # the setting for number of rows | number of columns | row number

    for i in kpi:
        dict_y_kpi = {
            "Self consumption": [0, 100],
            "Total annual production PV": [0, 3500000],
            "Degree of NZE": [0, 250],
            "Degree of autonomy": [0, 100],
            # "Total annual production solar inverter": [],
            "Total electricity demand heat pump": [0, 13000000],
            "Total_excessElectricity": [0, 80000],
            "Total_feedinElectricity": [0, 1100000],
            # "Total demand electricity": [],
            "Total_consumption_from_grid": [0, 11000000],
            # "Total flow ESS Li-Ion storage": [],
            "Total costs": [0, 51000000],
            "Total costs heat pump": [0, 12500000],
            "Total costs Electricity grid_consumption_source": [0, 51000000],
            "Total costs TES": [0, 1400000],
            "Total costs solar inverter": [0, 410000],
            "Total costs electricity grid_feedin": [-625000, 0],
            "Total costs of ESS Li-Ion storage": [0, 450000],
            # "Total costs PV": [],
            # "Installed capacity PV": [],
            # "Installed heat pump capacity": [],
            # "Installed capacity per heat pump": [],
            # "Installed TES capacity": [],
            # "ESS Li-Ion storage capacity": [],
            "Total emissions": [0, 4000000],
        }
        ax = fig.add_subplot(num)
        num = num + 1

        min_value_year = []
        max_value_year = []
        diff_value_year = []

        for key in output_dict.keys():
            df = pd.DataFrame()
            df = df.from_dict(output_dict[key])

            max_value_year.append(max(df[i]))
            min_value_year.append(min(df[i]))
            diff_value_year.append(max(df[i]) - min(df[i]))

        scenario_name_ending = []
        for scenario_name in scenario_list:
            scenario_name_ending.append(scenario_name.split("_")[1])
        # Plot bar with maximum value of all three years
        label_legend_min = "KPI Minimum der Wetterjahre"
        label_legend_max = "KPI Minimum der Wetterjahre"

        if switch_german:
            ax.bar(
                scenario_name_ending,
                max_value_year,
                color=color_1[0],
                edgecolor=color_1[0],
                linewidth=0.5,
                label=label_legend_min,
            )

            ax.bar(
                scenario_name_ending,
                diff_value_year,
                bottom=min_value_year,
                edgecolor=color_2[0],
                linewidth=0.5,
                color=color_2[0],
                label=label_legend_max,
            )

        else:
            ax.bar(
                scenario_name_ending,
                max_value_year,
                color=color_1[0],
                edgecolor=color_1[0],
                linewidth=0.5,
                label="KPI minimum of weather years",
            )
            # Plot span between minimum and maximum value of all three years
            ax.bar(
                scenario_name_ending,
                diff_value_year,
                bottom=min_value_year,
                edgecolor=color_2[0],
                linewidth=0.5,
                color=color_2[0],
                label="KPI maximum of weather years",
            )

        ax.set_ylabel(y_title[i])
        if switch_german:
            ax.set_xlabel("Szenario")
        else:
            ax.set_xlabel("Scenario")
        ax.get_yaxis().set_label_coords(-0.37, 0.5)
        ax.set_xlim(ax.get_xlim()[0] - 0.1, ax.get_xlim()[1] + 0.1)
        if i in dict_y_kpi.keys():
            ax.set_ylim(dict_y_kpi[i])
        # if i == "Total costs electricity grid_feedin":
        #     ax.set_ylim([-610000, 0])
        # else:
        #     ax.set_ylim([0, 1100000])
        # Print minor and major grid lines for better readability
        ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] + ax.get_ylim()[1] * 0.1)
        ax.grid(b=True, which="major", axis="both", color="w", linewidth=1.0)
        ax.grid(b=True, which="minor", axis="both", color="w", linewidth=0.5)

    plt.tight_layout(rect=(-0.12, 0.08, 1, 1))

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        # ncol=2,
        loc="lower center",
        # mode="expand",
        facecolor="white",
        framealpha=0,
    )

    name = ""
    for scenario_name in scenario_name_ending:
        name = name + "_" + str(scenario_name)

    fig.savefig(
        os.path.join(outputs_directory, "plot_PeroSi_CPV_Si" + str(name) + ".png")
    )
    fig.savefig(
        os.path.join(outputs_directory, "plot_PeroSi_CPV_Si" + str(name) + ".pdf")
    )


def plot_compare_technologies(
    variable_name, kpi, scenario_list, outputs_directory=None
):
    """
    kpi: list of str
        List of KPI's to be plotted.
        Possible entries:
            "Degree of NZE"
            "Costs total PV",
            "Installed capacity PV",
            "Total renewable energy use",
            "Renewable share",
            "LCOE PV",
            "self consumption",
            "self sufficiency",
            "Degree of autonomy",
            "Total non-renewable energy use"
    scenario_list: list
        List with the scenario names that should be compared
         Notice: all scenarios you want to compare, need to include the
         loop-outputs for the same variable / steps. The scenario names
         should follow the scheme: "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    outputs_directory: str
        Path to output directory.
        Default: constants.DEFAULT_OUTPUTS_DIRECTORY
    Returns
    -------
        None
        saves figure into `loop_output_directory`
    -------
    """
    # height = len(kpi) * 2
    # fig = plt.figure(figsize=(7, height))

    output_dict = {}
    for scenario_name in scenario_list:
        if outputs_directory == None:
            outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
            scenario_folder = os.path.join(outputs_directory, scenario_name)
        else:
            scenario_folder = os.path.join(outputs_directory, scenario_name)
            if not os.path.isdir(scenario_folder):
                logging.warning(f"The scenario folder {scenario_name} does not exist.")
        loop_output_directory = os.path.join(
            scenario_folder, "loop_outputs_" + str(variable_name)
        )
        if not os.path.isdir(loop_output_directory):
            logging.warning(
                f"The loop output folder {loop_output_directory} does not exist. "
                f"Please check the variable_name"
            )
        # parse through scalars folder and read in all excel sheets
        output_dict[scenario_name] = {}
        output_dict[scenario_name]["Total costs"] = pd.DataFrame()
        output_dict[scenario_name]["Total costs PV"] = pd.DataFrame()
        output_dict[scenario_name]["LCOE"] = pd.DataFrame()
        output_dict[scenario_name]["Installed capacity PV"] = pd.DataFrame()
        output_dict[scenario_name]["Total annual production"] = pd.DataFrame()
        output_dict[scenario_name]["Total renewable energy"] = pd.DataFrame()
        output_dict[scenario_name]["Renewable factor"] = pd.DataFrame()
        output_dict[scenario_name]["LCOE PV"] = pd.DataFrame()
        output_dict[scenario_name]["Self consumption"] = pd.DataFrame()
        output_dict[scenario_name]["Self sufficiency"] = pd.DataFrame()
        output_dict[scenario_name]["Degree of autonomy"] = pd.DataFrame()
        output_dict[scenario_name]["Total emissions"] = pd.DataFrame()
        output_dict[scenario_name]["Total non-renewable energy"] = pd.DataFrame()
        output_dict[scenario_name]["Degree of NZE"] = pd.DataFrame()

        for filepath in list(
            glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
        ):
            file_sheet1 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="cost_matrix1"
            )
            file_sheet2 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="scalar_matrix1"
            )
            file_sheet3 = pd.read_excel(
                filepath, header=0, index_col=0, sheet_name="scalars1"
            )

            # get variable value from filepath
            split_path = filepath.split("_")
            get_step = split_path[::-1][0]
            step = get_step.split(".")[0]
            year = int(split_path[::-1][1])
            # get all different pv assets
            csv_directory = os.path.join(
                scenario_folder,
                "mvs_outputs_loop_"
                + str(variable_name)
                + "_"
                + str(year)
                + "_"
                + str(step),
                "inputs",
                "csv_elements",
            )
            energyProduction = pd.read_csv(
                os.path.join(csv_directory, "energyProduction.csv"), index_col=0
            )
            energyProduction = energyProduction.drop(["unit"], axis=1)
            pv_labels = energyProduction.columns
            # get total costs pv and installed capacity

            index = str(year)  # + "_" + str(step)

            for pv in pv_labels:
                output_dict[scenario_name]["Total costs"].loc[
                    index, pv
                ] = file_sheet3.at["costs_total", 0]
                output_dict[scenario_name]["Total costs PV"].loc[
                    index, pv
                ] = file_sheet1.at[pv, "costs_total"]
                output_dict[scenario_name]["LCOE"].loc[index, pv] = file_sheet1.at[
                    pv, "levelized_cost_of_energy_of_asset"
                ]
                output_dict[scenario_name]["Installed capacity PV"].loc[
                    index, pv
                ] = file_sheet2.at[pv, "optimizedAddCap"]
                output_dict[scenario_name]["Total annual production"].loc[
                    index, pv
                ] = file_sheet2.at[pv, "annual_total_flow"]
                output_dict[scenario_name]["Total renewable energy"].loc[
                    index, pv
                ] = file_sheet3.at["Total renewable energy use", 0]
                output_dict[scenario_name]["Total renewable energy"].loc[
                    index, pv
                ] = file_sheet3.at["Total_feedinElectricity", 0]
                output_dict[scenario_name]["Total feedin Electricity"].loc[
                    index, pv
                ] = file_sheet3.at["Renewable factor", 0]
                output_dict[scenario_name]["LCOE PV"].loc[index, pv] = file_sheet1.at[
                    pv, "levelized_cost_of_energy_of_asset"
                ]
                output_dict[scenario_name]["Self consumption"].loc[
                    index, pv
                ] = file_sheet3.at["Onsite energy fraction", 0]
                output_dict[scenario_name]["Self sufficiency"].loc[
                    index, pv
                ] = file_sheet3.at["Onsite energy matching", 0]
                output_dict[scenario_name]["Degree of autonomy"].loc[
                    index, pv
                ] = file_sheet3.at["Degree of autonomy", 0]
                output_dict[scenario_name]["Total emissions"].loc[
                    index, pv
                ] = file_sheet3.at["Total emissions", 0]
                output_dict[scenario_name]["Total non-renewable energy"].loc[
                    index, pv
                ] = file_sheet3.at["Total non-renewable energy use", 0]
                output_dict[scenario_name]["Degree of NZE"].loc[
                    index, pv
                ] = file_sheet3.at["Degree of NZE", 0]
    output_min = {}
    output_diff = {}
    output_max = {}
    for scenario_name in output_dict.keys():
        output_min[scenario_name] = {}
        output_diff[scenario_name] = {}
        output_max[scenario_name] = {}

        for key in output_dict[scenario_name].keys():
            output_min[scenario_name][key] = pd.DataFrame()
            output_diff[scenario_name][key] = pd.DataFrame()
            output_max[scenario_name][key] = pd.DataFrame()
            for c in output_dict[scenario_name][key].columns:
                if c.endswith("si"):
                    technology = "SI"
                elif c.endswith("cpv"):
                    technology = "CPV"
                elif c.endswith("psi"):
                    technology = "PSI"
                output_min[scenario_name][key].loc[
                    technology, str(c)[:-1]
                ] = output_dict[scenario_name][key][c].min()
                output_diff[scenario_name][key].loc[technology, str(c)[:-1]] = (
                    output_dict[scenario_name][key][c].max()
                    - output_dict[scenario_name][key][c].min()
                )
                output_max[scenario_name][key].loc[
                    technology, str(c)[:-1]
                ] = output_dict[scenario_name][key][c].max()

    # define y labels
    y_title = {
        "Costs total PV": "Costs total PV \n in EUR",
        "Installed capacity PV": "Installed capacity \nPV in kWp",
        "Total renewable energy": "Total renewable \nenergy in kWh",
        "Renewable factor": "Renewable factor \nin %",
        "LCOE PV": "LCOE PV \nin EUR/kWh",
        "Total_feedinElectricity": "Total grid \nfeed-in in kW",
        "Self consumption": "Self consumption \nin %",
        "Self sufficiency": "Self sufficiency \nin %",
        "Degree of autonomy": "Degree of \nautonomy in %",
        "Total emissions": "Total emissions \nin kgCO2eq/kWh",
        "Total non-renewable energy": "Total non-renewable \n energy in kWh",
        "Degree of NZE": "Degree of NZE \n in %",
        "Total annual production": "Total annual production \n in kWh",
        "Total costs": "Total costs \n in EUR",
    }

    x_title = {
        "Scenario_H1": "Helsinki, Finland",
        "Scenario_H2": "Riga, Latvia",
        "Scenario_H3": "Sevilla, Spain",
        "Scenario_H4": "Paris, France",
        "Scenario_H5": "Budapest, Hungary",
        "Scenario_H6": "Warsaw, Poland",
        "Scenario_H7": "Bukarest, Romania",
        "Scenario_H8": "Rome, Italy",
        "Scenario_H9": "Athens, Greece",
        "Scenario_H10": "Manchester, UK",
        "Scenario_H11": "Berlin, Germany",
        "Scenario_H12": "Madrid, Spain",
    }

    #    output.sort_index(inplace=True)
    # plot
    hight = len(kpi) * 4
    fig = plt.figure(figsize=(15, hight))
    fig.subplots_adjust(bottom=0.2)
    rows = len(kpi)
    num = (
        rows * 100 + 11
    )  # the setting for number of rows | number of columns | row number

    color_1 = sns.color_palette()
    color_2 = sns.color_palette("pastel")

    for i in kpi:
        ax = fig.add_subplot(num)
        num = num + 1

        df_min = pd.DataFrame()
        df_max = pd.DataFrame()

        for scenario_name in output_dict.keys():
            df = pd.DataFrame()
            df = df.from_dict(output_dict[scenario_name][i])
            for pv in df.columns:

                df_min.loc[scenario_name, pv] = df[pv].min()
                df_max.loc[scenario_name, pv] = df[pv].max()

        df_max.plot(
            kind="bar",
            ax=ax,
            legend=False,
            label=str(),
            sharex=True,
            color=color_2,
            linewidth=0.5,
        )

        df_min.plot(
            kind="bar",
            ax=ax,
            label=i,
            legend=False,
            sharex=True,
            color=color_1,
            linewidth=0.5,
        )
        ax.set_xticklabels(x_title.values(), rotation=40, ha="right")
        ax.set_ylabel(y_title[i])
        ax.set_xlabel("technology")
        ax.get_yaxis().set_label_coords(-0.04, 0.5)
        ax.set_xlim(ax.get_xlim()[0] - 0.5, ax.get_xlim()[1] + 0.5)
        ax.grid(b=True, which="major", axis="both", color="w", linewidth=1.0)
        ax.grid(b=True, which="minor", axis="both", color="w", linewidth=0.5)
    plt.tight_layout(rect=(0.02, 0.03, 1, 1))

    #    plt.xticks(x_title.values(),rotation=40, ha="right")
    fig.legend(
        df_min.columns, loc="lower left", mode="expand",
    )

    fig.savefig(
        os.path.join(
            outputs_directory,
            "plot_technologies_"
            + str(scenario_name)
            + "_"
            + str(variable_name)
            + ".png",
        )
    )


if __name__ == "__main__":
    scenario_name = "Scenario_C2"
    # plot_all_flows(
    #     scenario_name=scenario_name,
    #     month=None,
    #     calendar_week=28,
    #     weekday=None,
    #     timeseries_directory=os.path.join(
    #         constants.DEFAULT_OUTPUTS_DIRECTORY,
    #         scenario_name,
    #         "mvs_outputs_loop_storeys_2013_5",
    #     ),
    # )

    # scenario_dict = {"Scenario_C5": "PSI", "Scenario_C7": "CPV", "Scenario_B5": "SI"}
    # scenario_dict = {"Scenario_C6": "PSI", "Scenario_C8": "CPV", "Scenario_A8": "SI"}
    #
    # scenario_dict = {"Scenario_A7": "Scenario A7", "Scenario_A9": "Scenario A9", "Scenario_A11": "Scenario A11", "Scenario_B5": "Scenario B5", "Scenario_B7": "Scenario B7"}
    # plot_kpi_loop(
    #     scenario_dict=scenario_dict,
    #     variable_name="storeys",
    #     kpi=[
    # "Total annual production",
    # "Total_feedinElectricity",
    # "Feedin",
    # "Degree of NZE",
    # "LCOE PV",
    # "Total costs PV",
    # "Total costs heat pump",
    # "Total costs TES",
    # "Installed capacity PV",
    # "Self consumption",
    # "Degree of autonomy",
    # "ESS Li-Ion storage capacity",
    # "Total_consumption_from_grid",
    # "Installed TES capacity",
    # "Installed heat pump capacity",
    # "Installed capacity battery",
    # "Total electricity demand heat pump",
    # "Installed capacity per heat pump",
    #     ],
    # )
    #
    # compare_weather_years(
    #     latitude=latitude,
    #     longitude=longitude,
    #     country=country,
    #     static_inputs_directory=None,
    # )

    # plot_facades(
    #     variable_name="technology",
    #     kpi=["LCOE PV", "Costs total PV", "Installed capacity PV",],
    #     scenario_name="Scenario_E2",
    #     outputs_directory=None,
    # )
    #
    # scenario_list = [
    #     "Scenario_A1",
    #     "Scenario_A3",
    # "Scenario_A5",
    # "Scenario_B1",
    # "Scenario_B3",
    # "Scenario_RefE1",
    # "Scenario_RefG1",
    # ]
    # scenario_list = [
    # "Scenario_A2",
    # "Scenario_A4",
    # "Scenario_A6",
    # "Scenario_B2",
    # "Scenario_B4",
    # "Scenario_RefE2_no_battery",
    # "Scenario_RefG2"
    # ]
    scenario_list = [
        # "Scenario_A1",
        # "Scenario_A3",
        # "Scenario_A5",
        # "Scenario_B1",
        # "Scenario_B3",
        # "Scenario_RefE1",
        # "Scenario_RefG1",
        # "Scenario_A1",
        # "Scenario_A3",
        # "Scenario_B1",
        # "Scenario_RefG1",
        # "Scenario_RefE1",
        # "Scenario_C1",
        # "Scenario_C3",
        # "Scenario_B1",
        # "Scenario_C2",
        # "Scenario_C4",
        # "Scenario_A2",
        # "Scenario_A4",
        # "Scenario_A6",
        # "Scenario_B2",
        # "Scenario_B4",
        # "Scenario_RefE2",
        # "Scenario_RefG2",
        # "Scenario_A2",
        # "Scenario_A4",
        # "Scenario_B2",
        # "Scenario_RefG2",
        # "Scenario_RefE2"
    ]
    plot_compare_scenarios(
        "storeys",
        [
            # "Self consumption",
            # "Total annual production PV",
            # "Total annual production solar inverter",
            # "Total electricity demand heat pump",
            # "Total_excessElectricity",
            # "Total_feedinElectricity",
            # "Total demand electricity",
            # "Total_consumption_from_grid",
            # "Total flow ESS Li-Ion storage",
            # "Total costs",
            # "Total costs Electricity grid_consumption_source",
            # "Total costs heat pump",
            # "Total costs TES",
            # "Total costs solar inverter",
            # "Total costs electricity grid_feedin",
            # "Total costs of ESS Li-Ion storage",
            # "Total costs PV",
            # "Installed capacity PV",
            # "Installed heat pump capacity",
            # "Installed capacity per heat pump",
            # "Installed TES capacity",
            # "ESS Li-Ion storage capacity",
            # "Degree of NZE",
            # "Degree of autonomy",
            # "Total emissions"
        ],
        scenario_list,
    )
    # scenario_list = [
    #     "Scenario_H1",
    #     "Scenario_H2",
    #     "Scenario_H3",
    #     "Scenario_H4",
    #     "Scenario_H5",
    #     "Scenario_H6",
    #     "Scenario_H7",
    #     "Scenario_H8",
    #     "Scenario_H9",
    #     "Scenario_H10",
    #     "Scenario_H11",
    #     "Scenario_H12",
    # ]
    # plot_compare_technologies(
    #     variable_name="technology",
    #     kpi=["Total annual production", "Degree of NZE"],
    #     scenario_list=scenario_list,
    #     outputs_directory=None,
    # )
