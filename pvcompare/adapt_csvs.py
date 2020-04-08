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

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

import cpvtopvlib.cpvsystem as cpv
import greco_technologies.cpv.hybrid
import greco_technologies.cpv.inputs
from pvcompare import area_potential
from pvcompare import constants


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
    energy_production.loc[
        ["label"], ["pv_plant_0" + str(pp_number)]
    ] = "PV plant (mono)" + str(pp_number)
    logging.info(
        "The file_name of the time series of pv_plant_0%s" % pp_number
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
