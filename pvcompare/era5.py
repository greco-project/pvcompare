"""
This module loads ERA5 weather data and preprocesses the data into the correct
format for the pvlib's ModelChain.
"""

import numpy as np
import xarray as xr
import pandas as pd
import logging
import pvlib

from feedinlib.cds_request_tools import get_cds_data_from_datespan_and_position


def load_era5_weatherdata(lat, lon, year):
    r"""
    Loads ERA5 weather data.

    Loads ERA5 weather data and converts it into format required by
    `pvlib <https://pvlib-python.readthedocs.io/en/stable/>`_.
    For these calculations the Climate Data Store (CDS) is retrieved
    with the :py:func:`~.get_era5_data_from_datespan_and_position`
    functionality.

    Parameters
    ----------
    lat: float or int
        Latitude in the range [-90, 90] relative to the
        equator, north corresponds to positive latitude.
    lon: float or int
        Longitude in the range [-180, 180] relative to
        Greenwich Meridian, east relative to the meridian corresponds to
        positive longitude.
    year: str
        Weather data of ERA5 for a specific year.

    Returns
    ---------
    weather_df: :pandas:`pandas.DataFrame<frame>`
        Weather data Dataframe formatted for the pvlib.
    """

    start_date = str(year) + "-01-01"
    end_date = str(year) + "-12-31"

    logging.info("loading ERA5 weather data for the year %s" % year)

    weather_xarray = get_era5_data_from_datespan_and_position(
        start_date=start_date,
        end_date=end_date,
        variable="pvcompare",
        latitude=lat,
        longitude=lon,
        grid=None,
        target_file=None,
        chunks=None,
        cds_client=None,
    )
    logging.info("ERA5 weatherdata successfully loaded.")
    weather_df = format_pvcompare(weather_xarray)

    spa = pvlib.solarposition.spa_python(
        time=weather_df.index, latitude=lat, longitude=lon
    )

    weather_df["dni"] = pvlib.irradiance.dirint(
        weather_df["ghi"], solar_zenith=spa["zenith"], times=weather_df.index
    ).fillna(0)

    weather_df["dhi"] = weather_df["ghi"] - (
        weather_df["dni"] * np.cos(np.deg2rad(spa["zenith"]))
    )

    logging.info("weatherdata successfully converted into pvlib format.")
    return weather_df


def get_era5_data_from_datespan_and_position(
    start_date,
    end_date,
    variable="pvcompare",
    latitude=None,
    longitude=None,
    grid=None,
    target_file=None,
    chunks=None,
    cds_client=None,
):
    r"""
    Send request for ERA5 data to the Climate Data Store (CDS).

    Parameters
    ----------
    variable: str or list of str
        ERA5 variables to download. If you
        want to download all variables necessary to use the 'pvlib', set
        `variable` to 'pvlib'. If you want to download all variables necessary
        to use the 'windpowerlib', set `variable` to 'windpowerlib'.
        To download both variable sets for 'pvlib' and 'windpowerlib',
        set `variable` to 'feedinlib'.
        Default: 'pvcompare'.
    start_date: str
        Start date of the date span in YYYY-MM-DD format.
    end_date: str
        End date of the date span in YYYY-MM-DD format.
    latitude: float
        Latitude in the range [-90, 90] relative to the
        equator, north corresponds to positive latitude.
    longitude: float
        Longitude in the range [-180, 180] relative to
        Greenwich Meridian, east relative to the meridian corresponds to
        positive longitude.
    grid: list of float
        Provide the latitude and longitude grid resolutions in deg.
        It needs to be an integer fraction of 90 deg.
    target_file: str
        Name of the file in which to store downloaded data locally.
    chunks: dict TODO: Description needed
    cds_client: None
        Handle to CDS client. If none is provided, then it is created.

    Returns
    ---------
    get_cds_data_from_datespan_and_position: xarray
        CDS data in an xarray format.
    """

    if variable == "pvcompare":
        variable = ["fdir", "ssrd", "2t", "10u", "10v", "tcwv"]
    elif variable == "pvlib":
        variable = ["fdir", "ssrd", "2t", "10u", "10v"]

    return get_cds_data_from_datespan_and_position(**locals())


def format_pvcompare(ds):
    r"""
    Format weather data to dataframe as required by the pvlib's ModelChain.

    The `pvlib's <https://pvlib-python.readthedocs.io/en/stable/>`_
    :py:func:`~.ModelChain` functionality requires a weather
    DataFrame with time series for wind speed `wind_speed` in m/s,
    temperature `temp_air` in C, direct irradiation 'dni' in W/m²
    (calculated later), global horizontal irradiation 'ghi' in W/m².

    Parameters
    ----------
    ds: xarray.Dataset
        Dataset with ERA5 weather data.

    Returns
    --------
    df: :pandas:`pandas.DataFrame<frame>`
        Dataframe formatted for the pvlib.
    """

    # compute the norm of the wind speed
    ds["wind_speed"] = np.sqrt(ds["u10"] ** 2 + ds["v10"] ** 2).assign_attrs(
        units=ds["u10"].attrs["units"], long_name="10 metre wind speed"
    )

    # convert temperature to Celsius (from Kelvin)
    ds["temp_air"] = ds.t2m - 273.15

    # ds["dirhi"] = (ds.fdir / 3600.0).assign_attrs(units="W/m^2")
    ds["ghi"] = (ds.ssrd / 3600.0).assign_attrs(
        units="W/m^2", long_name="global horizontal irradiation"
    )
    # ds["dhi"] = (ds.ghi - ds.dirhi).assign_attrs(
    #    units="W/m^2", long_name="direct irradiation"
    # )
    ds["precipitable_water"] = (ds.tcwv / 10).assign_attrs(
        units="kg/m^2", long_name="total column water vapour"
    )

    # drop not needed variables
    pvlib_vars = ["ghi", "wind_speed", "temp_air", "precipitable_water"]
    ds_vars = list(ds.variables)
    drop_vars = [
        _ for _ in ds_vars if _ not in pvlib_vars + ["latitude", "longitude", "time"]
    ]
    ds = ds.drop(drop_vars)

    # convert to dataframe
    df = ds.to_dataframe().reset_index()

    # the time stamp given by ERA5 for mean values (probably) corresponds to
    # the end of the valid time interval; the following sets the time stamp
    # to the middle of the valid time interval
    df["time"] = df.time - pd.Timedelta(minutes=30)

    df.set_index(["time"], inplace=True)
    df.sort_index(inplace=True)
    df = df.tz_localize("UTC", level=0)

    df = df[
        [
            "latitude",
            "longitude",
            "ghi",
            "wind_speed",
            "temp_air",
            "precipitable_water",
        ]
    ]
    df.dropna(inplace=True)

    return df


def weather_df_from_era5(era5_netcdf_filename, lib, start=None, end=None):
    r"""
    Converts ERA5 weather data to :pandas:`pandas.DataFrame<frame>`.

    Gets ERA5 weather data from netcdf file and converts it to a pandas
    dataframe as required by the specified lib.
    If the lib is 'pvcompare', weather data is formatted with the
    :py:func:`~.format_pvcompare` functionality.

    Parameters
    -----------
    era5_netcdf_filename : str
        Filename including path of netcdf file containing ERA5 weather data
        for specified time span and area.
    lib: str
        Choose between 'pvcompare' or 'windpowerlib'.
    start : None or anything `pandas.to_datetime` can convert to a timestamp
        Get weather data starting from this date. Defaults to None in which
        case start is set to first time step in the dataset.
    end : None or anything `pandas.to_datetime` can convert to a timestamp
        Get weather data up to this date.
        Defaults to None in which case the end date is set to the last time
        step in the dataset.

    Returns
    -------
    df: :pandas:`pandas.DataFrame<frame>`
        Dataframe with ERA5 weather data in format required by the lib.
    """

    ds = xr.open_dataset(era5_netcdf_filename)

    if lib == "pvcompare":
        df = format_pvcompare(ds)
    else:
        raise ValueError(
            "Unknown value for `lib`. "
            "It must be either 'pvcompare' or 'windpowerlib'."
        )

    # drop latitude and longitude from index in case a single location
    # is given in parameter `area`

    if start is None:
        start = df.index[0]
    if end is None:
        end = df.index[-1]
    return df[start:end]


if __name__ == "__main__":

    latitude = 40.3
    longitude = 5.4

    df = load_era5_weatherdata(lat=latitude, lon=longitude, year=2015)
