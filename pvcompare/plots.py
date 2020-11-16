import constants
import os
import pandas as pd
import glob
import shutil
import matplotlib.pyplot as plt
import logging


def plot_all_flows(
    period,
    output_directory=None,
    timeseries_directory=None,
    timeseries_name="timeseries_all_busses.xlsx",
):

    """
    Plots all flows of the energy system for a given period of time.

    Parameters
    ----------
    period: str
        year, month, week or day
    output_directory: str or None
        path to the directory in which the plot should be saved
        default: None.
        If None: `output_directory = constants.DEFAULT_MVS_OUTPUT_DIRECTORY`
    timeseries_directory: str or None
        path to the timeseries directory
        default: None.
        If None: `timeseries_directory = output_directory`
    timeseries_name: str or None
        default: timeseries_all_busses.xlsx

    Returns
    -------


    """
    # read timeseries
    if output_directory == None:
        output_directory = constants.DEFAULT_MVS_OUTPUT_DIRECTORY
    if timeseries_directory == None:
        timeseries_directory = output_directory
    df = pd.read_excel(
        os.path.join(timeseries_directory, timeseries_name),
        sheet_name="Electricity_bus",
        index_col=0,
    )

    # define period for the plot
    if period == "month":
        df = df[df.index.month == 6]
    elif period == "week":
        df = df[df.index.week == 25]
    elif period == "day":
        df = df[df.index.week == 25]
        df = df[:25]

    # plot
    plt.title("All Flows", color="black")
    df.plot().legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.xlabel("time")
    plt.ylabel("kW")

    # save plot into output directory
    plt.savefig(
        os.path.join(output_directory, f"plot_{timeseries_name}{period}.png"),
        bbox_inches="tight",
    )


def plot_kpi_loop(variable_name, kpi, loop_output_directory=None):

    """
    plots the total costs from the scalars_**.xlsx files in loop_outputs over
    the changed variable. The plot is saved into the loop_outputs folder.

    Parameters
    ----------
    variable_name: str
        name of the variable that is changed each loop
    kpi: list
        list of KPI's to be plotted
        possible entries:
            "costs total PV"
            "installed capacity PV"
            "Total renewable energy use"
            "Renewable share"
            "LCOE PV"
            "self consumption"
            "self sufficiency"
            "Degree of autonomy"
    loop_output_directory: str
        if None then value will be taken from constants.py

    Returns
        None
        saves figure into `output_directory`
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

        file_sheet1 = pd.read_excel(
            filepath, header=0, index_col=1, sheet_name="cost_matrix"
        )
        file_sheet2 = pd.read_excel(
            filepath, header=0, index_col=1, sheet_name="scalar_matrix"
        )
        file_sheet3 = pd.read_excel(
            filepath, header=0, index_col=0, sheet_name="scalars"
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
            loop_output_directory, "plot_scalars" + str(variable_name) + "_2.png"
        )
    )


if __name__ == "__main__":

    #    plot_all_flows(
    #        period="week",
    #    )

    plot_kpi_loop(
        variable_name="Number of storeys",
        kpi=[
            "costs total PV",
            "Degree of autonomy",
            "self consumption",
            "self sufficiency",
        ],
        loop_output_directory=os.path.join(
            os.path.dirname(__file__), "data", "CPV_STOREYS"
        ),
    )
