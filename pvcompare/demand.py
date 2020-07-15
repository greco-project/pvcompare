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
import numpy as np
import inspect
from pkgutil import iter_modules
from importlib import import_module
from pvcompare import constants

import logging

log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
import workalendar

try:
    from workalendar.europe import Germany
except ImportError:
    workalendar = None


# todo (nice to have): add function that writes name of demand.csv into energyConsumption.csv


def calculate_load_profiles(
    country, population, year, weather, input_directory=None, mvs_input_directory=None,
):
    """
    Calculates electricity and heat load profiles and saves them to csv.

    Parameters
    ---------
    country: str
        The country's name has to be in English and with capital first letter.
    population: int
        The district population.
    year: int
        Year for which power demand time series is calculated, needs to be between 2011 - 2015.
    weather :
        # todo add
    input_directory: str or None
        Path to input directory of pvcompare. If None: DEFAULT_INPUT_DIRECTORY. Default: None.
    mvs_input_directory : str or None
        Path to mvs input directory. If None: DEFAULT_MVS_INPUT_DIRECTORY. Default: None.

    Returns
    ------
    None
    """

    if input_directory is None:
        input_directory = constants.DEFAULT_INPUT_DIRECTORY
    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

    calculate_power_demand(
        country=country,
        population=population,
        year=year,
        input_directory=input_directory,
        mvs_input_directory=mvs_input_directory,
    )
    calculate_heat_demand(
        country=country,
        population=population,
        year=year,
        weather=weather,
        input_directory=input_directory,
        mvs_input_directory=mvs_input_directory,
    )


def calculate_power_demand(
    country, population, year, input_directory=None, mvs_input_directory=None
):
    """
    Calculates electricity demand profile for `population` and `country`.

    The electricity demand is calculated for a given population in a certain
    country and year. The annual electricity demand is calculated by the
    following procedure:

    1) the residential electricity consumption for a country is requested from
       [2]
    2) the population of the country is requested from EUROSTAT_population
    3) the total residential demand is divided by the countries population and
       multiplied by the districts population
    4) The load profile is shifted due to country specific behaviour

    [2] https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use

    Parameters
    ----------
    country: str
        The country's name has to be in English and with capital first letter.
    population: int
        The district population.
    year: int
        Year for which power demand time series is calculated. # todo needs to be between 2011 - 2015 like above?
    weather: pd.DataFrame
        # todo
    input_directory: str or None
        Path to input directory of pvcompare. If None: DEFAULT_INPUT_DIRECTORY. Default: None.
    mvs_input_directory: str or None
        Path to mvs input directory. If None: DEFAULT_MVS_INPUT_DIRECTORY.  Default: None.

    Returns
    -------
    :pandas:`pandas.Series<series>`
        hourly time series of the electrical demand
    """

    logging.info("loading calender for %s" % country)
    cal = get_workalendar_class(country)
    holidays = dict(cal.holidays(int(year)))

    logging.info("loading residential electricity demand")

    if input_directory is None:
        input_directory = constants.DEFAULT_INPUT_DIRECTORY

    bp = pd.read_csv(
        os.path.join(input_directory, "building_parameters.csv"), index_col=0
    )

    filename_residential_electricity_demand = bp.at[
        "filename_residential_electricity_demand", "value"
    ]
    filename_population = bp.at["filename_country_population", "value"]

    filename_elec = os.path.join(
        input_directory, filename_residential_electricity_demand
    )
    powerstat = pd.read_csv(filename_elec, sep=":", index_col=0, header=1)

    filename1 = os.path.join(input_directory, filename_population)
    populations = pd.read_csv(filename1, index_col=0, sep=",")
    # convert mtoe in kWh
    national_energyconsumption = powerstat.at[country, str(year)] * 11630
    annual_demand_per_population = (
        national_energyconsumption / populations.at[country, str(year)]
    ) * population

    logging.info(
        "The annual demand for a population of %s" % population
        + " for the year %s " % year
        + "is %s Watts" % annual_demand_per_population
    )

    ann_el_demand_h0 = {"h0": annual_demand_per_population}

    # read standard load profiles
    e_slp = bdew.ElecSlp(int(year), holidays=holidays)

    # multiply given annual demand with timeseries
    elec_demand = e_slp.get_profile(ann_el_demand_h0)

    # Resample 15-minute values to hourly values.
    elec_demand = elec_demand.resample("H").mean()

    shifted_elec_demand = shift_working_hours(country=country, ts=elec_demand)

    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    timeseries_directory = os.path.join(mvs_input_directory, "time_series/")

    logging.info(
        "The electrical load profile is completly calculated and "
        "being saved under %s." % timeseries_directory
    )
    filename = os.path.join(timeseries_directory, "electricity_load.csv")
    shifted_elec_demand.to_csv(filename, index=False)

    return shifted_elec_demand


def calculate_heat_demand(
    country, population, year, weather, input_directory=None, mvs_input_directory=None,
):
    """
    Calculates heat demand profile for `population` and `country`.

    The heat demand is calculated for a given population in a certain country
    and year. The annual heat demand is calculated by the following procedure:

    1) the residential heat demand for a country is requested from [2]
    2) the population of the country is requested from EUROSTAT_population
    3) the total residential demand is devided by the countries population and
       multiplied by the districts population
    4) The load profile is shifted due to countrys specific behaviour

    [2] https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use

    Parameters
    ----------
    country: str
        The country's name has to be in English and with capital first letter.
    population: int
        The district population.
    year: int
        Year for which heat demand time series is calculated. # todo needs to be between 2011 - 2015 like above?
    weather: :pandas:`pandas.DataFrame<frame>`
        weather Data Frame # todo add requirements
    input_directory: str or None
        Path to input directory of pvcompare. If None: DEFAULT_INPUT_DIRECTORY. Default: None.
    mvs_input_directory: str or None
        Path to mvs input directory. If None: DEFAULT_MVS_INPUT_DIRECTORY.  Default: None.


    Returns
    -------
    shifted_heat_demand : :pandas:`pandas.Series<series>`
        Hourly heat demand time series.
    """

    # load workelendar for country
    cal = get_workalendar_class(country)
    holidays = dict(cal.holidays(int(year)))

    # define temperature
    temp = weather["temp_air"]

    # Create DataFrame for demand timeseries
    demand = pd.DataFrame(
        index=pd.date_range(
            pd.datetime(int(year), 1, 1, 0), periods=temp.count(), freq="H"
        )
    )

    # calculate annual demand
    # The annual heat consumption is calculated by adding up the total
    # consumption for SH and WH and subtracting the electrical consumption of
    # SH and WH for a country
    if input_directory is None:
        input_directory = constants.DEFAULT_INPUT_DIRECTORY

    bp = pd.read_csv(
        os.path.join(input_directory, "building_parameters.csv"), index_col=0
    )
    filename_total_SH = os.path.join(
        input_directory, bp.at["filename_total_SH", "value"]
    )
    filename_total_WH = os.path.join(
        input_directory, bp.at["filename_total_WH", "value"]
    )
    filename_electr_SH = os.path.join(
        input_directory, bp.at["filename_elect_SH", "value"]
    )
    filename_electr_WH = os.path.join(
        input_directory, bp.at["filename_elect_WH", "value"]
    )

    total_SH = pd.read_csv(filename_total_SH, sep=":", index_col=0, header=1)
    total_WH = pd.read_csv(filename_total_WH, sep=":", index_col=0, header=1)
    electr_SH = pd.read_csv(filename_electr_SH, sep=":", index_col=0, header=1)
    electr_WH = pd.read_csv(filename_electr_WH, sep=":", index_col=0, header=1)

    total_SH[str(year)] = pd.to_numeric(total_SH[str(year)], errors="coerce")
    total_WH[str(year)] = pd.to_numeric(total_WH[str(year)], errors="coerce")
    electr_SH[str(year)] = pd.to_numeric(electr_SH[str(year)], errors="coerce")
    electr_WH[str(year)] = pd.to_numeric(electr_WH[str(year)], errors="coerce")

    filename_population = bp.at["filename_country_population", "value"]
    filename1 = os.path.join(input_directory, filename_population)
    populations = pd.read_csv(filename1, index_col=0, sep=",")
    # convert Mtoe in kWh
    heat_demand = (
        total_SH.at[country, str(year)]
        + total_WH.at[country, str(year)]
        - electr_SH.at[country, str(year)]
        - electr_WH.at[country, str(year)]
    ) * 11630
    annual_heat_demand_per_population = (
        heat_demand / populations.at[country, str(year)]
    ) * population

    # Multi family house (mfh: Mehrfamilienhaus)
    demand["h0"] = bdew.HeatBuilding(
        demand.index,
        holidays=holidays,
        temperature=temp,
        shlp_type="MFH",
        building_class=2,
        wind_class=0,
        annual_heat_demand=annual_heat_demand_per_population,
        name="MFH",
    ).get_bdew_profile()

    shifted_heat_demand = shift_working_hours(country=country, ts=demand)

    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    timeseries_directory = os.path.join(mvs_input_directory, "time_series/")

    logging.info(
        "The electrical load profile is completely calculated and "
        "being saved under %s." % timeseries_directory
    )
    shifted_heat_demand.to_csv(
        os.path.join(timeseries_directory, "heat_load.csv"), index=False
    )
    return shifted_heat_demand


def shift_working_hours(country, ts):
    """
    Shift the demand time series with regard to country's customs.

    Since the energy demand for domestic hot water depends strongly on
    behaviour, the demand profile is adjusted for the different EU countries.
    (see [3] HOTMAPS report p. 127). The statistics are received from [4].

    [3] `Hotmaps <https://www.hotmaps-project.eu/wp-content/uploads/2018/03/D2.3-Hotmaps_for-upload_revised-final_.pdf>`_

    [4] `Eurostat <https://ec.europa.eu/eurostat/web/products-manuals-and-guidelines/-/KS-RA-08-014>`_


    Parameters
    -----------
    country: str
        The country's name has to be in English and with capital first letter.
    ts: :pandas:`pandas.DataFrame<frame>`
        Hourly load profile time series.

    Returns
    -------
    ts: :pandas:`pandas.DataFrame<frame>`
        Shifted time series.

    """

    # check if time series contains more than 24 h
    time0 = ts.index[0]
    time24 = time0 + pd.DateOffset(hours=24)
    if not time24 in ts.index:
        logging.warning(
            "Your demand timeseries does not cover 24h and is "
            "therefore not shifted according to the local "
            "behaviour."
        )
        return ts
    if country in [
        "Bulgaria",
        "Croatia",
        "Czech Republic",
        "Hungary",
        "Lithuania",
        "Poland",
        "Slovakia",
        "Slovenia",
        "Romania",
    ]:
        logging.info("The load profile is shifted by -1 hours only on " "weekends.")
        # The timeseries is shifted by -1 hour only on weekends
        ts["Day"] = pd.DatetimeIndex(ts.index).day_name()
        one_weekend = pd.DataFrame()
        counter = 0
        for i, row in ts.iterrows():
            if row["Day"] in ["Saturday", "Sunday"]:
                counter = 1
                one_weekend = one_weekend.append(row)
            else:
                if counter == 1:
                    one_weekend.h0 = one_weekend.h0.shift(-1)
                    one_weekend.fillna(method="ffill", inplace=True)
                    ts.update(one_weekend)
                    one_weekend = pd.DataFrame()
                    counter = counter + 1
                else:
                    pass
        return ts.drop("Day", axis=1)

    elif country in [
        "Belgium",
        "Estonia",
        "Ireland",
        "Italy",
        "Latvia",
        "Malta",
        "France",
        "UK",
    ]:
        logging.info("The load profile is shifted by +1 hours.")
        # the timeseries is shifted by one hour
        ts.h0 = ts.h0.shift(1)
        nans = ts[ts.isnull().any(axis=1)]

        for i, row in nans.iterrows():
            newindex = i + pd.DateOffset(hours=24)
            newvalue = ts.loc[str(newindex)]
            return ts.replace(to_replace=np.nan, value=newvalue)

    elif country in ["Cyprus", "Greece", "Portugal", "Spain"]:
        logging.info("The load profile is shifted by +2 hours.")
        # the timeseries is shifted by two hours
        ts.h0 = ts.h0.shift(2)
        nans = ts[ts.isnull().any(axis=1)]

        for i, row in nans.iterrows():
            newindex = i + pd.DateOffset(hours=24)
            newvalue = ts.loc[str(newindex)]
            return ts.replace(to_replace=np.nan, value=newvalue)
    else:
        logging.info("The load profile is not shifted.")
        return ts


def get_workalendar_class(country):
    """
    Loads workalender for a given country.

    Parameters
    ---------
    country: str
        name of the country

    Returns
    ------
     str
        class of the country specific workalender
    """
    country_name = country
    for finder, name, ispkg in iter_modules(workalendar.__path__):
        module_name = "workalendar.{}".format(name)
        import_module(module_name)
        classes = inspect.getmembers(sys.modules[module_name], inspect.isclass)
        for class_name, _class in classes:
            if _class.__doc__ == country_name:
                return _class()

    return None


if __name__ == "__main__":

    # weather = pd.read_csv("./data/inputs/weatherdata.csv")
    #
    # mvs_input_directory = "./data/mvs_inputs/"
    # input_directory = "./data/inputs/"
    # #    calculate_power_demand(country='Bulgaria', population=600, year='2011',
    # #                           input_directory=None, plot=True,
    # #                           mvs_input_directory=mvs_input_directory)
    # calculate_load_profiles(
    #     country="Germany",
    #     population=600,
    #     year=2001,
    #     weather=weather,
    #     plot=True,
    #     input_directory=None,
    #     mvs_input_directory=mvs_input_directory,
    # )

    # check_if_country_is_valid(country="Spain", input_directory=input_directory)

    country = "Spain"
    population = 4800
    year = 2014
    input_directory = constants.DEFAULT_INPUT_DIRECTORY
    test_mvs_directory = "../tests/test_data/test_mvs_inputs"

    ts = pd.DataFrame()
    ts["h0"] = [19052, 19052, 14289, 19052, 19052, 14289]
    ts.index = [
        "2014-01-01 13:30:00+00:00",
        "2014-01-01 14:00:00+00:00",
        "2014-01-01 14:30:00+00:00",
        "2014-01-01 15:00:00+00:00",
        "2014-01-01 15:30:00+00:00",
        "2014-01-01 16:00:00+00:00",
    ]
    ts.index = pd.to_datetime(ts.index)

    weather_df = pd.DataFrame()
    weather_df["temp_air"] = [4, 5]
    weather_df["wind_speed"] = [2, 2.5]
    weather_df["dhi"] = [100, 120]
    weather_df["dni"] = [120, 150]
    weather_df["ghi"] = [200, 220]
    weather_df.index = ["2014-01-01 13:00:00+00:00", "2014-01-01 14:00:00+00:00"]
    weather_df.index = pd.to_datetime(weather_df.index)
    weather = weather_df

    d = calculate_heat_demand(
        country=country,
        population=population,
        year=year,
        weather=weather,
        input_directory=input_directory,
        mvs_input_directory=test_mvs_directory,
    )

    print(d.sum().values)

    #
    # output = shift_working_hours(country=country, ts=ts)
    # print(output['h0'].sum())
    #
    # cal=get_workalendar_class(country)
    # print(cal.__class__.__name__)

#    if cal == <workalendar.europe.spain.Spain object at 0x7f8e29b16390>:
#        print(cal.__class__.__name__)
