"""
This module reads existing csv files from "mvs_input_directory/csv_elements/"
and adapts the values of parameters according to the current simulation.
"""
from pvlib.location import Location
import pvlib.atmosphere
from pvlib.pvsystem import PVSystem
from pvlib.modelchain import ModelChain
import pandas as pd
import os
import pvlib
import glob
import logging
import sys
import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

import cpvtopvlib.cpvsystem as cpv
import greco_technologies.cpv.hybrid
import greco_technologies.cpv.inputs
from pvcompare import area_potential
from pvcompare import constants


def check_for_valid_country_year(country, year, input_directory):
    """
    checks if the input country is available in all input data

    The inputs checkes the countries for population, workalender and consumption.

    Parameters
    ----------
    country: str
        country of interest
    year: int
        year of interest
    input_directory: str
        input directory for data input

    Returns
    -------

    """

    pop = pd.read_csv(
        os.path.join(input_directory, "EUROSTAT_population.csv"), header=0, sep=","
    )
    workalendar = pd.read_csv(
        os.path.join(input_directory, "list_of_workalender_countries.csv"), header=0
    )
    consumption = pd.read_csv(
        os.path.join(input_directory, "total_electricity_consumption_residential.csv"),
        header=1,
        sep=":",
    )

    countries_pop = set(pop["country"][:43])
    countries_workalender = set(workalendar["country"])
    countries_consumption = set(consumption["country"][:32])

    years_pop = set([x for x in pop.columns if x != "country"])
    years_consumption = set(
        [
            x
            for x in consumption.columns
            if x not in ["country", "ISO code", "Unit", "Source Code", "Note"]
        ]
    )

    possible_countries = countries_pop & countries_workalender & countries_consumption
    possible_years = years_pop & years_consumption

    if country not in possible_countries:
        raise ValueError(
            f"The given country {country} is not recognized. "
            f"Please select one of the following "
            f"countries: {possible_countries}"
        )

    if str(year) not in possible_years:
        raise ValueError(
            f"The given year {year} is not recognized. "
            f"Please select one of the following "
            f"years: {possible_years}"
        )


def add_project_data(mvs_input_directory, latitude, longitude, country, year):
    """
    matches user input with mvs_inputs/csv_elements

    checks if latitude, longitude, country and year exist either as a user
    input or in the csv files. If a user input exists, the parameter in the
    certain csv file will be overwritten, otherwise the parameter is taken from
    the csv file.

    Parameters
    ----------
    mvs_input_directory: str
        directory to "mvs_inputs/"
    latitude: float
        latitude of the location
    longitude: float
        longitude of the location
    country: str
        country of the location
    year: int
        year of the simulation

    Returns
    -------

    """

    if mvs_input_directory == None:
        mvs_input_directory = os.path.join(constants.DEFAULT_MVS_INPUT_DIRECTORY)
    project_data_filename = os.path.join(
        mvs_input_directory, "csv_elements/" "project_data.csv"
    )
    if os.path.isfile(project_data_filename):
        project_data = pd.read_csv(project_data_filename, index_col=0)

        params = {"latitude": latitude, "longitude": longitude, "country": country}
        for key in params:
            if params[key] is None:
                logging.info(f"The parameter {key} is taken " f"from project_data.csv.")
                params[key] = project_data.at[key, "project_data"]
                if pd.isna(params[key]) == True:
                    raise ValueError(
                        f"The parameter {key} cannot be None. "
                        f"Please correct the parameter {key} in "
                        f"project_data.csv or change the paremeter "
                        f"in the main function."
                    )
            if params[key] != project_data.at[key, "project_data"]:
                logging.warning(
                    f"The parameter {key} in the main function"
                    f" differs from the value in"
                    f" project_data.csv. The value in file "
                    f"project_data.csv will be overwritten."
                )
                project_data.at[key, "project_data"] = params[key]

    else:
        logging.warning(
            f"The file project_data.csv does not"
            f"exist. Please check the input folder {mvs_input_directory}"
            "/csv_elements"
        )
    # change and insert start date in simulation settings
    simulation_settings_filename = os.path.join(
        mvs_input_directory, "csv_elements/" "simulation_settings.csv"
    )
    if os.path.isfile(simulation_settings_filename):
        simulation_settings = pd.read_csv(simulation_settings_filename, index_col=0)
    start_date = simulation_settings.at["start_date", "simulation_settings"]
    start_date = None if start_date == "None" else start_date
    if pd.isna(start_date) == False:
        year_ss = str(start_date)[:-15]
    else:
        year_ss = None
    if year is None:
        logging.info(f"The parameter 'year' is taken " f"from simulation_settings.csv.")
        if start_date is None:
            raise ValueError(
                f"The parameter year cannot be None. "
                f"Please correct the parameter 'start_date' in "
                f"simulation_settings.csv or change the paremeter "
                f"'year' in the main function."
            )
        else:
            year_ss = str(start_date)[:-15]
            year = year_ss
    elif year is not year_ss:
        logging.warning(
            f"The parameter year in the main function"
            f" does not correspond to the value in"
            f" simulation_settings.csv. The value in file "
            f"simulation_settings.csv will be overwritten."
        )
        simulation_settings.at["start_date", "simulation_settings"] = (
            str(year) + "-01-01 00:00:00"
        )

    # save energyProduction.csv
    project_data.to_csv(project_data_filename)
    simulation_settings.to_csv(simulation_settings_filename)
    return latitude, longitude, country, year


def energy_price_check(mvs_input_directory, electricity_price, country=None):
    """
    Checks the electricity price of 'energyProviders.csv'.

    This function is called by the main function when then user-input value of the cost of
    grid electricity is None (i.e., not provided by the user). This function then determines the cost
    of electricity by checking in the energyProviders.csv, and returns the value.
    If the value is not provided in that csv either,
    then the value from the csv with energy prices in the EU is obtained and returned.

    Parameters:
    -----------
    mvs_input_directory : str
        directory to "mvs_inputs/"
    energy_price :  float
        the price of electricity is either None or 0
    country : str
        the EU country for which the electricity price is to be determined

    Returns:
    --------
    energy_price : float
        price of the grid electrcity
    Updates value of energy_price in energyProviders.csv
    """
    if mvs_input_directory is None:
        mvs_input_directory = os.path.join(constants.DEFAULT_MVS_INPUT_DIRECTORY)
    energy_providers_filename = os.path.join(
        mvs_input_directory, "csv_elements/" "energyProviders.csv"
    )

    # Create dataframe containing the household electricity prices in the EU nations
    prices_file_path = os.path.join(
        constants.DEFAULT_INPUT_DIRECTORY, "electricity_prices_households.csv"
    )
    electricity_prices_eu = pd.read_csv(prices_file_path, index_col=0)

    if os.path.isfile(energy_providers_filename):
        grid_related = pd.read_csv(energy_providers_filename, index_col=0)

        if electricity_price is None:
            logging.info(
                f"The parameter electricity_price is taken from energyProviders.csv."
            )
            electricity_price = grid_related.at["energy_price", "Electricity grid "]
            if electricity_price is np.nan:
                logging.info(f"The parameter is not available in energyProviders.csv.")
                try:
                    electricity_price_from_csv = electricity_prices_eu.at[
                        country, "electricity_price_2019"
                    ]
                    electricity_price = electricity_price_from_csv
                except KeyError:
                    raise KeyError(
                        f"Please enter a country within the EU, you entered {country}."
                    )
                grid_related.at["energy_price", "Electricity grid "] = electricity_price
                grid_related.to_csv(energy_providers_filename)

        elif electricity_price != grid_related.at["energy_price", "Electricity grid "]:
            logging.warning(
                f"The parameter energy_price in the main function"
                f" differs from the value in"
                f" energyProviders.csv. The value in file "
                f"energyProviders.csv will be overwritten."
            )
            grid_related.at["energy_price", "Electricity grid "] = float(
                electricity_price
            )
            grid_related.to_csv(energy_providers_filename)

    else:
        logging.warning(
            f"The file energyProviders.csv does not "
            f"exist. Please check the input folder {mvs_input_directory}"
            "/csv_elements"
        )
    return electricity_price


def check_mvs_energy_production_file(
    pv_setup, mvs_input_directory=None, overwrite=True
):
    """
    checks if energyProduction.csv file with correct number of collumns exists.

    This function compares the number of powerplants in energyProduction.csv
    with the number of rows in pv_setup.csv. If the number differs and
    overwrite=True, a new energyProduction.csv file is created with the correct
    number of columns and default values. The old file is overwritten. If
    overwrite=False, the process throws an error.


    Parameters
    ----------
    pv_setup: dict
        Dictionary that contains the surface types with technology and
        orientation
    directory_energy_production: str
        path to the energyProduction.csv
    overwrite: bool

    Returns
    ---------
    None
    """

    if mvs_input_directory == None:
        mvs_input_directory = os.path.join(constants.DEFAULT_MVS_INPUT_DIRECTORY)
    energy_production_filename = os.path.join(
        mvs_input_directory, "csv_elements/" "energyProduction.csv"
    )
    if os.path.isfile(energy_production_filename):
        energy_production = pd.read_csv(energy_production_filename, index_col=0)

        if len(energy_production.columns) - 1 == len(pv_setup.index):
            logging.info(
                "mvs_input file energyProduction.csv contains the correct"
                "number of pv powerplants."
            )
        elif overwrite == False:
            raise ValueError(
                "The number of pv powerplants in energyProduction.csv"
                " differs from the number of powerplants listed in "
                "pv_setup.csv. Please check energyProduction.csv or "
                "allow overwrite=True to have energyProduction.csv "
                "set up automatically with default values. "
            )
        else:
            logging.warning(
                "The number of pv powerplants in energyProduction.csv"
                " differs from the number of powerplants listed in "
                "pv_setup.csv. The file energyProduction.csv will thus "
                "be overwritten and created anew with default values."
            )
            create_mvs_energy_production_file(pv_setup, energy_production_filename)

    elif overwrite == False:
        raise ValueError(
            "The file %s" % energy_production_filename + " does not"
            "exist. Please create energyProduction.csv or "
            "allow overwrite=True to have energyProduction.csv "
            "set up automatically with default values."
        )
    else:
        logging.warning(
            "The file %s" % energy_production_filename + "does not"
            "exist. It will thus be created anew with default "
            "values."
        )


def create_mvs_energy_production_file(pv_setup, energy_production_filename):
    """
    creates a new energyProduction.csv file

    creates a new energyProduction.csv file with the correct number of pv
    powerplants as defined in pv_setup.py and saves it into ./data/mvs_inputs/
    csv_elements/csv/energyProduction.csv

    Parameters
    ----------
    pv_setup: dict
        dictionary that contains details on the pv-surfaces
    energy_production_filename: str
        default: /data/mvs_inputs/csv_elements/csv/energyProduction.csv

    Returns
    ---------
    None
    """
    # hardcoded list of parameters
    data = {
        "index": [
            "age_installed",
            "capex_fix",
            "capex_var",
            "file_name",
            "installedCap",
            "label",
            "lifetime",
            "opex_fix",
            "opex_var",
            "optimizeCap",
            "outflow_direction",
            "type_oemof",
            "unit",
            "energyVector",
        ],
        "unit": [
            "year",
            "currency",
            "currency/unit",
            "str",
            "kWp",
            "str",
            "year",
            "currency/unit/year",
            "currency/kWh",
            "bool",
            "str",
            "str",
            "str",
            "str",
        ],
    }
    df = pd.DataFrame(data, columns=["index", "unit"])
    df.set_index("index", inplace=True)
    for i, row in pv_setup.iterrows():
        # hardcoded default parameters
        pp = [
            "0",
            "10000",
            "7200",
            "0",
            "0",
            "PV plant (mono)",
            "30",
            "80",
            "0",
            "True",
            "PV plant (mono)",
            "source",
            "kWp",
            "Electricity",
        ]
        df["pv_plant_0" + str(i + 1)] = pp

    df.to_csv(energy_production_filename)


def add_parameters_to_energy_production_file(
    pp_number, ts_filename, nominal_value, mvs_input_directory=None
):
    """
    enters new parameters into energyProduction.csv

    Parameters
    ---------
    pp_number: int
        number of powerplants / columns in pv_setup
    ts_filename: str
        file name of the pv time series
    nominal_value: float
        maximum value of installable capacity
    directory_energy_production: str
        default: DEFAULT_MVS_INPUT_DIRECTORY/csc_elements/

    Returns
    -------
    None
    """

    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    energy_production_filename = os.path.join(
        mvs_input_directory, "csv_elements/energyProduction.csv"
    )
    # load energyProduction.csv
    energy_production = pd.read_csv(energy_production_filename, index_col=0)
    # insert parameter values
    energy_production.loc[
        ["maximumCap"], ["pv_plant_0" + str(pp_number)]
    ] = nominal_value
    logging.info(
        "The maximum capacity of pv_plant_0%s" % pp_number + " has "
        "been added to energyProduction.csv."
    )
    energy_production.loc[["file_name"], ["pv_plant_0" + str(pp_number)]] = ts_filename
    energy_production.loc[["label"], ["pv_plant_0" + str(pp_number)]] = (
        "PV " + str(ts_filename)[:-4]
    )
    logging.info(
        "The file_name of the time series of PV "
        + str(ts_filename)[:-4]
        + " has been added to energyProduction.csv."
    )
    # save energyProduction.csv
    energy_production.to_csv(energy_production_filename)


def add_evaluated_period_to_simulation_settings(time_series, mvs_input_directory):
    """
    adds number of days of the time series into simulation_settings.csv

    Parameters
    ----------
    time_series: :pandas:`pandas.DataFrame<frame>`
        pv time series
    mvs_input_directory: str
        path to mvs input directory

    Returns
    ------
    None
    """

    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    simulation_settings_filename = os.path.join(
        mvs_input_directory, "csv_elements/simulation_settings.csv"
    )
    # load simulation_settings.csv
    simulation_settings = pd.read_csv(simulation_settings_filename, index_col=0)
    length = len(time_series.index) / 24
    simulation_settings.loc[["evaluated_period"], ["simulation_settings"]] = int(length)
    simulation_settings.to_csv(simulation_settings_filename)
