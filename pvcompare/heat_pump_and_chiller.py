"""
This module contains functions for calculating temperature dependent
coefficient of performance (COP) of heat pumps and energy efficiency ratios
(EER) of chillers.

"""

import pandas as pd
import numpy as np
import os
import logging
import maya

import oemof.thermal.compression_heatpumps_and_chillers as cmpr_hp_chiller

# internal imports
from pvcompare import constants


def calculate_cops_and_eers(
    weather,
    lat,
    lon,
    mode,
    temperature_col="temp_air",
    input_directory=None,
    mvs_input_directory=None,
):
    r"""
    Calculates the COPs of a heat pump or EERs of a chiller depending on `mode`.

    Temperature dependency is taken into consideration.
    For these calculations the oemof.thermal `calc_cops()` functionality is
    used. Data like quality grade and factor icing is read from the file
    `heat_pumps_and_chillers.csv` in the `input_directory`.
    Negative values, which might occur due to high ambient temperatures in summer are
    set to zero.

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
        Defines whether COPs of heat pump ("heat_pump") or EERs of chiller
        ("chiller") are calculated. Default: "heat_pump".
    input_directory: str or None
        Path to input directory of pvcompare containing file
        `heat_pumps_and_chillers.csv` that specifies heat pump and/or chiller
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
    filename = os.path.join(input_directory, "heat_pumps_and_chillers.csv")

    try:
        parameters = pd.read_csv(filename, header=0, index_col=0).loc[mode]
    except KeyError:
        raise ValueError(
            f"Parameter `mode` should be 'heat_pump' or 'chiller' but is {mode}"
        )
    # prepare parameters for calc_cops
    low_temperature = float(parameters.temp_low)
    high_temp = float(parameters.temp_high)
    high_temperature = [float(parameters.temp_high)]
    quality_grade = float(parameters.quality_grade)

    # prepare ambient temperature for calc_cops (list)
    ambient_temperature = weather[temperature_col].values.tolist()

    # create add on to filename (year, lat, lon)
    year = maya.parse(weather.index[int(len(weather) / 2)]).datetime().year
    add_on = f"_{year}_{lat}_{lon}_{high_temp}"

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
            temp_high=high_temperature,
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
            temp_low=low_temperature,
            quality_grade=quality_grade,
            mode=mode,
        )
        column_name = "eer"
        filename = f"eers_chiller{add_on}.csv"

    # add list of cops/eers to data frame
    df = pd.DataFrame(weather[temperature_col])
    df[column_name] = efficiency

    # set negative COPs/EERs to np.inf
    # COP/EER below zero results from temp_low > temp_high
    # and will therefore be represented with COP/EER -> infinity
    indices = df.loc[df[column_name] < 0].index
    df[column_name][indices] = np.inf

    # extract COPs/EERs as pd.Series from data frame
    efficiency_series = df[column_name]
    efficiency_series.name = "no_unit"

    # save time series to `mvs_input_directory/time_series`
    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    time_series_directory = os.path.join(mvs_input_directory, "time_series")

    logging.info(
        f"The cops of a heat pump are calculated and saved under {time_series_directory}."
    )

    efficiency_series.to_csv(
        os.path.join(time_series_directory, filename), index=False, header=True
    )

    return efficiency_series


def add_sector_coupling(
    weather, lat, lon, input_directory=None, mvs_input_directory=None
):
    """
    Add heat sector if heat pump or chiller in 'energyConversion.csv'.

    COPs or EERS are calculated automatically as long as the parameters
    `inflow_direction` and `outflow_direction` give a hint that the respective asset is
    a heat pump (inflow_direction: "Electricity", outflow_direction: "Heat") or chiller
    (Not implemented, yet.).

    Parameters
    ----------
    weather : :pandas:`pandas.DataFrame<frame>`
        DataFrame with time series for temperature in column 'temp_air' in °C.
    lat : float
        Latitude of ambient temperature location in `weather`.
    lon : float
        Longitude of ambient temperature location in `weather`.
    input_directory: str or None
        Path to input directory of pvcompare containing file
        `heat_pumps_and_chillers.csv` that specifies heat pump and/or chiller
        data. Default: DEFAULT_INPUT_DIRECTORY (see :func:`~pvcompare.constants`.
    mvs_input_directory: str or None
        Path to input directory containing files that describe the energy
        system and that are an input to MVS. Default:
        DEFAULT_MVS_OUTPUT_DIRECTORY (see :func:`~pvcompare.constants`).

    Notes
    -----
    Chillers were not tested, yet, and no automatic calculation of EERs is implemented.
    Attention: the above mentioned characteristics (inflow_direction: "Electricity",
    outflow_direction: "Heat") could also account for other heating elements. This
    function could be enhanced.

    Returns
    -------
    Depending on the case, updates energyConversion.csv and saves calculated cops to
    'data/mvs_inputs/time_series'.

    """
    # read energyConversion.csv file
    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    if input_directory is None:
        input_directory = constants.DEFAULT_INPUT_DIRECTORY
    energy_conversion = pd.read_csv(
        os.path.join(mvs_input_directory, "csv_elements", "energyConversion.csv"),
        header=0,
        index_col=0,
    )
    heat_pump_and_chillers = pd.read_csv(
        os.path.join(input_directory, "heat_pumps_and_chillers.csv"),
        header=0,
        index_col=0,
    )

    # Check if heat pump exists in specified system (energy vector is "Heat", inflow
    # direction includes "Electricity" or "electricity")
    heat_pumps = []
    for col in energy_conversion.keys():
        energy_vector = energy_conversion[col]["energyVector"]
        inflow = energy_conversion[col]["inflow_direction"]
        if "Heat" in energy_vector and (
            "Electricity" in inflow or "electricity" in inflow
        ):
            heat_pumps.extend([col])

    file_exists = True
    for heat_pump in heat_pumps:
        eff = energy_conversion[heat_pump]["efficiency"]
        try:
            float(eff)
            logging.info(
                f"Heat pump in column '{heat_pump}' of 'energyConversion.csv' has "
                + f"constant efficiency {eff}. For using temperature dependent COPs check the documentation."
            )
        except ValueError:
            # check if COPs file provided in efficiency exists
            cops_filename_csv_excl_path = eff.split("'")[3]
            cops_filename_csv = os.path.join(
                mvs_input_directory, "time_series", cops_filename_csv_excl_path
            )

            if not os.path.isfile(cops_filename_csv):
                high_temperature = heat_pump_and_chillers.at["heat_pump", "temp_high"]
                year = weather.index[int(len(weather) / 2)].year
                cops_filename = os.path.join(
                    mvs_input_directory,
                    "time_series",
                    f"cops_heat_pump_{year}_{lat}_{lon}_{high_temperature}.csv",
                )
                logging.info(
                    f"File containing COPs is missing: {cops_filename_csv} \nCalculated COPs are used instead."
                )
                file_exists = False
                # write new filename into energy_conversion
                energy_conversion[heat_pump]["efficiency"] = energy_conversion[
                    heat_pump
                ]["efficiency"].replace(
                    cops_filename_csv_excl_path,
                    f"cops_heat_pump_{year}_{lat}_{lon}_{high_temperature}.csv",
                )

        if file_exists == False:
            # update energyConversion.csv
            energy_conversion.to_csv(
                os.path.join(
                    mvs_input_directory, "csv_elements", "energyConversion.csv"
                )
            )
            # calculate COPs of heat pump for location if not existent
            if not os.path.isfile(cops_filename):
                calculate_cops_and_eers(
                    weather=weather,
                    mode="heat_pump",
                    lat=lat,
                    lon=lon,
                    mvs_input_directory=mvs_input_directory,
                    input_directory=input_directory,
                )
                logging.info(
                    "COPs successfully calculated and saved in `mvs_input_directory/time_series`."
                )

        # display warning if heat demand seems to be missing in energyConsumption.csv
        energy_consumption = pd.read_csv(
            os.path.join(mvs_input_directory, "csv_elements", "energyConsumption.csv"),
            header=0,
            index_col=0,
        )
        if (
            not "Heat" in energy_consumption.loc["inflow_direction"].values
            and not "heat" in energy_consumption.loc["inflow_direction"].values
        ):
            logging.warning(
                "Heat demand might be missing in `energyConsumption.csv` as none of "
                + "the assets' inflow direction is named 'Heat' nor 'heat'."
            )

    # chiller
    if "chiller" in [key.split("_")[0] for key in energy_conversion.keys()]:
        logging.warning(
            "Chillers were not tested, yet. Make sure to provide a cooling demand in "
            + "'energyConsumption.csv' and a constant EER or to place a file "
            + "containing EERs into `data/mvs_inputs/time_series` directory."
        )
    return None


if __name__ == "__main__":
    weather = pd.read_csv("./data/inputs/weatherdata.csv").set_index("time")

    cops = calculate_cops_and_eers(
        weather=weather, mode="heat_pump", lat=53.2, lon=13.2
    )
    print(cops)
    print(f"Min: {round(min(cops), 2)}, Max: {round(max(cops), 2)}")
