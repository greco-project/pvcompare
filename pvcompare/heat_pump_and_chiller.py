"""
This module contains functions for calculating temperature dependent
coefficient of performance (COP) of heat pumps and energy efficiency ratios
(EER) of chillers.

"""

import pandas as pd
import numpy as np
import os
import logging

import oemof.thermal.compression_heatpumps_and_chillers as cmpr_hp_chiller

# internal imports
from pvcompare import constants


def calculate_cops_heat_pump(
    weather, temperature_col="temp_air", input_directory=None, mvs_input_directory=None
):
    r"""
    Calculates the coefficients of performance (COP) of a heat pump.

    # todo same func can be used for chiller (no icing!)

    Temperature dependency is taken into consideration.
    For these calculations the oemof.thermal `calc_cops()` functionality is
    used. Data like quality grade, factor icing and the temperature from which
    heating is assumed to take place is read from the file
    `heat_pump_and_chillers.csv` in the `input_directory`.

    Parameters
    ----------
    weather : :pandas:`pandas.DataFrame<frame>`
        Contains weather data time series. Required: ambient temperature in
        column `temperature_col`.
    temperature_col : str
        Name of column in `weather` containing ambient temperature.
        Default: "temp_air".
    input_directory: str or None
        Path to input directory of pvcompare containing files that describe the
        pv setup and building parameters amongst others. Default:
        DEFAULT_INPUT_DIRECTORY (see :func:`~pvcompare.constants`.
    mvs_input_directory: str or None
        Path to input directory containing files that describe the energy
        system and that are an input to MVS. Default:
        DEFAULT_MVS_OUTPUT_DIRECTORY (see :func:`~pvcompare.constants`.

    Returns
    -------
    cop_series : :pandas:`pandas.Series<series>`
        COP time series of heat pump.

    """
    # read parameters from file
    if input_directory is None:
        input_directory = constants.DEFAULT_INPUT_DIRECTORY
    filename = os.path.join(input_directory, "heat_pump_and_chillers.csv")
    parameters = pd.read_csv(filename, header=0, index_col=0).loc["heat_pump"]

    # prepare parameters for calc_cops
    start_temperature = float(parameters.start_temperature)
    room_temperature = [float(parameters.room_temperature)]
    quality_grade = float(parameters.quality_grade)
    factor_icing = (
        None if parameters.factor_icing == "None" else float(parameters.factor_icing)
    )
    temp_threshold_icing = (
        None
        if parameters.temp_threshold_icing == "None"
        else float(parameters.temp_threshold_icing)
    )

    ambient_temperature = weather[temperature_col].values.tolist()

    # calculate cops of heat pump with oemof thermal
    cop = cmpr_hp_chiller.calc_cops(
        temp_high=room_temperature,
        temp_low=ambient_temperature,
        quality_grade=quality_grade,
        mode="heat_pump",
        temp_threshold_icing=temp_threshold_icing,
        factor_icing=factor_icing,
    )

    # add list of cops to data frame
    df = pd.DataFrame(weather[temperature_col])
    df["cop"] = cop

    # set cop to nan where ambient temperature > heating period temperature
    indices = df.loc[df[temperature_col] > start_temperature].index
    df["cop"][indices] = np.nan

    # extract cop as pd.Series from data frame
    cop_series = df["cop"]

    # save time series to mvs input directory / timeseries
    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    time_series_directory = os.path.join(mvs_input_directory, "time_series")

    logging.info(
        f"The cops of a heat pump are calculated and saved under {time_series_directory}."
    )

    cop_series.to_csv(
        os.path.join(time_series_directory, "cops_heat_pump.csv"),
        index=False,
        header=True,
    )

    return cop_series


# cops_chiller = cmpr_hp_chiller.calc_cops(t_high=data_t_high_list,
#                          t_low=data_t_low_list,
#                          quality_grade=0.25,
#                          mode="chiller")


if __name__ == "__main__":
    weather = pd.read_csv("./data/inputs/weatherdata.csv").set_index("time")

    cops = calculate_cops_heat_pump(weather=weather)
    print(cops)
    print(f"Min: {round(min(cops), 2)}, Max: {round(max(cops), 2)}")
