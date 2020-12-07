# imports
import pandas as pd
import logging
import sys
import os
import pvlib
import multi_vector_simulator.cli as mvs

# import feedinlib.era5 as era

# internal imports
from pvcompare import era5
from pvcompare import demand
from pvcompare import pv_feedin
from pvcompare import constants
from pvcompare import heat_pump_and_chiller
from pvcompare import stratified_thermal_storage
from pvcompare import check_inputs


# Reconfiguring the logger here will also affect test running in the PyCharm IDE
log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)


def main(
    population,
    country=None,
    latitude=None,
    longitude=None,
    year=None,
    input_directory=None,
    mvs_input_directory=None,
    plot=False,
    pv_setup=None,
):
    """
    Runs the main functionalities of pvcompare.

    Loads weather data for the given year and location, calculates pv feed-in time
    series, as well as the nominal values /installation capacities based on the building
    parameters. Additionally, COPs are calculated if a heat pump is added to the energy
    system.

    Parameters
    ----------
    population: int
        Population for which the demand and area potential for PV on buildings is
        calculated.
    country:
        Country of the location. Default: None.
    latitude: float or None
        Latitude of the location. Default: None.
    longitude: float or None
        Longitude of the location. Default: None.
    year: int
        Year of the simulation. Default: None.
    input_directory: str or None
        Directory of the pvcompare specific inputs. If None,
        `constants.DEFAULT_INPUT_DIRECTORY` is used as mvs_input_directory.
        Default: None.
    mvs_input_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_MVS_INPUT_DIRECTORY` is used as mvs_input_directory.
        Default: None.
    plot: bool
        If True, plots of the PV feed-in time series are created in
        :py:func:`~.pv_feedin.create_pv_components`. Default: False.
    pv_setup: dict or None
        Specifies the PV technologies and their installation details used in the
        simulation. The dictionary contains columns: surface_type, technology,
        surface_azimuth, surface_tilt.
        A tilt of 0 resembles a vertical orientation.
        If `pv_setup` is None, it is loaded from the `input_directory/pv_setup.cvs`.
        Default: None.

    Returns
    -------
    Saves calculated time series to `timeseries` folder in `mvs_input_directory` and
    updates csv files in `csv_elements` folder.

    """

    if input_directory == None:
        input_directory = constants.DEFAULT_INPUT_DIRECTORY
    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

    #    if all([latitude, longitude, country, year]) == False:
    check_inputs.add_project_data(
        mvs_input_directory, latitude, longitude, country, year
    )
    check_inputs.add_electricity_price()

    # check if weather data already exists
    weather_file = os.path.join(
        input_directory, f"weatherdata_{latitude}_{longitude}_{year}.csv"
    )
    if os.path.isfile(weather_file):
        weather = pd.read_csv(
            os.path.join(
                input_directory, f"weatherdata_{latitude}_{longitude}_{year}.csv"
            ),
            index_col=0,
        )
    else:
        # if era5 import works this line can be used
        weather = era5.load_era5_weatherdata(lat=latitude, lon=longitude, year=year)
        weather.to_csv(weather_file)
    # add datetimeindex
    weather.index = pd.to_datetime(weather.index)

    pv_feedin.create_pv_components(
        lat=latitude,
        lon=longitude,
        weather=weather,
        population=population,
        pv_setup=pv_setup,
        plot=plot,
        input_directory=input_directory,
        mvs_input_directory=mvs_input_directory,
        year=year,
        normalization="NRWC",
    )

    # add sector coupling in case heat pump or chiller exists in energyConversion.csv
    # note: chiller was not tested, yet.
    heat_pump_and_chiller.add_sector_coupling(
        mvs_input_directory=mvs_input_directory,
        input_directory=input_directory,
        weather=weather,
        lat=latitude,
        lon=longitude,
    )

    demand.calculate_load_profiles(
        country=country,
        population=population,
        year=year,
        input_directory=input_directory,
        mvs_input_directory=mvs_input_directory,
        weather=weather,
    )

    stratified_thermal_storage.add_strat_tes(
        weather=weather,
        lat=latitude,
        lon=longitude,
        storage_csv="storage_02.csv",
        input_directory=input_directory,
        mvs_input_directory=mvs_input_directory,
    )


def apply_mvs(mvs_input_directory=None, mvs_output_directory=None):
    r"""
    Starts the energy system simulation with MVS and stores results.

    Parameters
    ----------
    mvs_input_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_MVS_INPUT_DIRECTORY` is used as mvs_input_directory.
        Default: None.
    mvs_output_directory: str or None
        Directory in which simulation results are stored. If None,
        `constants.DEFAULT_MVS_OUTPUT_DIRECTORY` is used as mvs_input_directory.
        Default: None.

    Returns
    -------
    Stores simulation results in `mvs_output_directory`.

    """
    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    if mvs_output_directory == None:
        mvs_output_directory = constants.DEFAULT_MVS_OUTPUT_DIRECTORY

    mvs.main(
        path_input_folder=mvs_input_directory,
        path_output_folder=mvs_output_directory,
        input_type="csv",
        overwrite=True,
        save_png=True,
    )


if __name__ == "__main__":

    latitude = 52.5243700  # Madrid: 40.416775 # berlin: 52.5243700 oslo: 59.9127300 athens: 37.983810, Paris: 48.864716

    longitude = 13.4105300  # M: -3.703790 # berlin 13.4105300 oslo:10.7460900 	athens: 23.727539, paris: 2.349014
    year = 2014
    population = 48000
    country = "Germany"

    main(
        latitude=latitude,
        longitude=longitude,
        year=year,
        population=population,
        country=country,
        mvs_input_directory="/home/local/RL-INSTITUT/marie-claire.gering/Repositories/pvcompare/pvcompare/data/mvs_inputs_template_sector_coupling/",
    )
apply_mvs(
    mvs_input_directory="/home/local/RL-INSTITUT/marie-claire.gering/Repositories/pvcompare/pvcompare/data/mvs_inputs_template_sector_coupling/",
    mvs_output_directory=None,
)
