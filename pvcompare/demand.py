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


def calculate_load_profiles(
    country,
    lat,
    lon,
    storeys,
    year,
    weather,
    static_inputs_directory=None,
    user_inputs_pvcompare_directory=None,
    user_inputs_mvs_directory=None,
):
    r"""
    Calculates electricity and heat load profiles for `country`, `storeys`, and `year`.

    The electricity and heat load profiles are generated with the help of
    `oemof.demandlib <https://github.com/oemof/demandlib>`_.
    For these calculations the electricity demand is calculated with the
    :py:func:`~.calculate_power_demand` functionality and the heat demand with the
    :py:func:`~.calculate_heat_demand` functionality.

    Parameters
    ---------
    country: str
        The country's name has to be in English and with capital first letter.
    lat : float
        Latitude of country location in 'country'.
    lon : float
        Longitude of country location in 'country'.
    storeys: int
        The number of storeys of a building.
    year: int
        Year for which power demand time series is calculated. Year can be
        chosen between 2008 and 2018.
    weather: :pandas:`pandas.DataFrame<frame>`
        hourly weather data frame with the columns:
        time, latitude, longitude, wind_speed, temp_air, ghi, dhi, dni,
        precipitable_water.
    static_inputs_directory: str or None
        Directory of the pvcompare static inputs. If None,
        `constants.DEFAULT_STATIC_INPUTS_DIRECTORY` is used as static_inputs_directory.
        Default: None.
    user_inputs_pvcompare_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used as user_inputs_pvcompare_directory.
        Default: None.
    user_inputs_mvs_directory : str or None
        Path to mvs input directory. If None: DEFAULT_USER_INPUTS_MVS_DIRECTORY. Default: None.

    Returns
    ------
    None
    """

    if static_inputs_directory == None:
        static_inputs_directory = constants.DEFAULT_STATIC_INPUTS_DIRECTORY
    if user_inputs_pvcompare_directory == None:
        user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
    if user_inputs_mvs_directory is None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY

    # load eneryConsumption.csv
    energyConsumption = pd.read_csv(
        os.path.join(user_inputs_mvs_directory, "csv_elements/energyConsumption.csv"),
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
                    static_inputs_directory=static_inputs_directory,
                    user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
                    user_inputs_mvs_directory=user_inputs_mvs_directory,
                    column=column,
                )
            elif energyConsumption.at["energyVector", column] == "Electricity":
                calculate_power_demand(
                    country=country,
                    storeys=storeys,
                    year=year,
                    static_inputs_directory=static_inputs_directory,
                    user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
                    user_inputs_mvs_directory=user_inputs_mvs_directory,
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
    static_inputs_directory=None,
    user_inputs_pvcompare_directory=None,
    user_inputs_mvs_directory=None,
):
    r"""
    Calculates electricity demand profile for `country`, `storeys`, and `year`.

    For the electricity demand, the BDEW load profile for households (H0) is scaled with
    the annual demand of a certain population.
    For further information regarding the assumptions made for the electricty demand profile
    see `Electricity demand <https://pvcompare.readthedocs.io/en/latest/model_assumptions.html#electricity-demand>`_.
    The electricity demand profile is saved to the folder `time_series` in `user_inputs_mvs_directory`.

    Parameters
    ----------
    country: str
        The country's name has to be in English and with capital first letter.
    storeys: int
        The number of storeys of the buildings.
    year: int
        Year for which power demand time series is calculated.
        Year can be chosen between 2008 and 2018.
    column: str
        name of the demand column
    static_inputs_directory: str or None
        Directory of the static inputs. If None
        `constants.DEFAULT_STATIC_INPUTS_DIRECTORY` is used as static_inputs_directory.
        Default: None.
    user_inputs_pvcompare_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used as user_inputs_pvcompare_directory.
        Default: None.
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
        Default: None.

    Returns
    -------
    shifted_elec_demand: :pandas:`pandas.DataFrame<frame>`
        Hourly time series of the electrical demand.
    """

    if static_inputs_directory == None:
        static_inputs_directory = constants.DEFAULT_STATIC_INPUTS_DIRECTORY
    if user_inputs_pvcompare_directory == None:
        user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY

    # load calendar for holidays
    logging.info("loading calender for %s" % country)
    cal = get_workalendar_class(country)
    holidays = dict(cal.holidays(int(year)))

    logging.info("loading residential electricity demand")
    bp = pd.read_csv(
        os.path.join(user_inputs_pvcompare_directory, "building_parameters.csv"),
        index_col=0,
    )
    # loading total residential electricity demand
    filename_electr_SH = os.path.join(
        static_inputs_directory, bp.at["filename_elect_SH", "value"]
    )
    filename_residential_electricity_demand = bp.at[
        "filename_residential_electricity_demand", "value"
    ]
    filename_elec = os.path.join(
        static_inputs_directory, filename_residential_electricity_demand
    )
    powerstat = pd.read_excel(filename_elec, header=1, index_col=0)

    # loading residential space heating
    electr_SH = pd.read_excel(filename_electr_SH, header=1, index_col=0)

    # loading residential water heating
    filename_electr_WH = os.path.join(
        static_inputs_directory, bp.at["filename_elect_WH", "value"]
    )
    electr_WH = pd.read_excel(filename_electr_WH, header=1, index_col=0)

    # loading residential cooking demand total
    filename_total_cooking = os.path.join(
        static_inputs_directory, bp.at["filename_total_cooking_consumption", "value"]
    )
    filename_electricity_cooking = os.path.join(
        static_inputs_directory,
        bp.at["filename_electricity_cooking_consumption", "value"],
    )

    total_cooking = pd.read_excel(filename_total_cooking, header=1, index_col=0)
    elect_cooking = pd.read_excel(filename_electricity_cooking, header=1, index_col=0)

    # loading population for simulation
    filename_population = bp.at["filename_country_population", "value"]
    population_per_storey = int(bp.at["population per storey", "value"])
    number_of_houses = int(bp.at["number of houses", "value"])
    population = storeys * population_per_storey * number_of_houses

    # loading population of country
    filename1 = os.path.join(static_inputs_directory, filename_population)
    populations = pd.read_csv(filename1, index_col=0, sep=",")

    # calculate annual demand.
    # electricity_consumption = total_electricity_consumption -
    # electricity_consumption_SH - electricity_consumption_WH +
    # (total_consumption_cooking - electricity_consumption_cooking)
    # Convert TWh in kWh
    national_energyconsumption = (
        powerstat.at[country, year]
        - electr_SH.at[country, year]
        - electr_WH.at[country, year]
        + (total_cooking.at[country, year] - elect_cooking.at[country, year])
    ) * 10 ** 9
    annual_demand_per_population = (
        national_energyconsumption / float(populations.at[country, str(year)])
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

    timeseries_directory = os.path.join(user_inputs_mvs_directory, "time_series/")

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
        user_inputs_mvs_directory=user_inputs_mvs_directory,
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
    static_inputs_directory=None,
    user_inputs_pvcompare_directory=None,
    user_inputs_mvs_directory=None,
):
    r"""
    Calculates heat demand profile for `storeys`, `country`, `year`.

    The heat demand of either space heating or space heating and warm water
    is calculated for a given number of houses with a given
    number of storeys in a certain country and year.
    In order to take heat demand from warm water into account the parameter `include warm water`
    in pvcompare’s input file 'building_parameters.csv' is set to `True`.

    For further information regarding the  calculation of the heat demand profile
    see `Heat demand <https://pvcompare.readthedocs.io/en/latest/model_assumptions.html#heat-demand>`_.

    Parameters
    ----------
    country: str
        The country's name has to be in English and with capital first letter.
    storeys: int
        Number of storeys of the houses.
    year: int
        Year for which heat demand time series is calculated. # TODO: needs to be between 2011 - 2015 like above?
    column: str
        name of the demand
    weather: :pandas:`pandas.DataFrame<frame>`
        hourly weather data frame with the columns:
        time, latitude, longitude, wind_speed, temp_air, ghi, dhi, dni,
        precipitable_water.
    user_inputs_pvcompare_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used as user_inputs_pvcompare_directory.
        Default: None.
    user_inputs_mvs_directory: str or None
        Directory of the multi-vector simulation inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
        Default: None.

    Returns
    -------
    shifted_heat_demand : :pandas:`pandas.DataFrame<frame>`
        Hourly heat demand time series.
    """

    if static_inputs_directory == None:
        static_inputs_directory = constants.DEFAULT_STATIC_INPUTS_DIRECTORY
    if user_inputs_pvcompare_directory == None:
        user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY

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
        os.path.join(user_inputs_pvcompare_directory, "building_parameters.csv"),
        index_col=0,
    )
    filename_total_SH = os.path.join(
        static_inputs_directory, bp.at["filename_total_SH", "value"]
    )
    filename_total_WH = os.path.join(
        static_inputs_directory, bp.at["filename_total_WH", "value"]
    )
    population_per_storey = int(bp.at["population per storey", "value"])
    number_of_houses = int(bp.at["number of houses", "value"])
    population = storeys * population_per_storey * number_of_houses

    total_SH = pd.read_excel(filename_total_SH, header=1, index_col=0)
    total_WH = pd.read_excel(filename_total_WH, header=1, index_col=0)

    # load population
    filename_population = bp.at["filename_country_population", "value"]
    filename1 = os.path.join(static_inputs_directory, filename_population)
    populations = pd.read_csv(filename1, index_col=0, sep=",")

    # convert TWh in kWh
    # Heat demand of residential space heating
    heat_demand = total_SH.at[country, year] * 10 ** 9
    annual_heat_demand_per_population = (
        heat_demand / float(populations.at[country, str(year)])
    ) * population
    # Heat demand of residential water heating
    heat_demand_ww = total_WH.at[country, year] * 10 ** 9
    annual_heat_demand_ww_per_population = (
        heat_demand_ww / float(populations.at[country, str(year)])
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

    if user_inputs_mvs_directory is None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    timeseries_directory = os.path.join(user_inputs_mvs_directory, "time_series/")

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
        column=column,
        ts_filename=h_demand_csv,
        user_inputs_mvs_directory=user_inputs_mvs_directory,
    )
    return shifted_heat_demand


def adjust_heat_demand(temperature, heating_limit_temp, demand):
    r"""
    Adjust the hourly heat demands exceeding the heating limit temperature.

    The heat demand above the heating limit temperature is set to zero.
    Excess heat demand is then distributed equally over the remaining hourly heat demand.

    Parameters
    -----------
    temperature : :pandas:`pandas.Series<series>`
        Ambient temperature time series
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
    r"""
    Shift the demand time series `ts`depending `country`.

    Since the energy demand for domestic hot water depends strongly on
    behaviour, the demand profile is adjusted for the different EU countries.
    For further information regarding the hour shifting method
    see HOTMAPS [1]_.
    The statistics are received from Eurostat [2]_.

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

    References
    ----------
    .. [1] Pezzutto S. et al.: "D2.3 WP2 Report –Open Data Set for the EU28". Report, 2019, p.127
    .. [2] Eurostat: "Harmonised European time use surveys". Manuals and Guidelines, 2009
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
    r"""
    Loads workalender for a given country.

    Parameters
    ---------
    country: str
        name of the country

    Returns
    ------
    None
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
