"""
This module reads existing csv files from "mvs_input_directory/csv_elements/"
and adapts the values of parameters according to the current simulation.
"""
import pandas as pd
import os
import logging
from pvcompare import constants

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


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
        directory to 'mvs_inputs/'
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


def add_electricity_price(mvs_input_directory=None):
    """
    Adds the electricity price from 'electricity_prices.csv' to 'energyProviders.csv'.

    This function is called by the main function when the value of the parameter
    "energy_price" in energyProviders.csv is None. This function then adds the
    cost of electricity for the country and year from the csv file 'electricity_prices.csv' to
    energyProviders.csv.
    If the value is already provided in the 'energyProviders.csv' and this value
    differs from the one in 'electricity_prices.csv' a warning is returned.

    Parameters
    -----------
    mvs_input_directory : str
        directory to "mvs_inputs/"

    Returns
    --------
    None
    """
    # load energyProviders
    if mvs_input_directory is None:
        mvs_input_directory = os.path.join(constants.DEFAULT_MVS_INPUT_DIRECTORY)
    energy_providers_filename = os.path.join(
        mvs_input_directory, "csv_elements/" "energyProviders.csv"
    )
    if os.path.isfile(energy_providers_filename):
        energy_providers = pd.read_csv(energy_providers_filename, index_col=0)
    else:
        logging.error("The file energyProviders.csv is missing ")

    # load electricity prices
    prices_file_path = os.path.join(
        constants.DEFAULT_INPUT_DIRECTORY, "electricity_prices.csv"
    )
    electricity_prices_eu = pd.read_csv(prices_file_path, index_col=0)

    # load project data to select country
    project_data_filename = os.path.join(
        mvs_input_directory, "csv_elements/" "project_data.csv"
    )
    if os.path.isfile(project_data_filename):
        project_data = pd.read_csv(project_data_filename, index_col=0)
        country = project_data.at["country", "project_data"]
    else:
        logging.error("The file project_data.csv is missing.")

    # load simulation settings for year
    simulation_settings_filename = os.path.join(
        mvs_input_directory, "csv_elements/" "simulation_settings.csv"
    )
    if os.path.isfile(simulation_settings_filename):
        simulation_settings = pd.read_csv(simulation_settings_filename, index_col=0)
    else:
        logging.error("The file simulation_settings.csv is missing.")
    start_date = simulation_settings.at["start_date", "simulation_settings"]
    year = str(start_date)[:-15]

    electricity_price = energy_providers.at["energy_price", "DSO"]

    electricity_price_from_csv = electricity_prices_eu.at[country, year]

    if pd.isna(electricity_price) == False:
        if electricity_price != electricity_price_from_csv:
            logging.warning(
                "The electricity price in energyProviders.csv "
                "differs from the reference value of "
                f"{electricity_price_from_csv} for the country "
                f"{country}. If you want it to be overwritten "
                f"automatically, please set the value of "
                f"energy_Price in energyProviders.csv to None."
            )
    else:
        energy_providers.at["energy_price", "DSO"] = electricity_price_from_csv
        energy_providers.to_csv(energy_providers_filename)
        logging.info(
            "The parameter energy_price has been automatically added"
            "to energyProviders.csv."
        )
        electricity_price = electricity_price_from_csv
    return electricity_price


def check_mvs_energy_production_file(pv_setup, mvs_input_directory=None):
    """
    checks if energyProduction.csv file with correct number of collumns exists.

    This function compares the number of powerplants in energyProduction.csv
    with the number of rows in pv_setup.csv. If the number differs the process
    throws an error.


    Parameters
    ----------
    pv_setup: dict
        Dictionary that contains the surface types with technology and
        orientation
    directory_energy_production: str
        path to the energyProduction.csv

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
                "the mvs_input file energyProduction.csv contains the correct"
                "number of pv powerplants."
            )
        else:
            raise ValueError(
                "The number of pv powerplants in energyProduction.csv"
                " differs from the number of powerplants listed in "
                "pv_setup.csv. Please correct the number of columns in"
                " energyProduction.csv"
            )

    else:
        raise ValueError(
            "The file %s" % energy_production_filename + " does not"
            "exist. Please create energyProduction.csv."
        )


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


def add_parameters_to_energy_consumption_file(
    column, ts_filename, mvs_input_directory=None
):

    """
    enters new parameters into energyProduction.csv

    Parameters
    ---------
    column: str
        demand_01 or demand_02
    ts_filename: str
        file name of the demand time series
    mvs_input_directory: str
        default: DEFAULT_MVS_INPUT_DIRECTORY

    Returns
    -------
    None
    """

    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    energy_consumption_filename = os.path.join(
        mvs_input_directory, "csv_elements/energyConsumption.csv"
    )

    # load energyConsumption.csv
    energy_consumption = pd.read_csv(energy_consumption_filename, index_col=0)

    # check if demand column is available
    if column not in energy_consumption.columns:
        logging.warning(
            f"The demand {column} is not in energyConsumption.csv. "
            f"Please make sure you insert the column if the demand "
            f"is needed in further simulations."
        )
    else:
        # insert parameter values
        energy_consumption.loc[["file_name"], [column]] = ts_filename

        logging.info(
            "The file_name of the demand time series "
            "has been added to energyProduction.csv."
        )
        # save energyProduction.csv
        energy_consumption.to_csv(energy_consumption_filename)


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
