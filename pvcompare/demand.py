# -*- coding: utf-8 -*-
"""
Creating demand profiles.
The heat demand uses bdew profiles.

Installation requirements
-------------------------
This example requires at least version v0.1.4 of the oemof demandlib. Install
by:
    pip install 'demandlib>=0.1.4,<0.2'
Optional:
    pip install matplotlib

"""

import demandlib.bdew as bdew
import demandlib.particular_profiles as profiles
import os
import sys
import pandas as pd
import logging
import numpy as np
log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
import workalendar
try:
    from workalendar.europe import Germany
except ImportError:
    workalendar=None
import inspect
from pkgutil import iter_modules
from importlib import import_module
import datetime

def calculate_load_profiles(country, population, year, input_directory,
                           mvs_input_directory, plot):
    """
    calculate electricity and heat load profiles and saves them to csv
    :param country:
    :param population:
    :param year:
    :param input_directory:
    :param mvs_input_directory:
    :param plot:
    :return:
    """
    calculate_power_demand(country, population, year, input_directory,
                           mvs_input_directory, plot)
    calculate_heat_demand(country, population, year, weather, plot,
                          input_directory, mvs_input_directory)


def calculate_power_demand(country, population, year, input_directory,
                           mvs_input_directory, plot):

    """
    The electricity demand is calculated for a given population in a certain
    country and year. The annual electricity demand is calculated by the
    following procedure:
    1) the residential electricity consumption for a country is requested from
        https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use
    2) the population of the country is requested from
        EUROSTAT_population
    3) the total residential demand is divided by the countries' population and
        multiplied by the districts' population
    4) The load profile is shifted due to country specific behaviour

    Parameters
    ----------
    country: str
        the countries name has to be in english and with capital first letter
    population: int
        the district population
    year: int
        Year for which power demand time series is calculated.
    Returns
    -------
    pd.DataFrame
        hourly time series of the electrical demand
    """
    logging.info("loading calender for %s" %country)
    cal=get_workalendar_class(country)
    holidays = dict(cal.holidays(int(year)))

    logging.info("loading residential electricity demand")
    if input_directory is None:
        input_directory = os.path.join(os.path.dirname(__file__),
                                       'data/inputs/')

    bp= pd.read_csv(os.path.join(input_directory, "building_parameters.csv"),
                    index_col=0)

    filename_residential_electricity_demand=\
        bp.at['filename_residential_electricity_demand', 'value']
    filename_population=bp.at['filename_country_population', 'value']

    filename_elec=os.path.join(os.path.dirname(__file__), input_directory,
                               filename_residential_electricity_demand)
    powerstat= pd.read_csv(filename_elec, sep=';', index_col=0)

    filename1=os.path.join(input_directory, filename_population)
    populations=pd.read_csv(filename1, index_col=0, sep=';')
    national_energyconsumption=powerstat.at[country, year] * 11.63 * 1000000
    annual_demand_per_population=(national_energyconsumption /
                                  populations.at[country, 'Population']) * \
                                 population

    logging.info("The annual demand for a population of %s" %population +
                 " for the year %s " %year + "is %s"
                 %annual_demand_per_population)

    ann_el_demand_h0 = {'h0': annual_demand_per_population}

    # read standard load profiles
    e_slp = bdew.ElecSlp(int(year), holidays=holidays)

    # multiply given annual demand with timeseries
    elec_demand = e_slp.get_profile(ann_el_demand_h0)
    # Add the slp for the industrial group
    ilp = profiles.IndustrialLoadProfile(e_slp.date_time_index,
                                         holidays=holidays)

    # Change scaling factors
    elec_demand['h0'] = ilp.simple_profile(
        ann_el_demand_h0['h0'],
        profile_factors={'week': {'day': 1.0, 'night': 0.8},
                         'weekend': {'day': 0.8, 'night': 0.6}})

    # Resample 15-minute values to hourly values.
    elec_demand = elec_demand.resample('H').mean()

    shifted_elec_demand=shift_working_hours(country=country, ts=elec_demand)

    logging.info("The electrical load profile is completly calculated and "
                 "being saved under %s." % mvs_input_directory)
    filename=os.path.join(mvs_input_directory,'electricity_load_profile.csv')
    shifted_elec_demand.to_csv(filename)

    if plot is True:
        # Plot demand
        ax = shifted_elec_demand.plot()
        ax.set_xlabel("Date")
        ax.set_ylabel("Power demand")
        plt.show()


def calculate_heat_demand(country, population, year, weather, plot,
                          input_directory, mvs_input_directory):
    """
    The heat demand is calculated for a given population in a certain country
    and year. The annual heat demand is calculated by the following procedure:
    1) the residential heat demand for a country is requested from
        https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use
    2) the population of the country is requested from
        EUROSTAT_population
    3) the total residential demand is devided by the countries population and
        multiplied by the districts population
    4) The load profile is shifted due to country specific behaviour

    Parameters
    ----------
    country: str
        the countries name has to be in english and with capital first letter
    population: int
        the district population
    year: int
        Year for which heat demand time series is calculated.

    Returns
    -------
    pd.DataFrame
        hourly time series of the heat demand
    """

    # load workelendar for country
    cal=get_workalendar_class(country)
    holidays = dict(cal.holidays(int(year)))

    # define temperature
    temp = weather['temp_air']

    # Create DataFrame for demand timeseries
    demand = pd.DataFrame(
        index=pd.date_range(pd.datetime(int(year), 1, 1, 0),
                            periods=temp.count(), freq='H'))

    # calculate annual demand
    if input_directory is None:
        input_directory = os.path.join(os.path.dirname(__file__),
                                       'data/inputs/')

    bp = pd.read_csv(os.path.join(input_directory, "building_parameters.csv"),
                    index_col=0)
    filename_residential_gas_demand=bp.at['filename_residential_gas_demand',
                                          'value']
    path_to_gas_demand=os.path.join(input_directory,
                                    filename_residential_gas_demand)
    gas_demand = pd.read_csv(path_to_gas_demand, sep=';',
                            index_col=0, header=1)
    gas_demand[year] = pd.to_numeric(gas_demand[year], errors='coerce')

    filename_population=bp.at['filename_country_population', 'value']
    filename1 = os.path.join(input_directory, filename_population)
    populations = pd.read_csv(filename1, index_col=0, sep=';')

    total_heat_demand=(gas_demand.at[country, year] * 11.63 * 1000000)
    annual_heat_demand_per_population=(total_heat_demand/populations.at[
        country, 'Population']) * population


    # Multi family house (mfh: Mehrfamilienhaus)
    demand['h0'] = bdew.HeatBuilding(
        demand.index, holidays=holidays, temperature=temp,
        shlp_type='MFH',
        building_class=2, wind_class=0,
        annual_heat_demand=annual_heat_demand_per_population,
        name='MFH').get_bdew_profile()

    shifted_demand=shift_working_hours(country=country, ts=demand)

    logging.info("The electrical load profile is completly calculated and "
                 "being saved under %s." % mvs_input_directory)
    shifted_demand.to_csv(os.path.join(mvs_input_directory,
                                          'heat_load_profile.csv'))

    if plot is not None:
        # Plot demand of building
        ax = demand.plot()
        ax.set_xlabel("Date")
        ax.set_ylabel("Heat demand in kW")
        plt.show()
    else:
        print('Annual consumption: \n{}'.format(demand.sum()))


def shift_working_hours(country, ts):

    """
    Since the energy demand for domnestic hot water depends strongly on
    behaviour, the demand profile is adjusted for the different EU countries.
    (see HOTMAPS report p. 127). The Statistic is received from
    (HETUS: http://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/-
    /KS-RA-08-014)

    Parameters
    -----------
    country: str
        name of the country
    ts: pd.DataFrame()
        hourly load profile timeseries

    Returns:
    --------
    ts: pd.DataFrame()
        shifted time series
    """

    if country in ['Bulgaria', 'Croatia', 'Czech Republic', 'Hungary',
                   'Lithuania', 'Poland', 'Slovakia', 'Slovenia', 'Romania']:
        logging.info("The load profile is shifted by -1 hours only on "
                     "weekends.")
        # The timeseries is shifted by -1 hour only on weekends
        ts['Day'] = pd.DatetimeIndex(ts.index).day_name()
        one_weekend = pd.DataFrame()
        for i, row in ts.iterrows():
            if row['Day'] in  ['Saturday', 'Sunday']:
                counter=1
                one_weekend=one_weekend.append(row)
            else:
                if counter==1:
                    one_weekend.h0 = one_weekend.h0.shift(-1)
                    one_weekend.fillna(method='ffill', inplace=True)
                    ts.update(one_weekend)
                    one_weekend = pd.DataFrame()
                    counter=counter+1
                else:
                    pass
        return ts['h0']

    elif country in ['Belgium', 'Estonia', 'Ireland', 'Italy', 'Latvia',
                     'Malta', 'France', 'UK']:
        logging.info("The load profile is shifted by +1 hours.")
        # the timeseries is shifted by one hour
        ts.h0 = ts.h0.shift(1)
        nans=ts[ts.isnull().any(axis=1)]

        for i, row in nans.iterrows():
            newindex=i + pd.DateOffset(hours=24)
            newvalue=ts.loc[str(newindex)]
            return ts.replace(to_replace=np.nan, value=newvalue)

    elif country in ['Cyprus', 'Greece', 'Portugal', 'Spain']:
        logging.info("The load profile is shifted by +2 hours.")
        # the timeseries is shifted by two hours
        ts.h0 = ts.h0.shift(2)
        nans=ts[ts.isnull().any(axis=1)]

        for i, row in nans.iterrows():
            newindex=i + pd.DateOffset(hours=24)
            newvalue=ts.loc[str(newindex)]
            return ts.replace(to_replace=np.nan, value=newvalue)
    else:
        logging.info("The load profile is not shifted.")
        return ts


def get_workalendar_class(country):

    """
    loads workalender for a given country

    :param country: str
        name of the country
    :return: _class()
        class of the country specific workalender
    """
    country_name = country
    for finder, name, ispkg in iter_modules(workalendar.__path__):
        module_name = 'workalendar.{}'.format(name)
        import_module(module_name)
        classes = inspect.getmembers(sys.modules[module_name], inspect.isclass)
        for class_name, _class in classes:
            if _class.__doc__ == country_name:
                return _class()

    return None

if __name__ == '__main__':

    weather= pd.read_csv("/home/local/RL-INSTITUT/inia.steinbach/Dokumente/greco-project/pvcompare/pvcompare/data/ERA5_example_data_pvlib.csv")

    mvs_input_directory = "./data/mvs_inputs/"
#    calculate_power_demand(country='Bulgaria', population=600, year='2011',
#                           input_directory=None, plot=True,
#                           mvs_input_directory=mvs_input_directory)
    calculate_heat_demand(country='Belgium', population=600, year='2011',
                          weather=weather, plot=True, input_directory=None,
                          mvs_input_directory=mvs_input_directory)
