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
    mvs_output_directory=None,
    pv_setup=None,
):

    """
    loads weather data for the given year and location, calculates pv feedin
    timeseries as well as the nominal values /installation capacities based on
    the building parameters.

    :param latitude: num
    :param longitude: num
    :param year: str
    :return:
    """

    if input_directory == None:
        input_directory = constants.DEFAULT_INPUT_DIRECTORY
    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

    if all([latitude, longitude, country, year]) == False:
        check_inputs.add_project_data(
            mvs_input_directory, latitude, longitude, country, year
        )
    check_inputs.add_electricity_price()

    # check if weather data already exists
    weather_file = os.path.join(input_directory, f"weatherdata_{country}_{year}.csv")
    if os.path.isfile(weather_file):
        weather = pd.read_csv(
            os.path.join(input_directory, f"weatherdata_{country}_{year}.csv"),
            index_col=0,
        )
    else:
        # if era5 import works this line can be used
        weather = era5.load_era5_weatherdata(lat=latitude, lon=longitude, year=year)
        weather.to_csv(weather_file)

    #  otherwise this example weather data for one year (2014) can be used for now
    # weather = pd.read_csv("./data/inputs/weatherdata_Germany_2016.csv", index_col=0)
    # weather.index = pd.to_datetime(weather.index)
    # spa = pvlib.solarposition.spa_python(
    #     time=weather.index, latitude=latitude, longitude=longitude
    # )
    # weather["dni"] = pvlib.irradiance.dirint(
    #     weather["ghi"], solar_zenith=spa["zenith"], times=weather.index
    # )

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
        normalized=True,
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


def apply_mvs(mvs_input_directory, mvs_output_directory):

    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    if mvs_output_directory == None:
        mvs_output_directory = constants.DEFAULT_MVS_OUTPUT_DIRECTORY

    mvs.main(
        path_input_folder=mvs_input_directory,
        path_output_folder=mvs_output_directory,
        input_type="csv",
        overwrite=True,
    )


if __name__ == "__main__":

    latitude = 48.864716  # Madrid: 40.416775 # berlin: 52.5243700 oslo: 59.9127300 athens: 37.983810, Paris: 48.864716

    longitude = 2.349014  # M: -3.703790 # berlin 13.4105300 oslo:10.7460900 	athens: 23.727539, paris: 2.349014
    year = 2014
    population = 48000
    country = "France"

    main(
        latitude=latitude,
        longitude=longitude,
        year=year,
        population=population,
        country=country,
    )
apply_mvs(mvs_input_directory=None, mvs_output_directory=None)
