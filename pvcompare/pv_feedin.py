from pvlib.location import Location
import pvlib.atmosphere
from pvlib.pvsystem import PVSystem
from pvlib.modelchain import ModelChain
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import pvlib

import pvlib_CPVsystem as cpv
import INS_CPV as ins

"""
This module is designed for the use with the pvlib.

The weather data set has to be a DataFrame with the following columns:

pvlib:
 * ghi - global horizontal irradiation [W/m2]
 * dni - direct normal irradiation [W/m2]
 * dhi - diffuse horizontal irradiation [W/m2]
 * temp_air - ambient temperature [°C]
 * wind_speed - wind speed [m/s]
"""





def create_PV_timeseries(lat, lon, weather, PV_setup=None, plot=True):

    """For each building surface listed in PV_setup, one PV timeseries is
    created with regard to the technology and its orientation used on this
    building surface. All timeseries are normalized to the peak power of the
    module unsed and stored as csv files in ./Data/...

    Parameters
    ----------
    lat: float
        latitude
    lon: float
        longitude
    PV_setup: dict
        with collumns: technology, surface_azimuth, surface_tilt
        a tilt of 0 resembles a vertical orientation.
    plot: boolean

    Returns
    -------
    None
    """

    if PV_setup is None:
        # read example PV_setup file
        datapath = os.path.join(os.path.dirname(__file__),
                                'Data/PV/PV_setup.csv')
        PV_setup=pd.read_csv(datapath)

    technologies = PV_setup["technology"]

    for i in set(technologies):
        orientations= PV_setup.loc[(PV_setup["technology"] == i)]
        surface_azimuth=orientations['surface_azimuth']
        surface_tilt = orientations['surface_tilt']
        surface_tilt = pd.to_numeric(surface_tilt, errors='ignore')

        if i == "si":
            for i, row in orientations.iterrows():
                j = row['surface_azimuth']
                k = row['surface_tilt']
                k=pd.to_numeric(k, errors='ignore')
                if k == "optimal":
                    k=get_optimal_pv_angle(lat)

                timeseries=create_normalized_SI_timeseries(lat=lat, lon=lon, weather=weather, surface_azimuth=j, surface_tilt=k)
                timeseries.to_csv('Data/PV_feedin_SI_' + str(j) + '_' + str(k) + '.csv')

                if plot==True:
                    plt.plot(timeseries, label='si'+ str(j) + '_' + str(k))
                    plt.legend()

        elif i == "cpv":
            for i, row in orientations.iterrows():
                j = row['surface_azimuth']
                k = row['surface_tilt']
                k = pd.to_numeric(k, errors='ignore')
                if k == "optimal":
                    k=get_optimal_pv_angle(lat)
                timeseries=create_normalized_CPV_timeseries(lat, lon, weather, j, k)
                timeseries.to_csv('Data/PV_feedin_CPV_' + str(j) + '_' + str(k) + '.csv')

                if plot==True:
                    plt.plot(timeseries, label='cpv'+ str(j) + '_' + str(k))
                    plt.legend()

        elif i == "psi":
            for i, row in orientations.iterrows():
                j = row['surface_azimuth']
                k = row['surface_tilt']
                k = pd.to_numeric(k, errors='ignore')
                if k == "optimal":
                    k=get_optimal_pv_angle(lat)
                timeseries=create_normalized_SI_timeseries(lat, lon, weather, j, k)
                timeseries.to_csv('Data/PV_feedin_PSI_' + str(j) + '_' + str(k) + '.csv')

        else:
            print(i, 'is not in technologies. Please chose si, cpv or psi.')

    if plot==True:
        plt.show()

def get_optimal_pv_angle(lat):
    """ About 27° to 34° from ground in Germany.
    The pvlib uses tilt angles horizontal=90° and up=0°. Therefore 90° minus
    the angle from the horizontal.
    """
    return round(lat - 15)


def set_up_system(type, surface_azimuth, surface_tilt):

    """Sets up the PV system for the given type of technology and returns
    the initialized system and the module parameters as a dictionary.

    Parameters
    ----------
    type: str
        possible technologies are: PV, CPV or PSI
    surface_azimuth: : float
        surface azimuth of the modules
    surface_tilt: : float
        surface tilt of the modules

    Returns
    -------
    PVSystem, pandas.Series
    """

    if type=="si":

        sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
        sandia_module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
        cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
        cec_inverter = cec_inverters[
            'ABB__MICRO_0_25_I_OUTD_US_208_208V__CEC_2014_']
        system = PVSystem(surface_tilt=surface_tilt,
                          surface_azimuth=surface_azimuth,
                          module_parameters=sandia_module,
                          inverter_parameters=cec_inverter)

        return system, sandia_module

    if type=='cpv':

        module_params = {'gamma_ref': 5.524, 'mu_gamma': 0.003,
                         'I_L_ref': 0.96,
                         'I_o_ref': 0.00000000017, 'R_sh_ref': 5226,
                         'R_sh_0': 21000, 'R_sh_exp': 5.50, 'R_s': 0.01,
                         'alpha_sc': 0.00, 'EgRef': 3.91, 'irrad_ref': 1000,
                         'temp_ref': 25, 'cells_in_series': 12, 'eta_m': 0.32,
                         'alpha_absorption': 0.9, 'Area':0.0001, 'Impo':8.3,
                         'Vmpo':43.9}

        cpv_sys = cpv.StaticCPVSystem(surface_tilt=30, surface_azimuth=180,
                                      module=None,
                                      module_parameters=module_params,
                                      modules_per_string=1,
                                      strings_per_inverter=1,
                                      inverter=None, inverter_parameters=None,
                                      racking_model='insulated',
                                      losses_parameters=None, name=None)

        return cpv_sys, module_params

    if type=='PSI':
        pass

    else:
        print(type, 'is not in technologies. Please chose si, cpv or psi.')


def create_normalized_SI_timeseries(lat, lon, weather, surface_azimuth, surface_tilt):

    """The cpv timeseries is created for a given weather dataframe, at a given
    orientation for the flat plate module "'Canadian_Solar_CS5P_220M___2009_'".
     The time series is normalized by the peak power of the module.

    Parameters
    ----------
    lat: float
        latitude
    lon: float
        longitude
    weather: pd.DataFrame
    surface_azimuth: float
        surface azimuth of the modules
    surface_tilt: float
        surface tilt of the modules

    Returns
    -------
    pd.DataFrame
    """

    system, module_parameters=set_up_system(type="si",
                                            surface_azimuth=surface_azimuth,
                                            surface_tilt=surface_tilt)
    location=Location(latitude=lat, longitude=lon)

    peak = module_parameters['Impo'] * module_parameters['Vmpo']

    mc = ModelChain(system, location, orientation_strategy=None, aoi_model='sapm', spectral_model='sapm')
    mc.run_model(times=weather.index, weather=weather)
    output=mc.dc
    return (output['p_mp']/peak).clip(0)


def create_normalized_CPV_timeseries(lat, lon, weather, surface_azimuth, surface_tilt):

    """The cpv timeseries is created for a given weather dataframe, at a given
    orientation for the INSOLIGHT CPV module. The time series is normalized by
    the peak power of the module.

    Parameters
    ----------
    lat: float
        latitude
    lon: float
        longitude
    weather: pd.DataFrame
    surface_azimuth: float
        surface azimuth of the modules
    surface_tilt: float
        surface tilt of the modules

    Returns
    -------
    pd.DataFrame
    """
    system, module_parameters=set_up_system(type="cpv",
                                            surface_azimuth=surface_azimuth,
                                            surface_tilt=surface_tilt)

    peak = module_parameters['Impo'] * module_parameters['Vmpo']
    return (ins.create_cpv_timeseries(lat, lon, weather, surface_azimuth, surface_tilt,
                          system)/peak).clip(0)

#def create_PSI_timeseries(lat, lon, weather, surface_azimuth, surface_tilt):


def nominal_values_PV(type, area, surface_azimuth, surface_tilt):

    """The nominal value for each PV technology is constructed by the size of
    the module,its peak power and the total available area. The nominal value
    functions as a limit for the potential installed capacity of pv in oemof.

    Parameters
    ----------
    type: str
        possible values are: PV, CPV or PSI
    area: float
        total available surface area
    surface_azimuth: float
        surface azimuth of the modules
    surface_tilt: float
        surface tilt of the modules

    Returns
    -------
    int
        the rounded possible installed capacity for an area
    """

    system, module_parameters = set_up_system(type=type,
                                              surface_azimuth=surface_azimuth,
                                              surface_tilt=surface_tilt)

    peak=module_parameters['Impo']*module_parameters['Vmpo']
    module_size= module_parameters['Area']

    return round(area/module_size*peak)




if __name__ == '__main__':

    filename = os.path.abspath(
        "/home/local/RL-INSTITUT/inia.steinbach/rl-institut/04_Projekte/163_Open_FRED/03-Projektinhalte/AP2 Wetterdaten/open_FRED_TestWetterdaten_csv/fred_data_test_2016.csv")
    weather_df = pd.read_csv(filename, skiprows=range(1, 50), nrows=(5000),
                             index_col=0,
                             date_parser=lambda idx: pd.to_datetime(idx,
                                                                    utc=True))
    weather_df.index = pd.to_datetime(weather_df.index).tz_convert(
        'Europe/Berlin')

    create_PV_timeseries(lat=40.3, lon=5.4, weather=weather_df, PV_setup=None)

    nominal_value_PV=calculate_nominal_values(type='PV', area=1323, surface_azimuth=180, surface_tilt='optimal')

    nominal_value_CPV = calculate_nominal_values(type='CPV', area=1323,
                                             surface_azimuth=180,
                                             surface_tilt='optimal')
