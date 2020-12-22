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


def add_scenario_name_to_project_data(mvs_input_directory, scenario_name):

    """
    matches user input 'scenario_name' with 'scenario_name' in 'project_data.csv'

    If user input 'scenario_name' is different in 'project_data.csv', a warning
    is returned.

    Parameters
    ----------
    mvs_input_directory: str
        directory to 'mvs_inputs/'
    scenario_name: str
        Name of the Scenario. The name should follow the scheme:
        "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.

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

        if scenario_name != project_data.at["scenario_name", "project_data"]:
            logging.warning(
                f"The parameter {scenario_name} in the main function"
                f" differs from the value in"
                f" project_data.csv. The value in file "
                f"project_data.csv will be overwritten."
            )
            project_data.at["scenario_name", "project_data"] = scenario_name

    else:
        logging.warning(
            f"The file project_data.csv does not"
            f"exist. Please check the input folder {mvs_input_directory}"
            "/csv_elements"
        )

    # save project data
    project_data.to_csv(project_data_filename)
    return


def check_for_valid_country_year(country, year, static_input_directory):
    """
    checks if the input country is available in all input data

    The inputs checkes the countries for population, workalender and consumption.

    Parameters
    ----------
    country: str
        country of interest
    year: int
        year of interest
    static_input_directory: str
        input directory for static data input

    Returns
    -------

    """

    pop = pd.read_csv(
        os.path.join(static_input_directory, "EUROSTAT_population.csv"),
        header=0,
        sep=",",
    )
    workalendar = pd.read_csv(
        os.path.join(static_input_directory, "list_of_workalender_countries.csv"),
        header=0,
    )
    consumption = pd.read_csv(
        os.path.join(
            static_input_directory, "total_electricity_consumption_residential.csv"
        ),
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
    params = {"latitude": latitude, "longitude": longitude, "country": country}
    if all(params)==None:
        output = {}
        for key in params:
            output[key] = load_parameter_from_mvs_file(mvs_input_directory,
                                      mvs_filename="project_data.csv",
                                      mvs_row=key,
                                      mvs_column="project_data")
        latitude=output["latitude"]
        longitude = output["longitude"]
        country = output["country"]
    elif any(x is None for x in params):
        raise ValueError("If you want to overwrite the location parameters in the "
                      "mvs_input files, please enter all three input parameters: "
                      "latitude, longitude and country into the main.py user inputs.")
    else:
        for key in params:
            add_parameter_to_mvs_file(mvs_input_directory,
                                      mvs_filename="project_data.csv",
                                      mvs_row=key,
                                      mvs_column="project_data",
                                      pvcompare_parameter=params[key],
                                      warning=True)
    if year is None:
        start_date=load_parameter_from_mvs_file(mvs_input_directory,
                                     mvs_filename="simulation_settings.csv",
                                     mvs_row="start_date",
                                     mvs_column="simulation_settings")
        year = str(start_date)[:-15]
    else:
        start_date = str(year) + "-01-01 00:00:00"
        add_parameter_to_mvs_file(mvs_input_directory,
                                  mvs_filename="simulation_settings.csv",
                                  mvs_row="start_date",
                                  mvs_column="simulation_settings",
                                  pvcompare_parameter=start_date,
                                  warning=True)

    return latitude, longitude, country, year


def add_electricity_price(static_input_directory, mvs_input_directory):
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
    static_input_directory: str


    Returns
    --------
    None
    """
    # load electricity prices
    prices_file_path = os.path.join(static_input_directory, "electricity_prices.csv")
    electricity_prices_eu = pd.read_csv(prices_file_path, index_col=0)

    # load project data to select country
    project_data_filename = os.path.join(
        mvs_input_directory, "csv_elements/" "project_data.csv")
    project_data = pd.read_csv(project_data_filename, index_col=0)
    country = project_data.at["country", "project_data"]

    # load latest electricity_price
    electricity_price = electricity_prices_eu.at[country, "2019"]

    add_parameter_to_mvs_file(mvs_input_directory,
                              mvs_filename="energyProviders.csv",
                              mvs_row="energy_price",
                              mvs_column="DSO",
                              pvcompare_parameter=electricity_price,
                              warning=True)



def check_mvs_energy_production_file(pv_setup, mvs_input_directory=None):      #todo:add pv_plant to energyProduction.csv
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
    technology, ts_filename, nominal_value, mvs_input_directory=None
):

    """
    enters new parameters into energyProduction.csv

    Parameters
    ---------
    technology: str
        technology of the pv plant. Should equal column name in energyProduction.csv.
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
    # add maximum capacity
    add_parameter_to_mvs_file(mvs_input_directory,
                              mvs_filename="energyProduction.csv",
                              mvs_row="maximumCap",
                              mvs_column=technology,
                              pvcompare_parameter=nominal_value,
                              warning=False)
    # add file name
    add_parameter_to_mvs_file(mvs_input_directory,
                              mvs_filename="energyProduction.csv",
                              mvs_row="file_name",
                              mvs_column=technology,
                              pvcompare_parameter=ts_filename,
                              warning=False)


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

    add_parameter_to_mvs_file(mvs_input_directory,
                              mvs_filename="energyConsumption.csv",
                              mvs_row="file_name",
                              mvs_column=column,
                              pvcompare_parameter=ts_filename, warning=False)



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

    length = len(time_series.index) / 24
    add_parameter_to_mvs_file(mvs_input_directory=mvs_input_directory,
                              mvs_filename="simulation_settings.csv",
                              mvs_row="evaluated_period",
                              mvs_column="simulation_settings",
                              pvcompare_parameter=int(length),
                              warning=False)


def add_parameter_to_mvs_file(mvs_input_directory, mvs_filename, mvs_row,
                              mvs_column, pvcompare_parameter, warning = True):
    """

    :param mvs_csv_file:
    :param mvs_parameter:
    :param pvcompare_parameter:
    :return:
    """
    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

    filename = os.path.join(
        mvs_input_directory, "csv_elements", mvs_filename
    )
    # load mvs_csv_file
    mvs_file = pd.read_csv(filename, index_col=0)

    if warning is True:
        if mvs_file.at[mvs_row, mvs_column] != pvcompare_parameter:
            logging.warning(f"The parameter {pvcompare_parameter} differs from"
                            f"the parameter {mvs_row} in {mvs_filename} and thus will "
                            f"be overwritten.")

    mvs_file.loc[[mvs_row], [mvs_column]] = pvcompare_parameter
    mvs_file.to_csv(filename)
    logging.info(f"The parameter {mvs_row} has been added to the "
                 f"mvs input file {mvs_filename}.")

def load_parameter_from_mvs_file(mvs_input_directory, mvs_filename, mvs_row,
                              mvs_column):
    """

    :param mvs_input_directory:
    :param mvs_filename:
    :param mvs_row:
    :param mvs_column:
    :param pvcompare_parameter:
    :param warning:
    :return:
    """

    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

    filename = os.path.join(
        mvs_input_directory, "csv_elements", mvs_filename
    )
    # load mvs_csv_file
    mvs_file = pd.read_csv(filename, index_col=0)

    pvcompare_parameter = mvs_file.at[mvs_row, mvs_column]

    logging.info(f"The parameter {mvs_row} has been loaded from the "
                 f"mvs input file {mvs_filename}.")
    return pvcompare_parameter