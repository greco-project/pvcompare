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
from pvcompare import check_inputs

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
    country,
    lat,
    lon,
    storeys,
    year,
    weather,
    static_input_directory=None,
    user_input_directory=None,
    mvs_input_directory=None,
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
    static_input_directory: str or None
        Directory of the pvcompare static inputs. If None,
        `constants.DEFAULT_STCATIC_INPUT_DIRECTORY` is used as static_input_directory.
        Default: None.
    user_input_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUT_DIRECTORY` is used as user_input_directory.
        Default: None.
    mvs_input_directory : str or None
        Path to mvs input directory. If None: DEFAULT_MVS_INPUT_DIRECTORY. Default: None.

    Returns
    ------
    None
    """

    if static_input_directory == None:
        static_input_directory = constants.DEFAULT_STATIC_INPUT_DIRECTORY
    if user_input_directory == None:
        user_input_directory = constants.DEFAULT_USER_INPUT_DIRECTORY
    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

    # load eneryConsumption.csv
    energyConsumption = pd.read_csv(
        os.path.join(mvs_input_directory, "csv_elements/energyConsumption.csv"),
        index_col=0,
    )

    for column in energyConsumption:
        if column != "unit":
            if energyConsumption.at["energyVector", column] == "Heat":
                calculate_heat_demand(
                    country=country,
                    lat=lat,
                    lon=lon,
                    storeys=storeys,
                    year=year,
                    weather=weather,
                    static_input_directory=static_input_directory,
                    user_input_directory=user_input_directory,
                    mvs_input_directory=mvs_input_directory,
                    column=column,
                )
            elif energyConsumption.at["energyVector", column] == "Electricity":
                calculate_power_demand(
                    country=country,
                    storeys=storeys,
                    year=year,
                    static_input_directory=static_input_directory,
                    user_input_directory=user_input_directory,
                    mvs_input_directory=mvs_input_directory,
                    column=column,
                )
            else:
                logging.warning(
                    "the given energyVector in energyConsumption.csv "
                    "is not recognized. Please enter either >Heat< "
                    "or >Electricity<"
                )


def calculate_power_demand(
    country,
    storeys,
    year,
    column,
    static_input_directory=None,
    user_input_directory=None,
    mvs_input_directory=None,
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
       multiplied by the districts population that is calulated by the number of
       storeys and the number of people per storey
    4) The load profile is shifted due to country specific behaviour

    [2] https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use

    Parameters
    ----------
    country: str
        The country's name has to be in English and with capital first letter.
    storeys: int
        The number of storeys of the houses.
    year: int
        Year for which power demand time series is calculated. # todo needs to be between 2011 - 2015 like above?
    column: str
        name of the demand column
    weather: pd.DataFrame
        # todo
    user_input_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUT_DIRECTORY` is used as user_input_directory.
        Default: None.
    mvs_input_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_MVS_INPUT_DIRECTORY` is used as mvs_input_directory.
        Default: None.
    mvs_input_directory: str or None
        Path to mvs input directory. If None: DEFAULT_MVS_INPUT_DIRECTORY.  Default: None.

    Returns
    -------
    :pandas:`pandas.Series<series>`
        hourly time series of the electrical demand
    """

    if static_input_directory == None:
        static_input_directory = constants.DEFAULT_STATIC_INPUT_DIRECTORY
    if user_input_directory == None:
        user_input_directory = constants.DEFAULT_USER_INPUT_DIRECTORY
    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

    # load calendar for holidays
    logging.info("loading calender for %s" % country)
    cal = get_workalendar_class(country)
    holidays = dict(cal.holidays(int(year)))

    logging.info("loading residential electricity demand")
    bp = pd.read_csv(
        os.path.join(user_input_directory, "building_parameters.csv"), index_col=0
    )

    filename_residential_electricity_demand = bp.at[
        "filename_residential_electricity_demand", "value"
    ]
    filename_population = bp.at["filename_country_population", "value"]

    population_per_storey = int(bp.at["population per storey", "value"])
    number_of_houses = int(bp.at["number of houses", "value"])
    population = storeys * population_per_storey * number_of_houses

    filename_elec = os.path.join(
        static_input_directory, filename_residential_electricity_demand
    )
    powerstat = pd.read_csv(filename_elec, sep=":", index_col=0, header=1)

    filename1 = os.path.join(static_input_directory, filename_population)
    populations = pd.read_csv(filename1, index_col=0, sep=",")
    # convert mtoe in kWh
    national_energyconsumption = powerstat.at[country, str(year)] * 11630000000
    annual_demand_per_population = (
        national_energyconsumption / populations.at[country, str(year)]
    ) * population

    logging.info(
        "The annual demand for a population of %s" % population
        + " for the year %s " % year
        + "is %s kW" % annual_demand_per_population
    )

    ann_el_demand_h0 = {"h0": annual_demand_per_population}

    # read standard load profiles
    e_slp = bdew.ElecSlp(int(year), holidays=holidays)

    # multiply given annual demand with timeseries
    elec_demand = e_slp.get_profile(ann_el_demand_h0)

    # Resample 15-minute values to hourly values.
    elec_demand = elec_demand.resample("H").mean()

    shifted_elec_demand = shift_working_hours(country=country, ts=elec_demand)
    # rename column "h0" to kWh
    shifted_elec_demand.rename(columns={"h0": "kWh"}, inplace=True)

    timeseries_directory = os.path.join(mvs_input_directory, "time_series/")

    logging.info(
        "The electrical load profile is completly calculated and "
        "being saved under %s." % timeseries_directory
    )

    # define the name of the output file of the time series
    el_demand_csv = f"electricity_load_{year}_{country}_{storeys}.csv"

    filename = os.path.join(timeseries_directory, el_demand_csv)
    shifted_elec_demand.to_csv(filename, index=False)

    # save the file name of the time series and the nominal value to
    # mvs_inputs/elements/csv/energyProduction.csv
    check_inputs.add_file_name_to_energy_consumption_file(
        column=column,
        ts_filename=el_demand_csv,
        mvs_input_directory=mvs_input_directory,
    )

    return shifted_elec_demand


def calculate_heat_demand(
    country,
    lat,
    lon,
    storeys,
    year,
    weather,
    column,
    static_input_directory=None,
    user_input_directory=None,
    mvs_input_directory=None,
):
    """
    Calculates heat demand profile for `storeys` and `country`.

    The heat demand is calculated for a given number of houses with a given number of storeys in a certain country
    and year. The annual heat demand is calculated by the following procedure:

    1) the residential heat demand for a country is requested from [2]
    2) the population of the country is requested from EUROSTAT_population
    3) the total residential demand is devided by the countries population and
       multiplied by the districts population that is calculated by the storeys
       of the house and the number of people in one storey
    4) The load profile is shifted due to countrys specific behaviour

    [2] https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use

    Parameters
    ----------
    country: str
        The country's name has to be in English and with capital first letter.
    storeys: int
        Number of storeys of the houses.
    year: int
        Year for which heat demand time series is calculated. # todo needs to be between 2011 - 2015 like above?
    column: str
        name of the demand
    weather: :pandas:`pandas.DataFrame<frame>`
        weather Data Frame # todo add requirements
    user_input_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUT_DIRECTORY` is used as user_input_directory.
        Default: None.
    mvs_input_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_MVS_INPUT_DIRECTORY` is used as mvs_input_directory.
        Default: None.
    mvs_input_directory: str or None
        Path to mvs input directory. If None: DEFAULT_MVS_INPUT_DIRECTORY.  Default: None.


    Returns
    -------
    shifted_heat_demand : :pandas:`pandas.Series<series>`
        Hourly heat demand time series.
    """

    if static_input_directory == None:
        static_input_directory = constants.DEFAULT_STATIC_INPUT_DIRECTORY
    if user_input_directory == None:
        user_input_directory = constants.DEFAULT_USER_INPUT_DIRECTORY
    if mvs_input_directory == None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY

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
    bp = pd.read_csv(
        os.path.join(user_input_directory, "building_parameters.csv"), index_col=0
    )
    filename_total_SH = os.path.join(
        static_input_directory, bp.at["filename_total_SH", "value"]
    )
    filename_total_WH = os.path.join(
        static_input_directory, bp.at["filename_total_WH", "value"]
    )
    filename_electr_SH = os.path.join(
        static_input_directory, bp.at["filename_elect_SH", "value"]
    )
    filename_electr_WH = os.path.join(
        static_input_directory, bp.at["filename_elect_WH", "value"]
    )
    population_per_storey = int(bp.at["population per storey", "value"])
    number_of_houses = int(bp.at["number of houses", "value"])
    population = storeys * population_per_storey * number_of_houses

    total_SH = pd.read_csv(filename_total_SH, sep=":", index_col=0, header=1)
    total_WH = pd.read_csv(filename_total_WH, sep=":", index_col=0, header=1)
    electr_SH = pd.read_csv(filename_electr_SH, sep=":", index_col=0, header=1)
    electr_WH = pd.read_csv(filename_electr_WH, sep=":", index_col=0, header=1)

    total_SH[str(year)] = pd.to_numeric(total_SH[str(year)], errors="coerce")
    total_WH[str(year)] = pd.to_numeric(total_WH[str(year)], errors="coerce")
    electr_SH[str(year)] = pd.to_numeric(electr_SH[str(year)], errors="coerce")
    electr_WH[str(year)] = pd.to_numeric(electr_WH[str(year)], errors="coerce")
    # load population
    filename_population = bp.at["filename_country_population", "value"]
    filename1 = os.path.join(static_input_directory, filename_population)
    populations = pd.read_csv(filename1, index_col=0, sep=",")

    # convert Mtoe in kWh
    # Heat demand of residential for space heating
    heat_demand = (
        total_SH.at[country, str(year)] - electr_SH.at[country, str(year)]
    ) * 11630000000
    annual_heat_demand_per_population = (
        heat_demand / populations.at[country, str(year)]
    ) * population
    # Heat demand of households for water heating
    heat_demand_ww = (
        total_WH.at[country, str(year)] - electr_WH.at[country, str(year)]
    ) * 11630000000
    annual_heat_demand_ww_per_population = (
        heat_demand_ww / populations.at[country, str(year)]
    ) * population

    # Multi family house (mfh: Mehrfamilienhaus)
    include_warm_water = eval(bp.at["include warm water", "value"])

    # Calculate heat demand only for space heating
    demand["h0"] = bdew.HeatBuilding(
        demand.index,
        holidays=holidays,
        temperature=temp,
        shlp_type="MFH",
        building_class=2,
        wind_class=0,
        annual_heat_demand=annual_heat_demand_per_population,
        name="MFH",
        ww_incl=False,  # This must be False. Warm water calc follows
    ).get_bdew_profile()

    # Read heating limit temperature
    heating_lim_temp = int(bp.at["heating limit temperature", "value"])

    if include_warm_water:
        # Calculate annual heat demand with warm water included
        annual_heat_demand_per_population = (
            annual_heat_demand_per_population + annual_heat_demand_ww_per_population
        )

        # Create a copy of demand dataframe for warm water calculations
        demand_ww_calc = demand.copy()

        # Get total heat demand with warm water
        demand_ww_calc["h0_ww"] = bdew.HeatBuilding(
            demand_ww_calc.index,
            holidays=holidays,
            temperature=temp,
            shlp_type="MFH",
            building_class=2,
            wind_class=0,
            annual_heat_demand=annual_heat_demand_per_population,
            name="MFH",
            ww_incl=True,
        ).get_bdew_profile()

        # Calculate hourly difference in demand between space heating and space heating with warm water
        demand_ww_calc["h0_diff"] = demand_ww_calc["h0_ww"] - demand_ww_calc["h0"]

        # for space heating *only* adjust the heat demand so there is no demand if daily mean temperature
        # is above the heating limit temperature
        demand["h0"] = adjust_heat_demand(temp, heating_lim_temp, demand["h0"])
        # Add the heat demand for warm water to the adjusted space heating demand
        demand["h0"] = demand["h0"] + demand_ww_calc["h0_diff"]

    else:
        # Adjust the heat demand so there is no demand if daily mean temperature
        # is above the heating limit temperature
        demand["h0"] = adjust_heat_demand(temp, heating_lim_temp, demand["h0"])

    shifted_heat_demand = shift_working_hours(country=country, ts=demand)
    shifted_heat_demand.rename(columns={"h0": "kWh"}, inplace=True)

    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    timeseries_directory = os.path.join(mvs_input_directory, "time_series/")

    logging.info(
        "The electrical load profile is completely calculated and "
        "being saved under %s." % timeseries_directory
    )
    # define the name of the output file of the time series
    h_demand_csv = f"heat_load_{year}_{lat}_{lon}_{storeys}.csv"

    filename = os.path.join(timeseries_directory, h_demand_csv)

    shifted_heat_demand.to_csv(filename, index=False)
    # save the file name of the time series and the nominal value to
    # mvs_inputs/elements/csv/energyProduction.csv
    check_inputs.add_file_name_to_energy_consumption_file(
        column=column, ts_filename=h_demand_csv, mvs_input_directory=mvs_input_directory
    )
    return shifted_heat_demand


def adjust_heat_demand(temperature, heating_limit_temp, demand):
    """
    Adjust the hourly heat demand setting a limit to the temperature of heating

    Heat demand above the heating limit temperature is set to zero
    Excess heat demand is then distributed equally over the remaining hourly heat demand

    Parameters
    -----------
    temperature : :pandas:`pandas.Series<series>`
        Ambient temperature data frame
    heating_limit_temp : int
        Temperature limit for heating
    demand : :pandas:`pandas.Series<series>`
        Heat demand from demandlib without limited heating during year

    Returns
    -------
    demand: :pandas:`pandas.Series<series>`
        Hourly heat demand time series with values set to zero above
        the heating limit temperature.
    """
    excess_demand = 0
    # Check for every day in the year the mean temperature
    for i, temp in enumerate(np.arange(0, len(temperature), 24)):
        # Calculate mean temperature of a day
        mean_temp = np.mean(temperature[temp : temp + 24])
        # Check if the daily mean temperature is higher than the heating limit temperature
        if mean_temp >= heating_limit_temp:
            # Gather the previous demand calculated by the demandlib in excess_demand
            excess_demand = excess_demand + sum(demand[temp : temp + 24])
            # Set heat demand to zero
            demand[temp : temp + 24] = 0

    # Count the hours where heat demand is not zero
    count_demand_hours = np.count_nonzero(demand)
    # Calculate heat demand that is shifted from excess demand equally to rest of demand
    hourly_excess_demand = excess_demand / count_demand_hours

    # Add hourly excess demand to heat demand that is not zero
    for i, heat_demand in enumerate(demand):
        if heat_demand != 0:
            demand[i] = demand[i] + hourly_excess_demand

    return demand


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
