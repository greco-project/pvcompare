# imports
import pandas as pd
import logging
import sys
import os

import multi_vector_simulator.cli as mvs

# internal imports
from pvcompare import era5
from pvcompare import demand
from pvcompare import pv_feedin
from pvcompare import constants
from pvcompare import heat_pump_and_chiller
from pvcompare import check_inputs


# Reconfiguring the logger here will also affect test running in the PyCharm IDE
log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)


def apply_pvcompare(
    storeys,
    country=None,
    latitude=None,
    longitude=None,
    year=None,
    static_inputs_directory=None,
    user_inputs_pvcompare_directory=None,
    user_inputs_mvs_directory=None,
    collections_mvs_inputs_directory=None,
    plot=False,
    pv_setup=None,
    overwrite_grid_costs=True,
    overwrite_pv_parameters=True,
):
    """
    Runs the main functionalities of pvcompare.

    Loads weather data for the given year and location, calculates pv feed-in time
    series, as well as the nominal values /installation capacities based on the building
    parameters. Additionally, COPs are calculated if a heat pump is added to the energy
    system.

    Parameters
    ----------
    storeys: int
        number of storeys for which the demand is calculated.
    country:
        Country of the location. Default: None.
    latitude: float or None
        Latitude of the location. Default: None.
    longitude: float or None
        Longitude of the location. Default: None.
    year: int
        Year of the simulation. Default: None.
    static_inputs_directory: str or None
        Directory of the pvcompare static inputs. If None,
        `constants.DEFAULT_STATIC_INPUTS_DIRECTORY` is used as static_inputs_directory.
        Default: None.
    user_inputs_pvcompare_directory: str or None
        If None, `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used
        as  user_inputs_pvcompare_directory.
        Default: None.
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
        Default: None.
    plot: bool
        If True, plots of the PV feed-in time series are created in
        :py:func:`~.pv_feedin.create_pv_components`. Default: False.
    pv_setup: dict or None
        Specifies the PV technologies and their installation details used in the
        simulation. The dictionary contains columns: surface_type, technology,
        surface_azimuth, surface_tilt.
        A tilt of 0 resembles a vertical orientation.
        If `pv_setup` is None, it is loaded from the `user_inputs_pvcompare_directory/pv_setup.cvs`.
        Default: None.
    overwrite_grid_costs: bool
        Default: True. If True, the energy-price is changed according to the
        country.
    overwrite_pv_parameters: bool
        Default: True. If true, the pv components in energyProduction.csv are
        overwritten with default values from 'data/user_inputs_collection/'
        according to the pv plants defined in 'pv_setup'.

    Returns
    -------
    Saves calculated time series to `timeseries` folder in `user_inputs_mvs_directory and
    updates csv files in `csv_elements` folder.

    """

    if static_inputs_directory == None:
        static_inputs_directory = constants.DEFAULT_STATIC_INPUTS_DIRECTORY
    if user_inputs_pvcompare_directory == None:
        user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY

    # add location and year to project data
    (
        latitude,
        longitude,
        country,
        year,
    ) = check_inputs.add_location_and_year_to_project_data(
        user_inputs_mvs_directory,
        static_inputs_directory,
        latitude,
        longitude,
        country,
        year,
    )
    # add electroicity price specified by country
    if overwrite_grid_costs == True:
        check_inputs.add_electricity_price(
            static_inputs_directory=static_inputs_directory,
            user_inputs_mvs_directory=user_inputs_mvs_directory,
        )

    # check if weather data already exists
    weather_file = os.path.join(
        static_inputs_directory, f"weatherdata_{latitude}_{longitude}_{year}.csv"
    )
    if os.path.isfile(weather_file):
        weather = pd.read_csv(weather_file, index_col=0,)
    else:
        # if era5 import works this line can be used
        weather = era5.load_era5_weatherdata(lat=latitude, lon=longitude, year=year)
        weather.to_csv(weather_file)
    # add datetimeindex
    weather.index = pd.to_datetime(weather.index)

    # check energyProduction.csv file for the correct pv technology
    check_inputs.overwrite_mvs_energy_production_file(
        pv_setup=pv_setup,
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
        collections_mvs_inputs_directory=collections_mvs_inputs_directory,
        overwrite_pv_parameters=overwrite_pv_parameters,
    )
    pv_feedin.create_pv_components(
        lat=latitude,
        lon=longitude,
        weather=weather,
        storeys=storeys,
        pv_setup=pv_setup,
        plot=plot,
        user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        year=year,
        normalization=True,
    )

    # add sector coupling in case heat pump or chiller exists in energyConversion.csv
    # note: chiller was not tested, yet.
    heat_pump_and_chiller.add_sector_coupling(
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
        weather=weather,
        lat=latitude,
        lon=longitude,
    )

    demand.calculate_load_profiles(
        country=country,
        lat=latitude,
        lon=longitude,
        storeys=storeys,
        year=year,
        static_inputs_directory=static_inputs_directory,
        user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
        user_inputs_mvs_directory=user_inputs_mvs_directory,
        weather=weather,
    )


def apply_mvs(
    scenario_name,
    user_inputs_mvs_directory=None,
    outputs_directory=None,
    mvs_output_directory=None,
):
    r"""
    Starts the energy system simulation with MVS and stores results.

    Parameters
    ----------
    scenario_name: str
        Name of the Scenario. The name should follow the scheme:
        "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
        Default: None.
    outputs_directory: str
        Path to output directory.
        Default: constants.DEFAULT_OUTPUTS_DIRECTORY
    mvs_output_directory: str or None
        This parameter should be set to None. It is filled filled in automatically
        according to 'outputs_directory' and 'scenario_name':
        'pvcompare/data/outputs/scenario_name/mvs_output'.
        Default: None.

    Returns
    -------
    Stores simulation results in `mvs_output_directory`.

    """
    if user_inputs_mvs_directory is None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    if outputs_directory is None:
        outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
    if not os.path.isdir(outputs_directory):
        os.mkdir(outputs_directory)

    scenario_folder = os.path.join(outputs_directory, scenario_name)
    if mvs_output_directory is None:
        mvs_output_directory = os.path.join(scenario_folder, "mvs_outputs")
    # check if output folder exists, if not: create it
    if not os.path.isdir(scenario_folder):
        # create output folder
        os.mkdir(scenario_folder)
    # check if mvs_output_directory already exists. If yes, raise error
    if os.path.isdir(mvs_output_directory):
        raise NameError(
            f"The mvs output directory {mvs_output_directory} "
            f"already exists. Please delete the folder or "
            f"rename 'scenario_name' to create a different scenario "
            f"folder."
        )

    # adapt parameter 'scenario_name' in 'project_data.csv'.
    check_inputs.add_scenario_name_to_project_data(
        user_inputs_mvs_directory, scenario_name
    )

    mvs.main(
        path_input_folder=user_inputs_mvs_directory,
        path_output_folder=mvs_output_directory,
        input_type="csv",
        overwrite=True,
        save_png=True,
    )


if __name__ == "__main__":

    latitude = 52.5243700  # Madrid: 40.416775 # berlin: 52.5243700 oslo: 59.9127300 athens: 37.983810, Paris: 48.864716

    longitude = 13.4105300  # M: -3.703790 # berlin 13.4105300 oslo:10.7460900 	athens: 23.727539, paris: 2.349014
    year = 2017
    storeys = 5
    country = "Germany"
    scenario_name = "Scenario_B2"

    apply_pvcompare(
        latitude=latitude,
        longitude=longitude,
        year=year,
        storeys=storeys,
        country=country,
    )

    apply_mvs(
        scenario_name=scenario_name,
        outputs_directory=None,
        user_inputs_mvs_directory=None,
    )
