"""
This module reads existing csv files from "user_inputs_mvs_directory/csv_elements/"
and adapts the values of parameters according to the current simulation.

functions this module contains:
- add_scenario_name_to_project_data
- add_location_and_year_to_project_data
- check_for_valid_country_year
- add_electricity_price
- overwrite_mvs_energy_production_file
- add_parameters_to_energy_production_file
- add_file_name_to_energy_consumption_file
- add_evaluated_period_to_simulation_settings
- add_parameter_to_mvs_file
- load_parameter_from_mvs_file


"""
import pandas as pd
import os
import logging
from pvcompare import constants

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def add_scenario_name_to_project_data(user_inputs_mvs_directory, scenario_name):

    """
    Matches user input 'scenario_name' with 'scenario_name' in 'project_data.csv'.

    If user input 'scenario_name' is different to the parameter in
    'project_data.csv', a warning is returned and 'project_data.csv' is
    overwritten.

    Parameters
    ----------
    user_inputs_mvs_directory: str
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
    scenario_name: str
        Name of the Scenario. The name should follow the scheme:
        "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.

    Returns
    -------

    """
    add_parameter_to_mvs_file(
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        mvs_filename="project_data.csv",
        mvs_row="scenario_name",
        mvs_column="project_data",
        pvcompare_parameter=scenario_name,
        warning=True,
    )


def add_location_and_year_to_project_data(
    user_inputs_mvs_directory,
    static_inputs_directory,
    latitude,
    longitude,
    country,
    year,
):

    """
    Matches user input for year, latitude, longitude and yountry with mvs_inputs.

    If location (latitude, longitude, country) and year are entered as user
    input, the accorting porameters in 'mvs_inputs/csv_elements' are overwritten.
    If one of the location elements is None, an error is returned. If location
    or year is None, the according parameter is loaded from 'mvs_inputs/csv_elements'.
    Finally, it is checked whether country and year are valid.

    Parameters
    ----------
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
    static_inputs_directory: str or None
        Directory of the pvcompare static inputs. If None,
        `constants.DEFAULT_STATIC_INPUTS_DIRECTORY` is used as static_inputs_directory.
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
    if all(value is None for value in params.values()):
        output = {}
        for key in params:
            output[key] = load_parameter_from_mvs_file(
                user_inputs_mvs_directory,
                mvs_filename="project_data.csv",
                mvs_row=key,
                mvs_column="project_data",
            )
        latitude = float(output["latitude"])
        longitude = float(output["longitude"])
        country = output["country"]
    elif any(x is None for x in params.values()):
        raise ValueError(
            "If you want to overwrite the location parameters in the "
            "mvs_input files, please enter all three input parameters: "
            "latitude, longitude and country into the main.py user inputs."
        )
    else:
        for key in params:
            add_parameter_to_mvs_file(
                user_inputs_mvs_directory=user_inputs_mvs_directory,
                mvs_filename="project_data.csv",
                mvs_row=key,
                mvs_column="project_data",
                pvcompare_parameter=params[key],
                warning=True,
            )
    if year is None:
        start_date = load_parameter_from_mvs_file(
            user_inputs_mvs_directory=user_inputs_mvs_directory,
            mvs_filename="simulation_settings.csv",
            mvs_row="start_date",
            mvs_column="simulation_settings",
        )
        year = str(start_date)[:-15]
    else:
        start_date = str(year) + "-01-01 00:00:00"
        add_parameter_to_mvs_file(
            user_inputs_mvs_directory=user_inputs_mvs_directory,
            mvs_filename="simulation_settings.csv",
            mvs_row="start_date",
            mvs_column="simulation_settings",
            pvcompare_parameter=start_date,
            warning=True,
        )
    # check if country and year are valid
    check_for_valid_country_year(country, year, static_inputs_directory)

    return latitude, longitude, country, int(year)


def check_for_valid_country_year(country, year, static_inputs_directory):
    """
    Checks static input files for valid countries and years and returns error
    if the country or year of the simulation is not valid.
    Static input files that are checked: 'EUROSTAT_population.csv',
    'list_of_workalender_countries.csv', 'total_electricity_consumption_residential.csv'

    Parameters
    ----------
    country: str
        country of simulation
    year: int
        year of simulation
    static_inputs_directory: str or None
        Directory of the pvcompare static inputs. If None,
        `constants.DEFAULT_STATIC_INPUTS_DIRECTORY` is used as static_inputs_directory.

    Returns
    -------

    """
    pop = pd.read_csv(
        os.path.join(static_inputs_directory, "EUROSTAT_population.csv"),
        header=0,
        sep=",",
    )
    workalendar = pd.read_csv(
        os.path.join(static_inputs_directory, "list_of_workalender_countries.csv"),
        header=0,
    )
    consumption = pd.read_excel(
        os.path.join(
            static_inputs_directory, "electricity_consumption_residential.xlsx"
        ),
        header=1,
        index_col=0,
    )

    countries_pop = set(pop["country"][:43])
    countries_workalender = set(workalendar["country"])
    countries_consumption = set(consumption.index[:30])

    years_pop = set([x for x in pop.columns if x != "country"])
    years_consumption = set(
        [
            str(x)
            for x in consumption.columns
            if x not in ["country", "ISO code", "Unit", "Source Code", "Note", "Source"]
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


def add_electricity_price(static_inputs_directory, user_inputs_mvs_directory):
    """
    Adds the electricity price from 'electricity_prices.csv' to 'energyProviders.csv'.

    This function adds the cost of electricity for the country and the latest
     year (2019) from the csv
    file 'electricity_prices.csv' to 'energyProviders.csv'.
    If the value is already provided in the 'energyProviders.csv' and this value
    differs from the one in 'electricity_prices.csv' a warning is returned.

    Parameters
    -----------
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
    static_inputs_directory: str or None
        Directory of the pvcompare static inputs. If None,
        `constants.DEFAULT_STATIC_INPUTS_DIRECTORY` is used as static_inputs_directory.

    Returns
    --------
    None
    """
    # load electricity prices
    prices_file_path = os.path.join(static_inputs_directory, "electricity_prices.csv")
    electricity_prices_eu = pd.read_csv(prices_file_path, index_col=0)

    # load project data to select country
    project_data_filename = os.path.join(
        user_inputs_mvs_directory, "csv_elements/" "project_data.csv"
    )
    project_data = pd.read_csv(project_data_filename, index_col=0)
    country = project_data.at["country", "project_data"]

    # load latest electricity_price
    electricity_price = electricity_prices_eu.at[country, "2019"]

    add_parameter_to_mvs_file(
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        mvs_filename="energyProviders.csv",
        mvs_row="energy_price",
        mvs_column="Electricity grid",
        pvcompare_parameter=electricity_price,
        warning=True,
    )


def overwrite_mvs_energy_production_file(
    pv_setup,
    user_inputs_mvs_directory,
    user_inputs_pvcompare_directory,
    overwrite_pv_parameters,
    collections_mvs_inputs_directory=None,
):
    """
    Inserts default values for PV technologies defined in pv_setup.csv

    This function compares the number of powerplants in energyProduction.csv
    with the number of rows in pv_setup.csv. If the number differs the process
    throws an error.


    Parameters
    ----------
    pv_setup: dict
        Dictionary that contains the surface types with technology and
        orientation
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.

    Returns
    ---------
    None
    """
    # load pv_setup.csv
    if pv_setup is None:
        pv_setup = pd.read_csv(
            os.path.join(user_inputs_pvcompare_directory, "pv_setup.csv"), index_col=0
        )
    technologies = pv_setup["technology"].values

    # load mvs user input file
    if user_inputs_mvs_directory is None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    if collections_mvs_inputs_directory is None:
        collections_mvs_inputs_directory = (
            constants.DEFAULT_COLLECTION_MVS_INPUTS_DIRECTORY
        )
    filename = os.path.join(
        user_inputs_mvs_directory, "csv_elements/" "energyProduction.csv"
    )
    user_input_ep = pd.read_csv(filename, index_col=0)

    if not overwrite_pv_parameters:
        if len(technologies) < len(user_input_ep.columns):
            raise ValueError(
                "The number of pv plants in pv_setup.csv is lower "
                "than the number of columns in energyProduction.csv. "
                "Please adapt the files or set 'overwrite_pv_parameters == True'."
            )
        for t in technologies:
            label = "PV " + t
            if label in user_input_ep.columns:
                logging.info(
                    "The technology in setup.py equals the column name "
                    "in energyProduction.csv. It will not be overwritten."
                )
            else:
                raise ValueError(
                    "The technology in 'pv_setup.py' differs from the "
                    "column name in 'energyProduction.csv'. Please "
                    "adapt the technology or set 'overwrite_pv_parameters == True'."
                )
    else:
        # drop all columns except of index and unit
        user_input_ep.drop(
            user_input_ep.columns.difference(["index", "unit"]), 1, inplace=True
        )
        # get pv parameters from collection_mvs_inputs
        if collections_mvs_inputs_directory is None:
            collections_mvs_inputs_directory = (
                constants.DEFAULT_COLLECTION_MVS_INPUTS_DIRECTORY
            )
        collection_filename = os.path.join(
            collections_mvs_inputs_directory, "csv_elements", "energyProduction.csv"
        )
        collection_ep = pd.read_csv(collection_filename, index_col=0)
        for t in technologies:
            i = 1
            label = "PV " + t
            if label in user_input_ep.columns:
                user_input_ep[label + str(i)] = collection_ep[label]
                i += 1
            else:
                # insert column from collection_mvs_inputs
                user_input_ep[label] = collection_ep[label]
            logging.info(
                f"The column {t} has been successfully added to "
                f"user_inputs/mvs_inputs/csv_elements/energyProduction.csv."
            )

        user_input_ep.to_csv(filename)


def add_parameters_to_energy_production_file(
    technology, ts_filename, nominal_value, user_inputs_mvs_directory=None
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
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.

    Returns
    -------
    None
    """
    # add maximum capacity
    label = "PV " + technology
    add_parameter_to_mvs_file(
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        mvs_filename="energyProduction.csv",
        mvs_row="maximumCap",
        mvs_column=label,
        pvcompare_parameter=nominal_value,
        warning=False,
    )
    # add file name
    add_parameter_to_mvs_file(
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        mvs_filename="energyProduction.csv",
        mvs_row="file_name",
        mvs_column=label,
        pvcompare_parameter=ts_filename,
        warning=False,
    )


def add_file_name_to_energy_consumption_file(
    column, ts_filename, user_inputs_mvs_directory=None
):

    """
    Enters demand time series file name to 'energyProduction.csv'.

    Parameters
    ---------
    column: str
        column name of 'energyProduction.csv'
    ts_filename: str
        file name of the demand time series
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.

    Returns
    -------
    None
    """

    add_parameter_to_mvs_file(
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        mvs_filename="energyConsumption.csv",
        mvs_row="file_name",
        mvs_column=column,
        pvcompare_parameter=ts_filename,
        warning=False,
    )


def add_evaluated_period_to_simulation_settings(time_series, user_inputs_mvs_directory):
    """
    adds number of days of the time series into simulation_settings.csv

    Parameters
    ----------
    time_series: :pandas:`pandas.DataFrame<frame>`
        pv time series
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.

    Returns
    ------
    None
    """

    length = len(time_series.index) / 24
    add_parameter_to_mvs_file(
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        mvs_filename="simulation_settings.csv",
        mvs_row="evaluated_period",
        mvs_column="simulation_settings",
        pvcompare_parameter=int(length),
        warning=False,
    )


def add_parameter_to_mvs_file(
    user_inputs_mvs_directory,
    mvs_filename,
    mvs_row,
    mvs_column,
    pvcompare_parameter,
    warning=True,
):
    """
    Overwrites a value from a file in 'mvs_inputs/csv_elements' with a user input.

    Parameters
    ----------
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
    mvs_filename: str
        name of the mvs-csv file
    mvs_row: str
        row name of the value in 'mvs_filename'
    mvs_column: str
        column name of the value in 'mvs_filename'
    pvcompare_parameter: str
        parameter that should be added to the mvs_csv file
    warning: bool
        if True, a waring is returned that the parameter with the name
        'mvs_row' is overwritten

    Returns
    ------
    None
    """
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY

    filename = os.path.join(user_inputs_mvs_directory, "csv_elements", mvs_filename)
    # load mvs_csv_file
    mvs_file = pd.read_csv(filename, index_col=0)

    if warning is True:
        if mvs_file.at[mvs_row, mvs_column] != pvcompare_parameter:
            logging.warning(
                f"The parameter {pvcompare_parameter} differs from"
                f"the parameter {mvs_row} in {mvs_filename} and thus will "
                f"be overwritten."
            )

    mvs_file.loc[[mvs_row], [mvs_column]] = pvcompare_parameter
    mvs_file.to_csv(filename)
    logging.info(
        f"The parameter {mvs_row} has been added to the "
        f"mvs input file {mvs_filename}."
    )


def load_parameter_from_mvs_file(
    user_inputs_mvs_directory, mvs_filename, mvs_row, mvs_column
):
    """
    Loads a value from a file in 'mvs_inputs/csv_elements'.

    Parameters
    ----------
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
    mvs_filename: str
        name of the mvs-csv file
    mvs_row: str
        row name of the value in 'mvs_filename'
    mvs_column: str
        column name of the value in 'mvs_filename'

    Returns
    ------
    str
        parameter that is loaded from mvs_file
    """

    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY

    filename = os.path.join(user_inputs_mvs_directory, "csv_elements", mvs_filename)
    # load mvs_csv_file
    mvs_file = pd.read_csv(filename, index_col=0)

    pvcompare_parameter = mvs_file.at[mvs_row, mvs_column]

    logging.info(
        f"The parameter {mvs_row} has been loaded from the "
        f"mvs input file {mvs_filename}."
    )
    return pvcompare_parameter
