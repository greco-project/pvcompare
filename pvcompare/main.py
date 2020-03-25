# import feedinlib.era5 as era
import pandas as pd
import logging
import sys
import pvlib
from pvcompare import era5
from pvcompare import demand
from pvcompare import pv_feedin
import mvs_tool as mvs
import os

DEFAULT_INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "data/inputs/")
DEFAULT_MVS_INPUT_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/mvs_inputs"
)
DEFAULT_MVS_OUTPUT_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/mvs_outputs"
)

# Reconfiguring the logger here will also affect test running in the PyCharm IDE
log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)


def main(
    lat,
    lon,
    year,
    population,
    country,
    input_directory=None,
    mvs_input_directory=None,
    plot=False,
    mvs_output_directory = None
):

    """
    loads weather data for the given year and location, calculates pv feedin
    timeseries as well as the nominal values /installation capacities based on
    the building parameters.

    :param lat: num
    :param lon: num
    :param year: str
    :return:
    """
    # todo: scpecify country automatically by lat/lon

        #if era5 import works this line can be used
    #weather= era5.load_era5_weatherdata(lat=lat, lon=lon, year=year)

#    otherwise this example weather data for one year (2014) can be used for now
    weather = pd.read_csv("./data/inputs/weatherdata.csv", index_col=0)
    weather.index = pd.to_datetime(weather.index)
    spa = pvlib.solarposition.spa_python(
        time=weather.index, latitude=lat, longitude=lon
    )
    weather["dni"] = pvlib.irradiance.dirint(
        weather["ghi"], solar_zenith=spa["zenith"], times=weather.index
    )

    pv_feedin.create_pv_components(lat=lat, lon=lon,
                                   weather=weather,
                                   population=population,
                                   pv_setup=None,
                                   plot=plot,
                                   input_directory=input_directory,
                                   mvs_input_directory=mvs_input_directory)

    demand.calculate_load_profiles(country=country,
                                   population=population,
                                   year=year,
                                   input_directory=input_directory,
                                   mvs_input_directory=mvs_input_directory,
                                   plot=plot,
                                   weather=weather)

    mvs.main(
        path_input_folder=mvs_input_directory,
        path_output_folder=mvs_output_directory,
        input_type = 'csv',
        overwrite=True,
    )


if __name__ == "__main__":

    latitude = 45.641603
    longitude = 5.875387
    year = 2013  # a year between 2011-2013!!!
    population = 48000
    country = "Spain"

    main(lat=latitude, lon=longitude, year=year, country=country, population=population)
