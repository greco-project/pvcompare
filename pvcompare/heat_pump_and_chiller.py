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


def calculate_cops_and_eers(
    weather,
    lat,
    lon,
    temperature_col="temp_air",
    mode="heat_pump",
    input_directory=None,
    mvs_input_directory=None,
):
    r"""
    Calculates the COPs of a heat pump or EERs of a chiller depending on `mode`.

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
    lat : float
        Latitude of ambient temperature location in `weather`.
    lon : float
        Longitude of ambient temperature location in `weather`.
    temperature_col : str
        Name of column in `weather` containing ambient temperature.
        Default: "temp_air".
    mode : str
        Defines whether COPs ot heat pump ("heat_pump") or EERs of chiller
        ("chiller") are calculated. Default: "heat_pump".
    input_directory: str or None
        Path to input directory of pvcompare containing file
        `heat_pump_and_chillers.csv` that specifies heat pump and/or chiller
        data. Default: DEFAULT_INPUT_DIRECTORY (see :func:`~pvcompare.constants`.
    mvs_input_directory: str or None
        Path to input directory containing files that describe the energy
        system and that are an input to MVS. Default:
        DEFAULT_MVS_OUTPUT_DIRECTORY (see :func:`~pvcompare.constants`.

    Returns
    -------
    efficiency_series : :pandas:`pandas.Series<series>`
        COP or EER time series of heat pump or chiller depending on `mode`.

    """
    # read parameters from file
    if input_directory is None:
        input_directory = constants.DEFAULT_INPUT_DIRECTORY
    filename = os.path.join(input_directory, "heat_pump_and_chillers.csv")
    parameters = pd.read_csv(filename, header=0, index_col=0).loc[mode]

    # prepare parameters for calc_cops
    start_temperature = float(parameters.start_temperature)
    room_temperature = [float(parameters.room_temperature)]
    quality_grade = float(parameters.quality_grade)

    # prepare ambient temperature for calc_cops (list)
    ambient_temperature = weather[temperature_col].values.tolist()

    # create add on to filename (year, lat, lon)
    year = weather.index[int(len(weather) / 2)].year
    add_on = f"_{year}_{lat}_{lon}"

    # calculate COPs or EERs with oemof thermal
    if mode == "heat_pump":
        # additional parameters for heat_pump mode
        factor_icing = (
            None
            if parameters.factor_icing == "None"
            else float(parameters.factor_icing)
        )
        temp_threshold_icing = (
            None
            if parameters.temp_threshold_icing == "None"
            else float(parameters.temp_threshold_icing)
        )

        efficiency = cmpr_hp_chiller.calc_cops(
            temp_high=room_temperature,
            temp_low=ambient_temperature,
            quality_grade=quality_grade,
            mode=mode,
            temp_threshold_icing=temp_threshold_icing,
            factor_icing=factor_icing,
        )

        # define variables for later proceeding
        column_name = "cop"
        filename = f"cops_heat_pump{add_on}.csv"

    elif mode == "chiller":
        efficiency = cmpr_hp_chiller.calc_cops(
            temp_high=ambient_temperature,
            temp_low=room_temperature,
            quality_grade=quality_grade,
            mode=mode,
        )
        column_name = "eer"
        filename = f"eers_chiller{add_on}.csv"

    else:
        raise ValueError(
            f"Parameter `mode` should be 'heat_pump' or 'chiller' but is {mode}"
        )

    # add list of cops/eers to data frame
    df = pd.DataFrame(weather[temperature_col])
    df[column_name] = efficiency

    # set COP to nan where ambient temperature > heating period temperature
    # or respectively set EER to nan where ambient temperature < cooling
    # period temperature
    if mode == "heat_pump":
        indices = df.loc[df[temperature_col] > start_temperature].index
    else:
        indices = df.loc[df[temperature_col] < start_temperature].index
    df[column_name][indices] = np.nan

    # extract COPs/EERs as pd.Series from data frame
    efficiency_series = df[column_name]
    efficiency_series.name = "no_unit"

    # save time series to mvs input directory / timeseries
    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    time_series_directory = os.path.join(mvs_input_directory, "time_series")

    logging.info(
        f"The cops of a heat pump are calculated and saved under {time_series_directory}."
    )

    efficiency_series.to_csv(
        os.path.join(time_series_directory, filename),
        index=False,
        header=True,
    )

    return efficiency_series

def add_sector_coupling():
    """
    Add heat sector if heat pump in `energyConversion.csv`.
    """
    pass


if __name__ == "__main__":
    weather = pd.read_csv("./data/inputs/weatherdata.csv").set_index("time")

    cops = calculate_cops_and_eers(weather=weather, mode="heat_pump")
    print(cops)
    print(f"Min: {round(min(cops), 2)}, Max: {round(max(cops), 2)}")
