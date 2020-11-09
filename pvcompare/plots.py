import constants
import os
import pandas as pd
import glob
import shutil
import matplotlib.pyplot as plt
import logging


def plot_all_flows(
    mvs_output_directory, period, timeseries_name="timeseries_all_busses.xlsx"
):

    """
    plots all flows of the energy system for a given period of time.

    Parameters
    ----------
    mvs_output_directory: str
        path to output directory
    period: str
        year, month, week or day
    timeseries_name: str
        default: timeseries_all_busses.xlsx

    Returns
    -------


    """

    if mvs_output_directory == None:
        logging.error("Please add a path to your mvs_output_directory.")

    df = pd.read_excel(
        os.path.join(mvs_output_directory, timeseries_name),
        sheet_name="Electricity_bus",
        index_col=0,
    )

    # Plotting
    if period == "month":
        df = df[df.index.month == 6]
    elif period == "week":
        df = df[df.index.week == 25]
    elif period == "day":
        df = df[df.index.week == 25]
        df = df[:25]

    f = plt.figure()

    plt.title("All Flows", color="black")
    df.plot().legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.xlabel("time")
    plt.ylabel("kW")

    plt.savefig(
        os.path.join(mvs_output_directory, f"plot_{timeseries_name}{period}.png"),
        bbox_inches="tight",
    )


if __name__ == "__main__":

    plot_all_flows(
        mvs_output_directory=os.path.join(
            os.path.dirname(__file__), "data/CPV_STOREYS/timeseries/"
        ),
        period="day",
        timeseries_name="timeseries_all_busses_05.xlsx",
    )
