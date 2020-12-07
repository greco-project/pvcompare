"""
This module contains the precalculations of the stratified thermal storage

It calculates:

    - The nominal storage capacity
    - The loss rate and
    - Fixed losses

using functions implemented in oemof.thermal (github.com/oemof/oemof-thermal)
"""

import pandas as pd
import numpy as np
import os
import logging
import maya
import oemof.thermal.stratified_thermal_storage as strat_tes

# internal imports
from pvcompare import constants


def calc_strat_tes_param(
    weather,
    lat,
    lon,
    temperature_col="temp_air",
    input_directory=None,
    mvs_input_directory=None,
):
    """

    Parameters
    ----------
    weather : :pandas:`pandas.DataFrame<frame>`
        Contains weather data time series. Required: ambient temperature in
        column `temperature_col`.
    temperature_col : str
        Name of column in `weather` containing ambient temperature.
        Default: "temp_air".
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
        DEFAULT_MVS_OUTPUT_DIRECTORY (see :func:`~pvcompare.constants`.

    Returns
    -------
    u_value : numeric
        Thermal transmittance (U-value) [W/(m2*K)]

    volume : numeric
        Volume of storage

    surface : numeric
        Total surface of storage [m2]

    nominal_storage_capacity : numeric
        Maximum amount of stored thermal energy [MWh]

    loss_rate : numeric (sequence or scalar)
        The relative loss of the storage capacity between two consecutive
        timesteps [-]

    fixed_losses_relative : numeric (sequence or scalar)
        Losses independent of state of charge between two consecutive
        timesteps relative to nominal storage capacity [-]

    fixed_losses_absolute : numeric (sequence or scalar)
        Losses independent of state of charge and independent of
        nominal storage capacity between two consecutive timesteps [MWh]

    """
    # *********************************************************************************************
    # Set paths - Read and prepare data
    # *********************************************************************************************
    if input_directory is None:
        input_directory = constants.DEFAULT_INPUT_DIRECTORY

    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

    time_series_directory = os.path.join(mvs_input_directory, "time_series")

    input_data_filename = os.path.join(
        input_directory, "stratified_thermal_storage.csv"
    )
    input_data = pd.read_csv(input_data_filename, header=0, index_col=0)["var_value"]

    # Prepare ambient temperature for precalculations
    ambient_temperature = weather[temperature_col]

    # Create add on to filename (year, lat, lon)
    year = maya.parse(weather.index[int(len(weather) / 2)]).datetime().year
    add_on = f"_{year}_{lat}_{lon}"

    # *********************************************************************************************
    # Precalculations
    # *********************************************************************************************

    u_value = strat_tes.calculate_storage_u_value(
        input_data["s_iso"],
        input_data["lamb_iso"],
        input_data["alpha_inside"],
        input_data["alpha_outside"],
    )

    volume, surface = strat_tes.calculate_storage_dimensions(
        input_data["height"], input_data["diameter"]
    )

    nominal_storage_capacity = (
        strat_tes.calculate_capacities(
            volume, input_data["temp_h"], input_data["temp_c"]
        )
        * 1000
    )

    (
        loss_rate,
        fixed_losses_relative,
        fixed_losses_absolute,
    ) = strat_tes.calculate_losses(
        u_value,
        input_data["diameter"],
        input_data["temp_h"],  # TODO: In future heat pump temp here
        input_data["temp_c"],  # TODO: In future relation to temp_h here
        ambient_temperature,
    )

    unit = ["no_unit", "kWh"]
    results = {
        "fixed losses relative": fixed_losses_relative,
        "fixed losses absolute": fixed_losses_absolute,
    }

    for name, result in results.items():
        # Get number of iteration
        result_index = list(results.keys()).index(name)

        # Prepare value name for csv saving
        value_name_underscore = name.replace(" ", "_")

        # Set file name
        filename = f"{value_name_underscore}_{add_on}.csv"

        # Set unit as new name of result in result list
        result.name = unit[result_index]

        # Save results to csv
        result.to_csv(
            os.path.join(time_series_directory, filename), index=False, header=True
        )
        logging.info(
            f"The time dependent {name} of a stratified thermal storage is calculated and saved under {time_series_directory}."
        )

    return (
        nominal_storage_capacity,
        loss_rate,
        fixed_losses_relative,
        fixed_losses_absolute,
    )


def add_strat_tes(
    weather, lat, lon, storage_csv, input_directory=None, mvs_input_directory=None
):
    """
    Adds stratified thermal storage if it exists either in 'energyStorage.csv' or in
    'energyConversion.csv'.

    The precalculations are done if `inflow_direction` and `outflow_direction` give a hint
    that the respective asset is a heat storage (inflow_direction: "Heat",
    outflow_direction: "Heat").

    Parameters
    ----------
    weather : :pandas:`pandas.DataFrame<frame>`
        DataFrame with time series for temperature in column 'temp_air' in °C.
    lat : float
        Latitude of ambient temperature location in `weather`.
    lon : float
        Longitude of ambient temperature location in `weather`.
    storage_csv : str
        Name of the storage specific file
    input_directory: str or None
        Path to input directory of pvcompare containing file
        `stratified_thermal_storage.csv` that specifies stratified thermal storage
        data. Default: DEFAULT_INPUT_DIRECTORY (see :func:`~pvcompare.constants`.
    mvs_input_directory: str or None
        Path to input directory containing files that describe the energy
        system and that are an input to MVS. Default:
        DEFAULT_MVS_OUTPUT_DIRECTORY (see :func:`~pvcompare.constants`).

    Notes
    -----
    You can include a stratified thermal storage in the model using two ways:

    1. With storage component with `inflow_direction` and `outflow_direction` to the heat bus
    2. With a storage bus, a storage component and `inflow_direction` and `outflow_direction`
        as Transformer feeding in and from that bus
        Please note that the cost parameters of `inflow_direction` and `outflow_direction` of the
        Transformer should be set to zero, since they cannot be assigned to a real plant
        component with cost parameters

    Returns
    -------
    Depending on the case, updates energyStorage.csv and saves calculated values to
    'data/mvs_inputs/time_series'.

    """
    # *********************************************************************************************
    # Set path if path is None
    # *********************************************************************************************
    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

    # *********************************************************************************************
    # Read files
    # *********************************************************************************************
    # 1. Read energyStorage.csv
    energy_storage = pd.read_csv(
        os.path.join(mvs_input_directory, "csv_elements", "energyStorage.csv"),
        header=0,
        index_col=0,
    )
    # 2. Read energyConversion.csv
    energy_conversion = pd.read_csv(
        os.path.join(mvs_input_directory, "csv_elements", "energyConversion.csv"),
        header=0,
        index_col=0,
    )

    # 3. Read storage_xx.csv from input value
    storage_xx = pd.read_csv(
        os.path.join(mvs_input_directory, "csv_elements", storage_csv),
        header=0,
        index_col=0,
    )

    # *********************************************************************************************
    # Check if stratified thermal storage exists in specified system and is implemented in
    # either one of the two or both options of implementing (see notes)
    # *********************************************************************************************
    stratified_thermal_storages = []
    inflow_tes = None
    outflow_tes = None
    # Option 1: With in- and outflow direction feeding in and from heat bus
    for col in energy_storage.keys():
        outflow = energy_storage[col]["outflow_direction"]
        inflow = energy_storage[col]["inflow_direction"]
        if outflow == "Heat" and inflow == "Heat":
            stratified_thermal_storages.extend([col])

    # Option 2: Storage bus with in- and outflow direction as transformer
    for col in energy_conversion.keys():
        outflow = energy_conversion[col]["outflow_direction"]
        inflow = energy_conversion[col]["inflow_direction"]
        if inflow == "Heat":
            outflow_tes = outflow
        elif outflow == "Heat" and inflow != "Electricity":
            inflow_tes = inflow

    if inflow_tes is not None and inflow_tes == outflow_tes:
        stratified_thermal_storages.extend([inflow_tes])

    # *********************************************************************************************
    # Check if time dependent data exists. Else calculate time series
    # *********************************************************************************************
    file_exists = True
    # Put all the time dependent values in a list
    time_dependent_value = ["rel_losses", "abs_losses"]
    # Explaining name of that value
    value_name = ["fixed losses relative", "fixed losses absolute"]

    for time_value in time_dependent_value:
        time_value_index = time_dependent_value.index(time_value)
        value_name_underscore = value_name[time_value_index].replace(" ", "_")
        for stratified_thermal_storage in stratified_thermal_storages:
            value = storage_xx["storage capacity"][time_value]
            try:
                float(value)
                logging.info(
                    f"Stratified thermal storage in column 'storage capacity' of '{storage_csv}' has "
                    + f"constant {value_name[time_value_index]} {value}. For using temperature dependent values check the documentation."
                )
            except ValueError:
                # check if result file exists
                filename_csv_excl_path = value.split("'")[3]
                filename_csv = os.path.join(
                    mvs_input_directory, "time_series", filename_csv_excl_path
                )

                if not os.path.isfile(filename_csv):
                    year = weather.index[int(len(weather) / 2)].year
                    result_filename = os.path.join(
                        mvs_input_directory,
                        "time_series",
                        f"{value_name_underscore}_{year}_{lat}_{lon}.csv",
                    )
                    logging.info(
                        f"File containing {value_name} is missing: {filename_csv} \nCalculated times series of {value_name} are used instead."
                    )
                    file_exists = False
                    # write new filename into storage_xx
                    storage_xx["storage capacity"][time_value] = storage_xx[
                        "storage capacity"
                    ][time_value].replace(
                        filename_csv_excl_path,
                        f"{value_name_underscore}_{year}_{lat}_{lon}.csv",
                    )

                if file_exists == False:
                    # update storage_xx.csv
                    storage_xx.to_csv(
                        os.path.join(
                            mvs_input_directory, "csv_elements", f"{storage_csv}"
                        )
                    )
                    # calculate results of stratified thermal storage for location if not existent
                    if not os.path.isfile(result_filename):
                        calc_strat_tes_param(
                            weather=weather,
                            lat=lat,
                            lon=lon,
                            mvs_input_directory=mvs_input_directory,
                            input_directory=input_directory,
                        )
                        logging.info(
                            f"Times series of {value_name} successfully calculated and saved in 'data/mvs_inputs/time_series'."
                        )

                # display warning if heat demand seems not to be in energyConsumption.csv
                energy_consumption = pd.read_csv(
                    os.path.join(
                        mvs_input_directory, "csv_elements", "energyConsumption.csv"
                    ),
                    header=0,
                    index_col=0,
                )
                if (
                    not "Heat" in energy_consumption.loc["inflow_direction"].values
                    and not "heat" in energy_consumption.loc["inflow_direction"].values
                ):
                    logging.warning(
                        "Heat demand might be missing in 'energyConsumption.csv' as non of the "
                        + "assets' inflow direction is named 'Heat' nor 'heat'."
                    )


def run_stratified_thermal_storage():
    """
    This function executes calc_strat_tes_param(input_data)
    with self selected input data series
    """
    # Set paths to inputs
    inputs_path = "./data/inputs/"

    # Choose weather data to examine
    weather_data = "weatherdata_52.52437_13.41053_2014.csv"
    weather = pd.read_csv(os.path.join(inputs_path, weather_data)).set_index("time")

    (
        nominal_storage_capacity,
        loss_rate,
        fixed_losses_relative,
        fixed_losses_absolute,
    ) = calc_strat_tes_param(
        weather=weather,
        lat=53.2,
        lon=13.2,
        temperature_col="temp_air",
        mvs_input_directory="./data/mvs_inputs_template_sector_coupling/",
    )

    parameter = {
        "Nominal storage capacity [kWh]": nominal_storage_capacity,
        "Loss rate [-]": loss_rate,
        "Fixed relative losses [-]": fixed_losses_relative,
        "Fixed absolute losses [kWh]": fixed_losses_absolute,
    }

    dash = "-" * 50

    print(dash)
    print("Results")
    print(dash)

    for name, param in parameter.items():
        print(name)
        print(param)
        print(dash)


if __name__ == "__main__":
    run_stratified_thermal_storage()
