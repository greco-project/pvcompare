
#import feedinlib.era5 as era
import pv_feedin
import pandas as pd
import logging

import era5

log = logging.getLogger()

def main(lat, lon, year, input_directory=None, output_directory=None):

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

    pv_feedin.create_pv_timeseries(lat=40.3, lon=5.4, weather=weather,
                                   PV_setup=None, plot=True,
                                   input_directory=input_directory,
                                   output_directory=None)

    optimal_tilt = pv_feedin.get_optimal_pv_angle(lat=40.3)
    nominal_value_pv = pv_feedin.nominal_values_pv(type='si', area=1323,
                                         surface_azimuth=180,
                                         surface_tilt=optimal_tilt)

    nominal_value_cpv = pv_feedin.nominal_values_pv(type='cpv', area=1323,
                                          surface_azimuth=180,
                                          surface_tilt=optimal_tilt)



if __name__ == '__main__':

    latitude=40.3
    longitude=5.4
    year=2015

    main(lat=latitude, lon=longitude, year=2015)