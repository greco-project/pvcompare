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

from pvlib.location import Location
import pvlib.atmosphere
from pvlib.pvsystem import PVSystem
from pvlib.modelchain import ModelChain
import pandas as pd
import os
import pvlib
import glob
import logging

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

import cpvtopvlib.cpvsystem as cpv
import greco_technologies.cpv.hybrid
import greco_technologies.cpv.inputs

#import INS_CPV as ins

def create_pv_timeseries(lat, lon, weather, PV_setup=None, plot=True,
                         input_directory=None, output_directory=None):

    """For each building surface listed in PV_setup, one PV timeseries is
    created with regard to the technology and its orientation used on this
    building surface. All timeseries are normalized to the peak power of the
    module unsed and stored as csv files in ./data/...

    Parameters
    ----------
    lat: float
        latitude
    lon: float
        longitude
    PV_setup: dict
        with collumns: technology, surface_azimuth, surface_tilt
        a tilt of 0 resembles a vertical orientation.
        PV_setup=None loads example file data/pv/PV_setup.csvS
    plot: boolean

    Returns
    -------
    None
    """

    if PV_setup is None:
        # read example PV_setup file
        logging.info("loading pv setup conditions from input directory.")

        if input_directory is None:
            try:
                datapath = os.path.join(os.path.dirname(__file__),
                                'data/inputs/PV_setup.csv')
            except:
                logging.error("input file data/inputs/PV_setup.csv does not "
                              "exist.")
        else:
            try:
                datapath = os.path.join(input_directory,
                                'PV_setup.csv')
            except:
                logging.error("input file %s " % input_directory +
                              "/PV_setup.csv does not exist.")

        PV_setup=pd.read_csv(datapath)
        logging.info("setup conditions successfully loaded.")

    #empty output folder
    if output_directory is None:
        try:
            output_directory=os.path.join(os.path.dirname(__file__),
                                'data/pv/output/')
        except:
            logging.error("default output directory %s" % output_directory +
                          "cannot be found.")

    files = glob.glob(os.path.join(output_directory, "*"))

    for f in files:
        os.remove(f)

    #check if all three required columns are in pv_setup
    if not all([item in PV_setup.columns for item in ['surface_azimuth',
                                                  'surface_tilt',
                                                  'technology']]):
        logging.error("The file PV_setup does not contain all required columns"
                      "surface_azimuth, surface_tilt and technology.")

    # parse through pv_setup file and create timeseries for each technology
    for i, row in PV_setup.iterrows():
        j = row['surface_azimuth']
        k = row['surface_tilt']
        k = pd.to_numeric(k, errors='ignore')
        if k == "optimal":
            k = get_optimal_pv_angle(lat)
        if row["technology"]=="si":
            timeseries = create_normalized_si_timeseries(lat=lat, lon=lon,
                                                         weather=weather,
                                                         surface_azimuth=j,
                                                         surface_tilt=k)
            timeseries.to_csv(
                'data/pv/output/PV_feedin_si_' + str(j) + '_' + str(
                    k) + '.csv')
            logging.info("si timeseries is saved as csv into output "
                         "directory")
            if plot == True:
                     plt.plot(timeseries, label='si'+ str(j) + '_' + str(k),
                              alpha=0.7)
                     plt.legend()

        elif row["technology"]=="cpv":
            timeseries = create_normalized_cpv_timeseries(lat, lon,
                                                          weather,
                                                          j, k)
            timeseries.to_csv(
                'data/pv/output/PV_feedin_cpv_' + str(j) + '_' + str(
                    k) + '.csv')
            logging.info("cpv timeseries is saved as csv into output "
                         "directory")
            if plot == True:
                     plt.plot(timeseries, label='cpv'+ str(j) + '_' + str(k),
                              alpha=0.7)
                     plt.legend()
        elif row["technology"]=="psi":
            logging.error("The timeseries of psi cannot be calculated "
                          "yet. Please only use cpv or si right now.")
        else:
            logging.error(i, 'is not in technologies. Please chose si, '
                             'cpv or psi.')

    if plot==True:
        plt.show()


def get_optimal_pv_angle(lat):
    r"""
    Calculates the optimal tilt angle depending on the latitude.

    About 27° to 34° from ground in Germany.
    The pvlib uses tilt angles horizontal=90° and up=0°. Therefore 90° minus
    the angle from the horizontal.
    """
    return round(lat - 15)


def set_up_system(type, surface_azimuth, surface_tilt):
    r"""
    Sets up the PV system for the given type of technology.

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
    PVSystem: pandas.Series
        Initialized PV system and module parameters.
    """

    if type=="si":

        sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
        sandia_module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
        cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
        cec_inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']
        system = PVSystem(surface_tilt=surface_tilt,
                          surface_azimuth=surface_azimuth,
                          module_parameters=sandia_module,
                          inverter_parameters=cec_inverter)

        return system, sandia_module

    if type=='cpv':

        logging.debug("cpv module parameters are loaded from "
                      "greco_technologies/inputs.py")
        module_params=greco_technologies.cpv.inputs.create_ins_dict()

        cpv_sys = cpv.StaticCPVSystem(surface_tilt=surface_tilt,
                                      surface_azimuth=surface_azimuth,
                                      module=None,
                                      module_parameters=module_params,
                                      modules_per_string=1,
                                      strings_per_inverter=1,
                                      inverter=None, inverter_parameters=None,
                                      racking_model='insulated',
                                      losses_parameters=None, name=None)

        return cpv_sys, module_params

    if type=='psi':
        logging.error('The nominal value for psi cannot be calculated yet.')
        pass

    else:
        logging.warning(type, 'is not in technologies. Please chose si, '
                              'cpv or psi.')


def create_normalized_si_timeseries(lat, lon, weather, surface_azimuth,
                                    surface_tilt, normalized=False):

    r"""The cpv timeseries is created for a given weather dataframe, at a given
    orientation for the flat plate module 'Canadian_Solar_CS5P_220M___2009_'.
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

    mc = ModelChain(system, location, orientation_strategy=None,
                    aoi_model='sapm', spectral_model='sapm')
    mc.run_model(times=weather.index, weather=weather)
    output=mc.dc
    if normalized==True:
        logging.info("normalized si timeseries is calculated.")
        return (output['p_mp']/peak).clip(0)
    else:
        logging.info("si timeseries is calculated without normalization.")
        return output['p_mp']


def create_normalized_cpv_timeseries(lat, lon, weather, surface_azimuth,
                                     surface_tilt, normalized=False):

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
    if normalized==True:
        logging.info("normalized cpv timeseries is calculated.")
        return (greco_technologies.cpv.hybrid.create_hybrid_timeseries(
            lat=lat, lon=lon, weather=weather, surface_tilt=25,
            surface_azimuth=180) / peak).clip(0)
    else:
        logging.info("cpv timeseries is calculated without normalization.")
        return greco_technologies.cpv.hybrid.create_hybrid_timeseries(
            lat=lat, lon=lon, weather=weather,
            surface_tilt=25, surface_azimuth=180)


#def create_PSI_timeseries(lat, lon, weather, surface_azimuth, surface_tilt):


def nominal_values_pv(type, area, surface_azimuth, surface_tilt):
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
    nominal_value=round(area/module_size*peak)
    logging.info('The nominal value of type %s' %type + " for the area of %s"
                 %area +" qm and a surface_azimuth and surface_tilt of %s %s"
                 %surface_azimuth %surface_tilt + " is %s" %nominal_value +
                 " .")
    return nominal_value




if __name__ == '__main__':

    filename = os.path.abspath('/home/local/RL-INSTITUT/inia.steinbach/Dokumente/greco-project/pvcompare/pvcompare/Data/weatherdata.csv')
    weather_df = pd.read_csv(filename, index_col=0,
                             date_parser=lambda idx: pd.to_datetime(idx,
                                                                    utc=True))
    weather_df.index = pd.to_datetime(weather_df.index).tz_convert(
        'Europe/Berlin')
    weather_df['dni']=weather_df['ghi']-weather_df['dhi']

    create_pv_timeseries(lat=40.3, lon=5.4, weather=weather_df, PV_setup=None)

    optimal_tilt=get_optimal_pv_angle(lat=40.3)
    nominal_value_pv=nominal_values_pv(type='si', area=1323,
                                       surface_azimuth=180,
                                       surface_tilt=optimal_tilt)

    nominal_value_cpv = nominal_values_pv(type='cpv', area=1323,
                                          surface_azimuth=180,
                                          surface_tilt=optimal_tilt)

    print('nominal value SI in MW:', nominal_value_pv)
    print('nominal value CPV in MW:', nominal_value_cpv)
