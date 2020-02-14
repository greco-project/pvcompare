from pvlib.location import Location
import pvlib.atmosphere
from pvlib.pvsystem import PVSystem
from pvlib.modelchain import ModelChain
import matplotlib.pyplot as plt
import pandas as pd
import os
import pvlib
import glob
import logging
import sys

import cpvtopvlib.cpvsystem as cpv
import greco_technologies.cpv.hybrid
import greco_technologies.cpv.inputs
import area_potential

log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)

#import INS_CPV as ins

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


def create_pv_timeseries(lat, lon, weather, population, PV_setup=None, plot=True,
                         input_directory=None, output_directory=None,
                         mvs_input_directory=None):

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
        PV_setup=None loads example file Data/pv/PV_setup.csvS
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
                input_directory='Data/inputs/'
                datapath = os.path.join(input_directory,'PV_setup.csv')
            except:
                logging.error("input file Data/inputs/PV_setup.csv does not "
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
            output_directory='Data/mvs_inputs/sequences/pv/'
        except:
            logging.error("default output directory %s" % output_directory +
                          "cannot be found.")
    files = glob.glob(os.path.join(output_directory, "*"))

    for f in files:
        os.remove(f)

    #check if all three required columns are in pv_setup
    if not all([item in PV_setup.columns for item in ['type','surface_azimuth',
                                                  'surface_tilt',
                                                  'technology']]):
        logging.error("The file PV_setup does not contain all required columns"
                      "surface_azimuth, surface_tilt and technology.")

    #check if mvs_input/energyProduction.csv contains all powerplants
    check_mvs_energyProduction_file(PV_setup, mvs_input_directory=None)
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
        elif row["technology"]=="cpv":
            timeseries = create_normalized_cpv_timeseries(lat, lon,
                                                          weather,
                                                          j, k)

        elif row["technology"]=="psi":
            logging.error("The timeseries of psi cannot be calculated "
                          "yet. Please only use cpv or si right now.")
        else:
            logging.error(row["technology"], 'is not in technologies. Please '
                                             'chose si, cpv or psi.')
        # define the name of the output file of the timeseries
        output_csv=os.path.join(output_directory, str(row["technology"]) + '_'
                                + str(j) + '_' + str(k) + '.csv')
        # save timeseries into mvs_inputs
        timeseries.to_csv(output_csv)
        logging.info("%s" %row["technology"] + " timeseries is saved as csv "
                                               "into output directory")
        if plot == True:
            plt.plot(timeseries, label=str(row["technology"]) + str(j) + '_'
                                       + str(k),
                     alpha=0.7)
            plt.legend()
        #calculate area potential
        surface_type_list=['flat_roof', 'gable_roof', 'south_facade',
                           'east_facade', 'west_facade']
        if row['surface_type'] not in surface_type_list:
            logging.error("The surface_type in row %s" %i + " in PV_setup.csv"
                          " is not valid. Please choose from %s"
                          %surface_type_list)
        else:
            area=area_potential.calculate_area_potential(population,
                                                         input_directory,
                                 surface_type=row['surface_type'])

        #calculate nominal value of the powerplant
        nominal_value= nominal_values_pv(technology=row["technology"], area=area,
                                         surface_azimuth=j, surface_tilt=k)
        # save the file name of the timeseries and the nominal value to
        # mvs_inputs/elements/csv/energyProduction.csv
        add_pp_column_to_energyProduction_file(pp_number=i+1,
                                               ts_filename=output_csv,
                                               nominal_value=nominal_value, )

    if plot==True:
        plt.show()


def get_optimal_pv_angle(lat):

    """ About 27° to 34° from ground in Germany.
    The pvlib uses tilt angles horizontal=90° and up=0°. Therefore 90° minus
    the angle from the horizontal.
    """
    return round(lat - 15)


def set_up_system(technology, surface_azimuth, surface_tilt):

    """Sets up the PV system for the given type of technology and returns
    the initialized system and the module parameters as a dictionary.

    Parameters
    ----------
    technology: str
        possible technologies are: PV, CPV or PSI
    surface_azimuth: : float
        surface azimuth of the modules
    surface_tilt: : float
        surface tilt of the modules

    Returns
    -------
    PVSystem, pandas.Series
    """

    if technology=="si":

        sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
        sandia_module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
        cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
        cec_inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']
        system = PVSystem(surface_tilt=surface_tilt,
                          surface_azimuth=surface_azimuth,
                          module_parameters=sandia_module,
                          inverter_parameters=cec_inverter)

        return system, sandia_module

    if technology=='cpv':

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

    if technology=='psi':
        logging.error('The nominal value for psi cannot be calculated yet.')
        pass

    else:
        logging.warning(technology, 'is not in technologies. Please chose si, '
                              'cpv or psi.')


def create_normalized_si_timeseries(lat, lon, weather, surface_azimuth,
                                    surface_tilt, normalized=True):

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
    system, module_parameters=set_up_system(technology="si",
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
                                     surface_tilt, normalized=True):

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
    system, module_parameters=set_up_system(technology="cpv",
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


def nominal_values_pv(technology, area, surface_azimuth, surface_tilt):

    """The nominal value for each PV technology is constructed by the size of
    the module,its peak power and the total available area. The nominal value
    functions as a limit for the potential installed capacity of pv in oemof.

    Parameters
    ----------
    technology: str
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

    system, module_parameters = set_up_system(technology=technology,
                                              surface_azimuth=surface_azimuth,
                                              surface_tilt=surface_tilt)

    peak=module_parameters['Impo']*module_parameters['Vmpo']
    module_size= module_parameters['Area']
    nominal_value=round(area/module_size*peak)/1000
    logging.info('The nominal value for %s' %type + " is %s" %nominal_value +
                " kWp for an area of %s" %area + " qm.")
    return nominal_value


def check_mvs_energyProduction_file(PV_setup, mvs_input_directory=None,
                               overwrite=True):
    """
    This function compares the number of powerplants in
    Data/mvs_inputs/elements/csv/energyProduction.csv with the number of rows
    in PV_setup.csv. If the number differs and overwrite=True, a new
    energyProduction.csv file is created with the correct number of columns and
    default values. The old file is overwritten. If overwrite=False, the
    process is aborted.


    :param PV_setup: pd.DataFrame
    :param mvs_input_directory: str
    :param overwrite: boolean
    :return: None
    """



    if mvs_input_directory==None:
        mvs_input_directory= os.path.join(os.path.dirname(__file__),
                                          "Data/mvs_inputs/elements/csv/")
    energyProduction_filename= os.path.join(mvs_input_directory,
                                            "energyProduction.csv")
    if os.path.isfile(energyProduction_filename):
        energyProduction = pd.read_csv(energyProduction_filename, index_col=0)

        if len(energyProduction.columns) - 1 == len(PV_setup.index):
            logging.info(
                "mvs_input file energyProduction.csv contains the correct"
                "number of pv powerplants.")
        elif overwrite == False:
            logging.error(
                "The number of pv powerplants in energyProduction.csv"
                " differs from the number of powerplants listed in "
                "PV_setup.csv. Please check energyProduction.csv or "
                "allow overwrite=True to have energyProduction.csv "
                "set up automatically with default values. ")
        else:
            logging.warning(
                "The number of pv powerplants in energyProduction.csv"
                " differs from the number of powerplants listed in "
                "PV_setup.csv. The file energyProduction.csv will thus "
                "be overwritten and created anew with default values.")
            create_mvs_energyProduction_file(PV_setup, energyProduction_filename)

    elif overwrite==False:
        logging.error("The file %s" %energyProduction_filename + "does not"
                      "exist. Please create energyProduction.csv or "
                      "allow overwrite=True to have energyProduction.csv "
                      "set up automatically with default values.")
    else: logging.warning("The file %s" %energyProduction_filename + "does not"
                          "exist. It will thus be created anew with default "
                          "values.")


def create_mvs_energyProduction_file(PV_setup, energyProduction_filename):

    """
    creates a new energyProduction.csv file with the correct number of pv
    powerplants as defined in PV_setup.py and saves it into mvs_inputs/elements
    /csv/energyProduction.csv

    :param PV_setup: pd.DataFrame()
    :param energyProduction_filename: str
    :return: None
    """

    data = {'index': ["age_installed",
                    "capex_fix",
                    "capex_var",
                    "file_name",
                    "installedCap",
                    "label",
                    "lifetime",
                    "opex_fix",
                    "opex_var",
                    "optimizeCap",
                    "outflow_direction",
                    "type_oemof",
                    "unit",
                    "energyVector"],
            'unit': ['year',
                    'currency',
                    'currency/unit',
                    'str',
                    'kWp',
                    'str',
                    'year',
                    'currency/unit/year',
                    'currency/kWh',
                    'bool',
                    'str',
                    'str',
                    'str',
                    'str',
                    ]}
    df = pd.DataFrame(data, columns=['index', 'unit'])
    df.set_index('index', inplace=True)
    for i, row in PV_setup.iterrows():
        pp=['0',
                '10000',
                '7200',
                '0',
                '0',
                'PV plant (mono)',
                '30',
                '80',
                '0',
                'True',
                'PV plant (mono)',
                'source',
                'kWp',
                'Electricity']
        df['pv_plant_0' + str(i+1)] = pp

    df.to_csv(energyProduction_filename)


def add_pp_column_to_energyProduction_file(pp_number, ts_filename,
                                           nominal_value,
                                           mvs_input_directory=None):

    """
    enters the calculated installedCap and file_name parameters of one
    pv-powerplant in energyProduction.csv

    :param pp_number: int
    :param ts_filename: str
    :param nominal_value: float
    :param mvs_input_directory: str
    :return: None
    """

    if mvs_input_directory==None:
        mvs_input_directory= os.path.join(os.path.dirname(__file__),
                                          "Data/mvs_inputs/elements/csv/")
    energyProduction_filename= os.path.join(mvs_input_directory,
                                            "energyProduction.csv")
    energyProduction = pd.read_csv(energyProduction_filename, index_col=0)

    energyProduction.loc[['installedCap'], ['pv_plant_0' + str(pp_number)]]=\
        nominal_value
    logging.info("The installed capacity of pv_plant_0%s" %pp_number +" has " \
                 "been added to energyProduction.csv.")
    energyProduction.loc[['file_name'], ['pv_plant_0' + str(pp_number)]]=\
        ts_filename
    logging.info("The file_name of the time series of pv_plant_0%s" %pp_number
                 +" has been added to energyProduction.csv.")

    energyProduction.to_csv(energyProduction_filename)







if __name__ == '__main__':

    filename = os.path.abspath('/home/local/RL-INSTITUT/inia.steinbach/Dokumente/greco-project/pvcompare/pvcompare/Data/ERA5_example_data_pvlib.csv')
    weather_df = pd.read_csv(filename, index_col=0,
                             date_parser=lambda idx: pd.to_datetime(idx,
                                                                    utc=True))
    weather_df.index = pd.to_datetime(weather_df.index).tz_convert(
        'Europe/Berlin')
    weather_df['dni']=weather_df['ghi']-weather_df['dhi']

    create_pv_timeseries(lat=40.3, lon=5.4, weather=weather_df, PV_setup=None,
                         population=48000)
    #
    # optimal_tilt=get_optimal_pv_angle(lat=40.3)
    # nominal_value_pv=nominal_values_pv(type='si', area=1323,
    #                                    surface_azimuth=180,
    #                                    surface_tilt=optimal_tilt)
    #
    # nominal_value_cpv = nominal_values_pv(type='cpv', area=1323,
    #                                       surface_azimuth=180,
    #                                       surface_tilt=optimal_tilt)
    #
    # print('nominal value SI in MW:', nominal_value_pv)
    # print('nominal value CPV in MW:', nominal_value_cpv)