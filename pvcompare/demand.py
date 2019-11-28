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
import pandas as pd
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
try:
    from workalendar.europe import Germany
except ImportError:
    workalendar=None


def calculate_power_demand(country, population, year):

    """The electricity demand is calculated for a given population in a certain
    country and year. The annual electricity demand is calculated by the
    following procedure:
    1) the residential electricity consumption for a country is requested from
        https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use
    2) the population of the country is requested from
        EUROSTAT_population
    3) the total residential demand is devided by the countries population and
        multiplied by the districts population

    Parameters
    ----------
    country: str
        the countries name has to be in english and with capital first letter
    population: int
        the district population
    year: int

    Returns
    -------
    pd.DataFrame
        hourly time series of the heat demand
    """
    #load workalender for the given country #todo: import different caleder for
                                            #todo: each country
    cal = Germany()
    holidays = dict(cal.holidays(2010))

    filename=os.path.join(os.path.dirname(__file__), 'Data/load_profiles/Electricity_consumption_residential.csv')
    powerstat= pd.read_csv(filename, sep=';', index_col=0)

    filename1=os.path.join(os.path.dirname(__file__), 'Data/load_profiles/EUROSTAT_population.csv')
    populations=pd.read_csv(filename1, index_col=0, sep=';')
    national_energyconsumption=powerstat.at[country, year] * 11.63 * 1000000
    annual_demand_per_population=(national_energyconsumption / populations.at[country, 'Population']) * population


    ann_el_demand_h0 = {
        'h0': annual_demand_per_population}

    # read standard load profiles
    year= int(year)

    e_slp = bdew.ElecSlp(year, holidays=holidays)

    load_profile_h0=e_slp.create_bdew_load_profiles(dt_index=e_slp.date_time_index, slp_types=['h0'], holidays=None)

    # multiply given annual demand with timeseries
    load_elec_demand=e_slp.all_load_profiles(time_df=e_slp.date_time_index, holidays=None)
    elec_demand = e_slp.get_profile(ann_el_demand_h0)
    ilp = profiles.IndustrialLoadProfile(e_slp.date_time_index,
                                         holidays=holidays)

    # Change scaling factors
    elec_demand['h0'] = ilp.simple_profile(
        ann_el_demand_h0['h0'],
        profile_factors={'week': {'day': 1.0, 'night': 0.8},
                         'weekend': {'day': 0.8, 'night': 0.6}})

    # Resample 15-minute values to hourly values.
    elec_demand = elec_demand.resample('H').mean()
    print("Annual electricity demand:", elec_demand.sum())

    if plt is not None:
        # Plot demand
        ax = elec_demand.plot()
        ax.set_xlabel("Date")
        ax.set_ylabel("Power demand")
        plt.show()

def calculate_heat_demand(country, population, year):


    """The heat demand is calculated for a given population in a certain country
    and year. The annual heat demand is calculated by the following procedure:
    1) the residential heat demand for a country is requested from
        https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use
    2) the population of the country is requested from
        EUROSTAT_population
    3) the total residential demand is devided by the countries population and
        multiplied by the districts population

    Parameters
    ----------
    country: str
        the countries name has to be in english and with capital first letter
    population: int
        the district population
    year: int

    Returns
    -------
    pd.DataFrame
        hourly time series of the heat demand
    """

    cal = Germany()
    holidays = dict(cal.holidays(2010))

    # read example temperature series
    datapath = os.path.join(os.path.dirname(__file__),
                            'Data/load_profiles/example_data.csv')
    temperature = pd.read_csv(datapath)["temperature"]
    # Create DataFrame for 2010
    demand = pd.DataFrame(
        index=pd.date_range(pd.datetime(2010, 1, 1, 0),
                            periods=8760, freq='H'))

    # calculate annual demand
    filename1=os.path.join(os.path.dirname(__file__), 'Data/load_profiles/Coal_consumption_residential.csv')
    filename2=os.path.join(os.path.dirname(__file__), 'Data/load_profiles/Gas_consumption_residential.csv')
    coal_demand= pd.read_csv(filename1, sep=';', index_col=0, header=1)
    gas_demand = pd.read_csv(filename2, sep=';', index_col=0, header=1)
    coal_demand[year] = pd.to_numeric(coal_demand[year], errors='coerce')
    gas_demand[year] = pd.to_numeric(gas_demand[year], errors='coerce')

    filename3=os.path.join(os.path.dirname(__file__), 'Data/load_profiles/EUROSTAT_population.csv')
    populations=pd.read_csv(filename3, index_col=0, sep=';')
    total_heat_demand=(coal_demand.at[country, year] * 11.63 * 1000000) + (gas_demand.at[country, year] * 11.63 * 1000000)
    annual_heat_demand_per_population=(total_heat_demand/populations.at[country, 'Population']) * population


    # Multi family house (mfh: Mehrfamilienhaus)
    demand['mfh in MW/h'] = bdew.HeatBuilding(
        demand.index, holidays=holidays, temperature=temperature,
        shlp_type='MFH',
        building_class=2, wind_class=0, annual_heat_demand=annual_heat_demand_per_population,
        name='MFH').get_bdew_profile()

    if plt is not None:
        # Plot demand of building
        ax = demand.plot()
        ax.set_xlabel("Date")
        ax.set_ylabel("Heat demand in kW")
        plt.show()
    else:
        print('Annual consumption: \n{}'.format(demand.sum()))

if __name__ == '__main__':
    calculate_power_demand(country='Germany', population=600, year='2011')
    calculate_heat_demand(country='Germany', population=600, year='2013')
