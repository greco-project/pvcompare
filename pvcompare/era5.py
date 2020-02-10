
import feedinlib.era5
import pvlib
import pandas as pd
import numpy as np


def load_era5_weatherdata(lat, lon, year):

    """
    loads era5 weatherdata and converts it into pvlib standart format 
    
    :param lat: numeric
    :param lon: numeric
    :param year: str
    :return: pd.DataFrame
    """

    start_date=str(year)+'-01-01'
    end_date=str(year)+'-12-31'

    weather_xarray=feedinlib.era5.get_era5_data_from_datespan_and_position(
    start_date=start_date,
    end_date=end_date,
    variable="feedinlib",
    latitude=lat,
    longitude=lon,
    grid=None,
    target_file=None,
    chunks=None,
    cds_client=None,
)
    weather_df=format_pvlib(weather_xarray)

    spa=pvlib.solarposition.spa_python(time=weather_df.index, latitude=lat,
                                       longitude=lon)

    weather_df['dni']=pvlib.irradiance.dirint(weather_df['ghi'],
                                              solar_zenith=spa['zenith'],
                                              times=weather_df.index).fillna(0)

    return weather_df


def format_pvlib(ds):
    """
    Format dataset to dataframe as required by the pvlib's ModelChain.

    The pvlib's ModelChain requires a weather DataFrame with time series for

    - wind speed `wind_speed` in m/s,
    - temperature `temp_air` in C,
    - direct irradiation 'dni' in W/m² (calculated later),
    - global horizontal irradiation 'ghi' in W/m²,
    - diffuse horizontal irradiation 'dhi' in W/m²

    Parameters
    ----------
    ds : xarray.Dataset
        Dataset with ERA5 weather data.

    Returns
    --------
    pd.DataFrame
        Dataframe formatted for the pvlib.

    """

    # compute the norm of the wind speed
    ds["wind_speed"] = np.sqrt(ds["u10"] ** 2 + ds["v10"] ** 2).assign_attrs(
        units=ds["u10"].attrs["units"], long_name="10 metre wind speed"
    )

    # convert temperature to Celsius (from Kelvin)
    ds["temp_air"] = ds.t2m - 273.15

    ds["dirhi"] = (ds.fdir / 3600.0).assign_attrs(units="W/m^2")
    ds["ghi"] = (ds.ssrd / 3600.0).assign_attrs(
        units="W/m^2", long_name="global horizontal irradiation"
    )
    ds["dhi"] = (ds.ghi - ds.dirhi).assign_attrs(
        units="W/m^2", long_name="direct irradiation"
    )

    # drop not needed variables
    pvlib_vars = ["ghi", "dhi", "wind_speed", "temp_air"]
    ds_vars = list(ds.variables)
    drop_vars = [
        _
        for _ in ds_vars
        if _ not in pvlib_vars + ["latitude", "longitude", "time"]
    ]
    ds = ds.drop(drop_vars)

    # convert to dataframe
    df = ds.to_dataframe().reset_index()

    # the time stamp given by ERA5 for mean values (probably) corresponds to
    # the end of the valid time interval; the following sets the time stamp
    # to the middle of the valid time interval
    df['time'] = df.time - pd.Timedelta(minutes=30)

    df.set_index(['time'], inplace=True)
    df.sort_index(inplace=True)
    df = df.tz_localize("UTC", level=0)

    df = df[['latitude', 'longitude', "wind_speed", "temp_air", "ghi", "dhi"]]
    df.dropna(inplace=True)

    return df


if __name__ == '__main__':

    latitude=40.3
    longitude=5.4

    df=load_era5_weatherdata(lat=latitude, lon=longitude, year=2015)
