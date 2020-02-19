
#import feedinlib.era5 as era
import pv_feedin
import pandas as pd
import logging
import sys
import era5

# Reconfiguring the logger here will also affect test running in the PyCharm IDE
log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)

def main(lat, lon, year, population, input_directory=None, output_directory=None,
         mvs_input_directory=None):

    """
    loads weather data for the given year and location, calculates pv feedin
    timeseries as well as the nominal values /installation capacities based on
    the building parameters.

    :param lat: num
    :param lon: num
    :param year: str
    :return:
    """

    weather= era5.load_era5_weatherdata(lat=lat, lon=lon, year=year)

    pv_feedin.create_pv_components(lat=40.3, lon=5.4, weather=weather,
                                   population=population,
                                   PV_setup=None, plot=True,
                                   input_directory=input_directory,
                                   output_directory=None)




if __name__ == '__main__':

    latitude=40.3
    longitude=5.4
    year=2015
    population=48000
    main(lat=latitude, lon=longitude, year=2015, population=population)