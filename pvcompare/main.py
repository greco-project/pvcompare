
#import feedinlib.era5 as era
import pv_feedin
import pandas as pd
import logging
import sys
from pvcompare import era5
from pvcompare import demand

# Reconfiguring the logger here will also affect test running in the PyCharm IDE
log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)

def main(lat, lon, year, population, country, input_directory=None, output_directory=None,
         mvs_input_directory=None, plot=True):

    """
    loads weather data for the given year and location, calculates pv feedin
    timeseries as well as the nominal values /installation capacities based on
    the building parameters.

    :param lat: num
    :param lon: num
    :param year: str
    :return:
    """
    #todo: scpecify country automatically by lat/lon

    weather= era5.load_era5_weatherdata(lat=lat, lon=lon, year=year)

    pv_feedin.create_pv_components(lat=lat, lon=lon, weather=weather,
                                   population=population,
                                   PV_setup=None, plot=plot,
                                   input_directory=input_directory,
                                   output_directory=output_directory,
                                   mvs_input_directory=mvs_input_directory)





if __name__ == '__main__':

    latitude=40.3
    longitude=5.4
    year=2015
    population=48000
    country = 'Spain'

    main(lat=latitude, lon=longitude, year=year, country=country,
         population=population)