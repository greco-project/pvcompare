"""
This module contains the precalculations of the stratified thermal storage

It calculates:

    - The nominal storage capacity
    - The loss rate
    - Fixed losses relative and
    - Fixed losses absolute

using functions implemented in oemof.thermal (github.com/oemof/oemof-thermal)
"""

import pandas as pd
import os
import logging
import maya
import oemof.thermal.stratified_thermal_storage as strat_tes

# internal imports
from pvcompare import constants
from pvcompare import check_inputs


def calc_strat_tes_param(
    weather,
    temperature_col="temp_air",
    user_inputs_pvcompare_directory=None,
    user_inputs_mvs_directory=None,
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
    user_inputs_pvcompare_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used as user_inputs_pvcompare_directory.
        Default: None.
    user_inputs_mvs_directory: str or None
        Path to input directory containing files that describe the energy
        system and that are an input to MVS. Default:
        DEFAULT_MVS_OUTPUT_DIRECTORY (see :func:`~pvcompare.constants`.

    Returns
    -------
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
    if user_inputs_pvcompare_directory is None:
        input_directory = constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY

    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY

    input_data_filename = os.path.join(
        user_inputs_pvcompare_directory, "stratified_thermal_storage.csv"
    )
    input_data = pd.read_csv(input_data_filename, header=0, index_col=0)["var_value"]

    # Prepare ambient temperature for precalculations
    ambient_temperature = weather[temperature_col]

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

    return (
        nominal_storage_capacity,
        loss_rate,
        fixed_losses_relative,
        fixed_losses_absolute,
    )


def save_time_dependent_values(
    losses, value_name, unit, filename, time_series_directory
):
    # Make dictionary before saving data with unit as label
    losses_dict = {unit: losses}

    # Save results to csv
    for name, value in losses_dict.items():
        # Set unit as new name of result in result list
        value.name = unit

        # Save value to csv
        value.to_csv(
            os.path.join(time_series_directory, filename), index=False, header=True
        )
    logging.info(
        f"The time dependent {value_name} of a stratified thermal storage is saved under {time_series_directory}."
    )


def add_strat_tes(
    weather,
    lat,
    lon,
    user_inputs_pvcompare_directory=None,
    user_inputs_mvs_directory=None,
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
    user_inputs_pvcompare_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used as user_inputs_pvcompare_directory.
        Default: None.
    user_inputs_mvs_directory: str or None
        Path to input directory containing files that describe the energy
        system and that are an input to MVS. Default:
        DEFAULT_MVS_OUTPUT_DIRECTORY (see :func:`~pvcompare.constants`.

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
    # Set paths
    # *********************************************************************************************
    # Set path if path is None
    if user_inputs_pvcompare_directory == None:
        user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY

    # Set path for results in time series
    time_series_directory = os.path.join(user_inputs_mvs_directory, "time_series")

    # *********************************************************************************************
    # Read files
    # *********************************************************************************************
    # 1. Read energyStorage.csv
    energy_storage = pd.read_csv(
        os.path.join(user_inputs_mvs_directory, "csv_elements", "energyStorage.csv"),
        header=0,
        index_col=0,
    )
    # 2. Read energyConversion.csv
    energy_conversion = pd.read_csv(
        os.path.join(user_inputs_mvs_directory, "csv_elements", "energyConversion.csv"),
        header=0,
        index_col=0,
    )

    # 3. Read energyBusses.csv
    energy_busses = pd.read_csv(
        os.path.join(user_inputs_mvs_directory, "csv_elements", "energyBusses.csv"),
        header=0,
        index_col=0,
    )

    # 3. Read storage_xx.csv from input value
    storage_xx = pd.read_csv(
        os.path.join(user_inputs_mvs_directory, "csv_elements", storage_csv),
        header=0,
        index_col=0,
    )

    # 4. Read stratified_thermal_storage.csv
    storage_input_data = pd.read_csv(
        os.path.join(user_inputs_pvcompare_directory, "stratified_thermal_storage.csv"),
        header=0,
        index_col=0,
    )

    # Create add on to filename (year, lat, lon, temp_high)
    year = maya.parse(weather.index[int(len(weather) / 2)]).datetime().year
    temp_high = storage_input_data.at["temp_h", "var_value"]
    add_on = f"_{year}_{lat}_{lon}_{temp_high}"

    # *********************************************************************************************
    # Check if stratified thermal storage exists in specified system
    # *********************************************************************************************
    stratified_thermal_storages = []

    for bus in energy_busses.keys():
        if energy_busses[bus]["energyVector"] == "Heat":
            heat_bus = bus
            for col in energy_storage.keys():
                outflow = energy_storage[col]["outflow_direction"]
                inflow = energy_storage[col]["inflow_direction"]
                if outflow == heat_bus and inflow == heat_bus:
                    stratified_thermal_storages.extend([col])

    # *********************************************************************************************
    # Do precalculations for the stratified thermal storage
    # *********************************************************************************************
    (
        nominal_storage_capacity,
        loss_rate,
        fixed_losses_relative,
        fixed_losses_absolute,
    ) = calc_strat_tes_param(
        weather=weather,
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
    )
    logging.info(f"Stratified thermal storage successfully precalculated.")

    # Save calculated nominal storage capacity and loss rate to storage_xx.csv
    storage_csv = energy_storage.at["storage_filename", col]

    check_inputs.add_parameters_to_storage_xx_file(
        nominal_storage_capacity=nominal_storage_capacity,
        loss_rate=loss_rate,
        storage_csv=storage_csv,
        user_inputs_mvs_directory=user_inputs_mvs_directory,
    )
    # 3. Replace old storage_xx.csv with new one that contains calculated values
    storage_xx = pd.read_csv(
        os.path.join(user_inputs_mvs_directory, "csv_elements", storage_csv),
        header=0,
        index_col=0,
    )

    # *********************************************************************************************
    # Check if time dependent data exists. Else save above calculated time series
    # *********************************************************************************************
    file_exists = True
    # Put all the time dependent values in a list
    time_dependent_value = [
        "fixed_thermal_losses_relative",
        "fixed_thermal_losses_absolute",
    ]
    # Units of the time dependent values
    unit = ["no_unit", "kWh"]
    # Explaining name of that value
    value_name = ["fixed thermal losses relative", "fixed thermal losses absolute"]
    # Values from precalculation
    parameter = [fixed_losses_relative, fixed_losses_absolute]

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
                    user_inputs_mvs_directory, "time_series", filename_csv_excl_path
                )

                if not os.path.isfile(filename_csv):
                    year = weather.index[int(len(weather) / 2)].year
                    result_filename = os.path.join(
                        user_inputs_mvs_directory,
                        "time_series",
                        f"{value_name_underscore}_{year}_{lat}_{lon}_{temp_high}.csv",
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
                        f"{value_name_underscore}_{year}_{lat}_{lon}_{temp_high}.csv",
                    )

                if file_exists == False:
                    # update storage_xx.csv
                    storage_xx.to_csv(
                        os.path.join(
                            user_inputs_mvs_directory, "csv_elements", f"{storage_csv}"
                        )
                    )
                    # Write results of time dependent values if non existent
                    if not os.path.isfile(result_filename):
                        save_time_dependent_values(
                            parameter[time_value_index],
                            value_name_underscore,
                            unit[time_value_index],
                            result_filename,
                            time_series_directory,
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
        temperature_col="temp_air",
        user_inputs_mvs_directory="./data/mvs_inputs_template_sector_coupling/",
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
