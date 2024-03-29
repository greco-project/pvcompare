"""
This module contains functions for calculating temperature dependent
coefficient of performance (COP) of heat pumps and energy efficiency ratios
(EER) of chillers.

"""

import pandas as pd
import os
import logging
import maya
import numpy as np

import oemof.thermal.compression_heatpumps_and_chillers as cmpr_hp_chiller

# internal imports
from pvcompare import constants


def calculate_cops_and_eers(
    weather,
    lat,
    lon,
    mode,
    temperature_col="temp_air",
    user_inputs_pvcompare_directory=None,
    user_inputs_mvs_directory=None,
):
    r"""
    Calculates the COPs of a heat pump or EERs of a chiller depending on `mode`.

    Temperature dependency is taken into consideration.
    For these calculations the ``calc_cops()` <functionality>`_ functionality of
    `oemof.thermal <https://oemof-thermal.readthedocs.io/en/stable/>`_  is
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
    user_inputs_pvcompare_directory: str or None
        Path to user input directory. If None,
        `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used.
        Default: None.
    user_inputs_mvs_directory: str or None
        Path to input directory containing files that describe the energy
        system and that are an input to MVS. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used.
        Default: None.

    Returns
    -------
    None
    """

    # read parameters from file
    if user_inputs_pvcompare_directory == None:
        user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    filename = os.path.join(
        user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"
    )

    try:
        parameters_complete = pd.read_csv(filename)
        parameters = pd.read_csv(filename, header=0, index_col=0).loc[mode]
    except KeyError:
        raise ValueError(
            f"Parameter `mode` should be 'heat_pump' or 'chiller' but is {mode}"
        )
    # prepare parameters for calc_cops

    def process_temperatures(temperature, level, mode, technology):
        r"""
        Processes temperatures for specific `level`, `mode`, and `technology`.

        `temperature` can be passed in the following way:
        1. As NaN - The lower/higher temperature of the heat pump/chiller equals the ambient temperature time series
        2. As single value (float or int) - The temperature is constant
        3. As time series - The temperature is not constant or differs from ambient temperature (eg. ground source)

        Parameters
        ----------
        temperature : float, int, np.nan, :pandas:`pandas.Series<series>
            Passed temperature which was written from input data.
        level : str
            Defines whether high or low temperature has been passed.
        mode : str
            Defines whether COPs of heat pump ("heat_pump") or EERs of chiller
            ("chiller") are calculated.
        technology: str
            Defines whether technology is a "brine-water", "air-air"
            or "air-water".

        Returns
        -------
        temperature: list
            Temperature adjusted to use case of plant.
        """

        if isinstance(temperature, float):
            if pd.isna(temperature):
                # In case of NaN
                if (level == "low" and mode == "heat_pump") or (
                    level == "high" and mode == "chiller"
                ):
                    if technology == "brine-water":
                        # Prepare mean yearly ambient temperature for calc_cops (numeric)
                        temperature = np.average(weather[temperature_col].values)
                        temperature = [temperature]
                    elif technology == "air-air" or technology == "air-water":
                        # Prepare ambient temperature for calc_cops (list)
                        temperature = weather[temperature_col].values.tolist()
                        logging.info(
                            f"The {mode} is modeled with the ambient temperature from weather data as {level} temperature."
                        )
                    else:
                        # Prepare ambient temperature for calc_cops (list)
                        temperature = weather[temperature_col].values.tolist()
                        logging.warning(
                            f"The technology of the {mode} should be either 'air-air', 'air-water' or 'brine-water'."
                            f"'{technology}' is not a valid technology. The {mode} is modeled as an air source {mode} by default"
                            f" and with the ambient temperature from weather data as {level} temperature."
                        )
                    return temperature
                else:
                    # Required parameter is missing
                    raise ValueError(
                        f"Missing required value of {mode}: Please provide a numeric as {mode}'s {level} temperature in heat_pumps_and_chillers.csv."
                    )
            elif isinstance(temperature, (float, int)):
                # Numerics pass
                temperature = [temperature]
                logging.info(
                    f"The {mode} is modeled with the constant {level} temperature of {temperature} °C"
                )
                return temperature
        elif isinstance(temperature, str):
            # In case temperatures are provided as time series in separate file
            try:
                temp_string = temperature.split("'")
                temp_filename = temp_string[3]
                temp_header = temp_string[7]
                temperature_df = pd.read_csv(
                    os.path.join(user_inputs_pvcompare_directory, temp_filename)
                )
                temperature_df = temperature_df.set_index(temp_header)
                temperature = temperature_df.index.tolist()
                logging.info(
                    f"The {mode} is modeled with passed time series as {level} temperature."
                )
                return temperature

            except AttributeError:
                raise ValueError(
                    f"Wrong value: Please check the {level} temperature of the {mode}. See the documentation on passing the {mode}'s temperatures for further information"
                )
        else:
            # Required parameter is missing in case of None or else
            raise ValueError(
                f"Missing required value of {mode}: Please provide a numeric as {mode}'s {level} temperature in heat_pumps_and_chillers.csv."
            )

    low_temperature = process_temperatures(
        parameters.temp_low, "low", mode, parameters.technology
    )
    high_temperature = process_temperatures(
        parameters.temp_high, "high", mode, parameters.technology
    )

    if pd.isna(parameters.quality_grade):
        if parameters.technology == "air-air":
            if mode == "heat_pump":
                quality_grade = 0.1852
            elif mode == "chiller":
                quality_grade = 0.3
        elif parameters.technology == "air-water":
            if mode == "heat_pump":
                quality_grade = 0.403
            elif mode == "chiller":
                # Required parameter is missing in case of None or else
                raise ValueError(
                    f"Missing required value of {mode}: There is no default value of a quality grade provided for an {parameters.technology} {mode}"
                    f"Please provide a valid value of the quality grade."
                )
        elif parameters.technology == "brine-water":
            if mode == "heat_pump":
                quality_grade = 0.53
            elif mode == "chiller":
                # Required parameter is missing in case of None or else
                raise ValueError(
                    f"Missing required value of {mode}: There is no default value of a quality grade provided for a {parameters.technology} {mode}. "
                    f"Please provide a valid value of the quality grade."
                )
        else:
            # Required parameter is missing in case of different technology
            raise ValueError(
                f"Missing required value of {mode}: '{parameters.quality_grade}' could not be processed as quality grade. "
                f"Please provide a valid value or the technology of the {mode} in order to model with default quality grade."
            )
    elif isinstance(parameters.quality_grade, (float, int)):
        quality_grade = float(parameters.quality_grade)
    else:
        # Required parameter is missing in case of None or else
        raise ValueError(
            f"Missing required value of {mode}: '{parameters.quality_grade}' could not be processed as quality grade."
            f"Please provide a valid value or the technology of the {mode} in order to model from default quality grade."
        )

    # Save default quality grade to heat_pumps_and_chillers.csv
    parameters_complete.quality_grade = quality_grade
    parameters_complete.to_csv(filename, index=False, header=True, float_format="%g")

    # create add on to filename (year, lat, lon)
    year = maya.parse(weather.index[int(len(weather) / 2)]).datetime().year

    # calculate COPs or EERs with oemof thermal
    if mode == "heat_pump":
        if len(high_temperature) > 1:
            add_on = f"_{year}_{lat}_{lon}"
        elif len(high_temperature) == 1:
            add_on = f"_{year}_{lat}_{lon}_{high_temperature[0]}"
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
            temp_low=low_temperature,
            quality_grade=quality_grade,
            mode=mode,
            temp_threshold_icing=temp_threshold_icing,
            factor_icing=factor_icing,
        )

        # define variables for later proceeding
        column_name = "cop"
        filename = f"cops_heat_pump{add_on}.csv"

    elif mode == "chiller":
        if len(low_temperature) > 1:
            add_on = f"_{year}_{lat}_{lon}"
        elif len(low_temperature) == 1:
            add_on = f"_{year}_{lat}_{lon}_{low_temperature[0]}"
        efficiency = cmpr_hp_chiller.calc_cops(
            temp_high=high_temperature,
            temp_low=low_temperature,
            quality_grade=quality_grade,
            mode=mode,
        )
        column_name = "eer"
        filename = f"eers_chiller{add_on}.csv"

    # add list of cops/eers to data frame
    df = pd.DataFrame(weather[temperature_col])

    try:
        df[column_name] = efficiency
    except ValueError:
        df[column_name] = np.multiply(efficiency, np.ones(len(df)))

    # set negative COPs/EERs to np.inf
    # COP/EER below zero results from temp_low > temp_high
    # and will therefore be represented with COP/EER -> infinity
    indices = df.loc[df[column_name] < 0].index
    df[column_name][indices] = np.inf

    # extract COPs/EERs as pd.Series from data frame
    efficiency_series = df[column_name]
    efficiency_series.name = "no_unit"

    # save time series to `user_inputs_mvs_directory/time_series`
    time_series_directory = os.path.join(user_inputs_mvs_directory, "time_series")

    logging.info(
        f"The cops of a heat pump are calculated and saved under {time_series_directory}."
    )

    efficiency_series.to_csv(
        os.path.join(time_series_directory, filename), index=False, header=True
    )

    return efficiency_series


def add_sector_coupling(
    weather,
    lat,
    lon,
    user_inputs_pvcompare_directory=None,
    user_inputs_mvs_directory=None,
    overwrite_hp_parameters=None,
):
    r"""
    Add heat sector if heat pump or chiller are in `energyConversion.csv`.

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
    user_inputs_pvcompare_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used as user_inputs_pvcompare_directory.
        Default: None.
    user_inputs_mvs_directory: str or None
        Directory of the multi-vector simulation inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
        Default: None.
    overwrite_hp_parameters: bool
        Default: True. If true, existing COP time series of the heat pump will be
        overwritten with calculated time series of COP.

    Notes
    -----
    Chillers were not tested, yet, and no automatic calculation of EERs is implemented.
    Attention: the above mentioned characteristics (inflow_direction: "Electricity",
    outflow_direction: "Heat") could also account for other heating elements. This
    function could be enhanced.

    Returns
    -------
    None
        Depending on the case, updates `energyConversion.csv` and saves calculated cops to
        'data/mvs_inputs/time_series'.
    """

    # read energyConversion.csv file
    if user_inputs_pvcompare_directory == None:
        user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
    if user_inputs_mvs_directory is None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    energy_conversion = pd.read_csv(
        os.path.join(user_inputs_mvs_directory, "csv_elements", "energyConversion.csv"),
        header=0,
        index_col=0,
    )
    heat_pump_and_chillers = pd.read_csv(
        os.path.join(user_inputs_pvcompare_directory, "heat_pumps_and_chillers.csv"),
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
                user_inputs_mvs_directory, "time_series", cops_filename_csv_excl_path
            )

            if not os.path.isfile(cops_filename_csv) or overwrite_hp_parameters == True:
                high_temperature = heat_pump_and_chillers.at["heat_pump", "temp_high"]
                year = weather.index[int(len(weather) / 2)].year
                cops_filename = os.path.join(
                    user_inputs_mvs_directory,
                    "time_series",
                    f"cops_heat_pump_{year}_{lat}_{lon}_{high_temperature}.csv",
                )

                if not overwrite_hp_parameters:
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
                    user_inputs_mvs_directory, "csv_elements", "energyConversion.csv"
                )
            )
            # calculate COPs of heat pump for location if not existent
            if not os.path.isfile(cops_filename):
                calculate_cops_and_eers(
                    weather=weather,
                    mode="heat_pump",
                    lat=lat,
                    lon=lon,
                    user_inputs_mvs_directory=user_inputs_mvs_directory,
                    user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
                )
                logging.info(
                    "COPs successfully calculated and saved in `user_inputs_mvs_directory/time_series`."
                )

        # display warning if heat demand seems to be missing in energyConsumption.csv
        energy_consumption = pd.read_csv(
            os.path.join(
                user_inputs_mvs_directory, "csv_elements", "energyConsumption.csv"
            ),
            header=0,
            index_col=0,
        )

    # chiller
    if "chiller" in [key.split("_")[0] for key in energy_conversion.keys()]:
        logging.warning(
            "Chillers were not tested, yet. Make sure to provide a cooling demand in "
            + "'energyConsumption.csv' and a constant EER or to place a file "
            + "containing EERs into `data/mvs_inputs/time_series` directory."
        )
    return None
