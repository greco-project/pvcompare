import pvcompare.constants as constants
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
import logging


def plot_all_flows(
    output_directory=None,
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
    output_directory: str or None
        Path to the directory in which the plot should be saved.
        Default: None.
        If None: `output_directory = constants.DEFAULT_MVS_OUTPUT_DIRECTORY`
    timeseries_directory: str or None
        Path to the timeseries directory.
        If None: `timeseries_directory = output_directory`.
        Default: None.
    timeseries_name: str or None
        Default: timeseries_all_busses.xlsx

    Returns
    -------
        None
        Saves figure into output_directory
    -------


    """
    # check if weekday is a valid day
    if weekday not in range(0, 6, 1):
        logging.error(
            "The weekday is not valid. Please choose a number "
            "between 0-6 with 0:Monaday and 6:Sunday."
        )
    # read timeseries
    if output_directory == None:
        output_directory = constants.DEFAULT_MVS_OUTPUT_DIRECTORY
    if timeseries_directory == None:
        timeseries_directory = output_directory

    wb_data = pd.ExcelFile(os.path.join(timeseries_directory, timeseries_name))
    # Convert to a dataframe the entire workbook
    df = pd.read_excel(
        wb_data, sheet_name="Electricity bus", index_col=0, engine="openpyxl"
    )

    # Converting the index as date
    df.index = pd.to_datetime(df.index)

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
                df = df[df.index.weekday == weekday]
                period = "day_" + str(calendar_week) + "_" + str(weekday)
            else:
                df = df[df.index.week == calendar_week]
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
                period = "week_" + str(calendar_week)
            else:
                logging.warning(
                    "You inserted a month, a caldendar_week and a weekday. In this case the "
                    "plot will cover one weekday only. If you want to plot "
                    "over one month please set the caldendar_week and weekday to 'None'"
                )
                df = df[df.index.week == calendar_week]
                df = df[df.index.weekday == weekday]
                period = "day_" + str(calendar_week) + "_" + str(weekday)
        else:
            df = df[df.index.month == month]
            period = "month_" + str(month)

    # plot
    plt.title("All Flows", color="black")
    df.plot().legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.xlabel("time")
    plt.ylabel("kW")

    # save plot into output directory
    plt.savefig(
        os.path.join(output_directory, f"plot_{timeseries_name[:-5]}_{period}.png"),
        bbox_inches="tight",
    )


def plot_kpi_loop(variable_name, kpi, loop_output_directory=None):

    """
    Plots KPI's from the 'mvs_output/scalars_**.xlsx' files in `loop_outputs`
    for a loop over one variable.

    The 'energyProduction.csv' needs to be saved into 'output_directory'. If the
    loop output is created with :py:func:`~.automated_loop.loop`, the
    'energyProduction.csv' file is copied into the `output_directory` automatically.

    The plot is saved into the `loop_output_directory`.

    Parameters
    ----------
    variable_name: str
        Name of the variable that is changed each loop. Please do not enter
        white spaces within the string.
    kpi: list of str
        List of KPI's to be plotted.
        Possible entries:
            "costs total PV",
            "installed capacity PV",
            "Total renewable energy use",
            "Renewable share",
            "LCOE PV",
            "self consumption",
            "self sufficiency",
            "Degree of autonomy"
    loop_output_directory: str
        Default: None.
        If None: `loop_output_directory = constants.DEFAULT_LOOP_OUTPUT_DIRECTORY`

    Returns
    -------
        None
        saves figure into `loop_output_directory`
    -------


    """

    if loop_output_directory == None:
        loop_output_directory = constants.DEFAULT_LOOP_OUTPUT_DIRECTORY
    # get all different pv assets
    energyProduction = pd.read_csv(
        os.path.join(loop_output_directory, "energyProduction.csv"), index_col=0
    )
    energyProduction = energyProduction.drop(["unit"], axis=1)
    pv_labels = energyProduction.columns
    #    pv_labels = energyProduction.loc["label"]

    output = pd.DataFrame()
    # parse through scalars folder and read in all excel sheets
    for filepath in list(
        glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
    ):

        wb_data = pd.ExcelFile(os.path.join(filepath))
        # Convert to a dataframe the entire workbook
        file_sheet1 = pd.read_excel(
            wb_data, sheet_name="cost_matrix", header=0, index_col=1, engine="openpyxl"
        )

        file_sheet2 = pd.read_excel(
            wb_data,
            header=0,
            index_col=1,
            sheet_name="scalar_matrix",
            engine="openpyxl",
        )

        file_sheet3 = pd.read_excel(
            wb_data, header=0, index_col=0, sheet_name="scalars", engine="openpyxl"
        )

        # get lifetime from filepath
        i_split_one = filepath.split("_")[::-1][0]
        i = i_split_one.split(".")[0]
        # get total costs pv and installed capacity
        for pv in pv_labels:
            output.loc[int(i), "costs total PV"] = file_sheet1.at[pv, "costs_total"]
            output.loc[int(i), "installed capacity PV"] = file_sheet2.at[
                pv, "optimizedAddCap"
            ]
            output.loc[int(i), "Total renewable energy use"] = file_sheet3.at[
                "Total renewable energy use", 0
            ]
            output.loc[int(i), "Renewable share"] = file_sheet3.at["Renewable_share", 0]
            output.loc[int(i), "LCOE PV"] = file_sheet1.at[
                pv, "levelized_cost_of_energy_of_asset"
            ]
            output.loc[int(i), "self consumption"] = file_sheet3.at[
                "Onsite energy fraction", 0
            ]
            output.loc[int(i), "self sufficiency"] = file_sheet3.at[
                "Onsite energy matching", 0
            ]
            output.loc[int(i), "Degree of autonomy"] = file_sheet3.at[
                "Degree of autonomy", 0
            ]

    output.sort_index(inplace=True)

    # plot
    fig = plt.figure()
    rows = len(kpi)
    num = (
        rows * 100 + 11
    )  # the setting for number of rows | number of columns | row number
    for i in kpi:
        ax = fig.add_subplot(num)
        num = num + 1
        output[i].plot(title=i, ax=ax, legend=False)

    fig.text(0.5, 0.0, str(variable_name), ha="center")
    plt.tight_layout()
    plt.show()

    fig.savefig(
        os.path.join(
            loop_output_directory, "plot_scalars_" + str(variable_name) + ".png"
        )
    )


if __name__ == "__main__":

    plot_all_flows(month=None, calendar_week=25, weekday=5)

    # plot_kpi_loop(
    #     variable_name="Number_of_storeys",
    #     kpi=[
    #         "costs total PV",
    #         "Degree of autonomy",
    #         "self consumption",
    #         "self sufficiency",
    #     ],
    #     loop_output_directory=os.path.join(
    #         os.path.dirname(__file__), "data", "CPV_STOREYS"
    #     ),
    # )
