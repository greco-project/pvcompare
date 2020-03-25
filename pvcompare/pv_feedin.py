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
import sys

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

import cpvtopvlib.cpvsystem as cpv
import greco_technologies.cpv.hybrid
import greco_technologies.cpv.inputs
from pvcompare import area_potential

log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)

DEFAULT_INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "data/inputs/")
DEFAULT_MVS_INPUT_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/mvs_inputs/"
)


def create_pv_components(
    lat,
    lon,
    weather,
    population,
    pv_setup=None,
    plot=True,
    input_directory=None,
    mvs_input_directory=None,
    directory_energy_production=None,
    cpv_type='m300'
):
    """
    Reads pv_setup.csv; for each surface_type listed in pv_setup,
    one PV time series is created with regard to the technology and its
    orientation. All time series are normalized to the peak power of the
    module and stored as csv files in ./data/mvs_inputs/time_series.
    Further the area potential of the surface_type with regard to the building
    parameters defined in building_parameters.csv is calculated and the
    maximum installed capacity (nominal value) is calculated. Both parameters
    are stored into ./data/mvs_inputs/elements/csv/energyProduction.csv

    Parameters
    ----------
    lat: float
        latitude
    lon: float
        longitude
    population: num
        population
    pv_setup: dict or None
        with collumns: surface_type, technology, surface_azimuth, surface_tilt
        a tilt of 0 resembles a vertical orientation.
        if pv_setup=None loads example file data/inputs/pv_setup.csv
        # todo If pv_setup is None, it is loaded from the input_directory
    plot: boolean
        if true plots created pv times series
    input_directory: str
        if None: ./data/inputs/
    mvs_input_directory: str
        if None: ./data/mvs_inputs/
    directory_energy_production: str
        if None: ./data/mvs_inputs/elements/csv/

    Returns
    -------
    None
    """

    if pv_setup is None:
        # read example pv_setup file
        logging.info("loading pv setup conditions from input directory.")

        if input_directory is None:
            input_directory = DEFAULT_INPUT_DIRECTORY

        data_path = os.path.join(input_directory, "pv_setup.csv")
        pv_setup = pd.read_csv(data_path)
        logging.info("setup conditions successfully loaded.")

    # empty output folder
    if mvs_input_directory is None:
        mvs_input_directory = DEFAULT_MVS_INPUT_DIRECTORY
    time_series_directory = os.path.join(DEFAULT_MVS_INPUT_DIRECTORY,
                                        "time_series")
    files = glob.glob(os.path.join(time_series_directory, "*"))
    for f in files:
        os.remove(f)

    # check if all required columns are in pv_setup
    if not all(
        [
            item in pv_setup.columns
            for item in [
                "surface_type",
                "surface_azimuth",
                "surface_tilt",
                "technology",
            ]
        ]
    ):
        raise ValueError(
            "The file pv_setup does not contain all required columns"
            "surface_azimuth, surface_tilt and technology."
        )

    # check if mvs_input/energyProduction.csv contains all power plants
    check_mvs_energy_production_file(pv_setup, directory_energy_production)
    # parse through pv_setup file and create time series for each technology
    for i, row in pv_setup.iterrows():
        j = row["surface_azimuth"]
        k = row["surface_tilt"]
        k = pd.to_numeric(k, errors="ignore")
        if k == "optimal":
            k = get_optimal_pv_angle(lat)
        if row["technology"] == "si":
            time_series = create_si_time_series(
                lat=lat, lon=lon, weather=weather, surface_azimuth=j, surface_tilt=k
            )
        elif row["technology"] == "cpv":
            time_series = create_cpv_time_series(lat, lon, weather, j, k,
                                               cpv_type=cpv_type)
        elif row["technology"] == "psi":
            raise ValueError(
                "The time series of psi cannot be calculated "
                "yet. Please only use cpv or si right now."
            )
        else:
            raise ValueError(
                row["technology"],
                "is not in technologies. Please " "choose 'si', 'cpv' or 'psi'.",
            )

        # define the name of the output file of the time series
        ts_csv = f"{row['technology']}_{j}_{k}.csv"
        output_csv = os.path.join(
            time_series_directory,
            ts_csv,
        )

        # add "evaluated_period" to simulation_settings.csv
        add_evaluated_period_to_simulation_settings(
            time_series=time_series,
            mvs_input_directory=mvs_input_directory
        )

        # save time series into mvs_inputs
#        time_series.fillna(0, inplace=True)
        time_series.to_csv(output_csv, header=['kW'], index=False)
        logging.info(
            "%s" % row["technology"] + " time series is saved as csv "
            "into output directory"
        )
        if plot == True:
            plt.plot(
                time_series,
                label=str(row["technology"]) + str(j) + "_" + str(k),
                alpha=0.7,
            )
            plt.legend()

        # calculate area potential
        surface_type_list = [
            "flat_roof",
            "gable_roof",
            "south_facade",
            "east_facade",
            "west_facade",
        ]
        if row["surface_type"] not in surface_type_list:
            raise ValueError(
                "The surface_type in row %s" % i + " in pv_setup.csv"
                " is not valid. Please choose from %s" % surface_type_list
            )
        else:
            area = area_potential.calculate_area_potential(
                population, input_directory, surface_type=row["surface_type"]
            )

        # calculate nominal value of the powerplant
        nominal_value = nominal_values_pv(
            technology=row["technology"], area=area, surface_azimuth=j,
            surface_tilt=k, cpv_type=cpv_type
        )
        # save the file name of the time series and the nominal value to
        # mvs_inputs/elements/csv/energyProduction.csv
        add_parameters_to_energy_production_file(
            pp_number=i + 1, ts_filename=ts_csv, nominal_value=nominal_value,
        )
    if plot == True:
        plt.show()


def get_optimal_pv_angle(lat):

    """
    Calculates the optimal tilt angle depending on the latitude.

    e.G. about 27° to 34° from ground in Germany.
    The pvlib uses tilt angles horizontal=90° and up=0°. Therefore 90° minus
    the angle from the horizontal.
    """
    return round(lat - 15)


def set_up_system(technology, surface_azimuth, surface_tilt, cpv_type):

    """
    Initializes the pvlib.PVSystem for the given type of technology and returns
    the system and the module parameters as a dictionary.


    Parameters
    ----------
    technology: str
        possible technologies are: si, cpv or psi
    surface_azimuth: : float
        surface azimuth of the module
    surface_tilt: : float
        surface tilt of the module

    Returns
    -------
    PVSystem: pandas.Series
        Initialized PV system and module parameters.
    """

    if technology == "si":

        sandia_modules = pvlib.pvsystem.retrieve_sam("SandiaMod")
        sandia_module = sandia_modules["Canadian_Solar_CS5P_220M___2009_"]
        cec_inverters = pvlib.pvsystem.retrieve_sam("cecinverter")
        cec_inverter = cec_inverters["ABB__MICRO_0_25_I_OUTD_US_208__208V_"]
        system = PVSystem(
            surface_tilt=surface_tilt,
            surface_azimuth=surface_azimuth,
            module_parameters=sandia_module,
            inverter_parameters=cec_inverter,
        )

        return system, sandia_module

    elif technology == "cpv":

        logging.debug(
            "cpv module parameters are loaded from " "greco_technologies/inputs.py"
        )
        module_params = greco_technologies.cpv.inputs.create_cpv_dict(
            cpv_type=cpv_type)

        cpv_sys = cpv.StaticCPVSystem(
            surface_tilt=surface_tilt,
            surface_azimuth=surface_azimuth,
            module=None,
            module_parameters=module_params,
            modules_per_string=1,
            strings_per_inverter=1,
            inverter=None,
            inverter_parameters=None,
            racking_model="insulated",
            losses_parameters=None,
            name=None,
        )

        return cpv_sys, module_params

    elif technology == "psi":
        raise ValueError("The nominal value for psi cannot be calculated yet.")
    else:
        logging.warning(
            technology, "is not in technologies. Please chose si, cpv or psi."
        )


def create_si_time_series(lat, lon, weather, surface_azimuth, surface_tilt,
                         normalized=False):
    r"""
    Calculates feed-in time series for a silicon PV module.

    The cpv time series is created for a given weather data frame, at a given
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
    normalized: boolean

    Returns
    -------
    pd.DataFrame
    """

    system, module_parameters = set_up_system(
        technology="si", surface_azimuth=surface_azimuth,
        surface_tilt=surface_tilt, cpv_type=None
    )
    location = Location(latitude=lat, longitude=lon)

    peak = module_parameters["Impo"] * module_parameters["Vmpo"]

    mc = ModelChain(
        system,
        location,
        orientation_strategy=None,
        aoi_model="sapm",
        spectral_model="sapm",
    )
    mc.run_model(times=weather.index, weather=weather)
    output = mc.dc
    if normalized == True:
        logging.info("normalized si time series is calculated.")
        return (output["p_mp"] / peak).clip(0)
    else:
        logging.info("si time series is calculated without normalization.")
        return  output["p_mp"]


def create_cpv_time_series(
    lat, lon, weather, surface_azimuth, surface_tilt, cpv_type, normalized=False,
):
    r"""
    Creates power time series of a CPV module.

    The CPV time series is created for a given weather data frame (`weather`)
    for the INSOLIGHT CPV module. If `normalized` is set to True, the time
    series is divided by the peak power of the module.

    Parameters
    ----------
    lat : float
        Latitude of the location for which the time series is calculated.
    lon : float
        Longitude of the location for which the time series is calculated.
    weather : :pandas:`pandas.DataFrame<frame>`
        DataFrame with time series for temperature `temp_air` in C°, wind speed
        `wind_speed` in m/s,
        # todo etc..
    surface_azimuth : float
        Surface azimuth of the modules (180° for south, 270° for west, etc.).
    surface_tilt: float
        Surface tilt of the modules. #todo example/definition
    cpv_type  : str
        Defines the type of module of which the time series is calculated.
        Options: "ins", "m300".
    normalized: bool
        If True, the time series is divided by the peak power of the CPV
        module. Default: False.

    Returns
    -------
    :pandas:`pandas.Series<series>`
        Power output of CPV module in W (if parameter `normalized` is False) or todo check unit.
        normalized power output of CPV module (if parameter `normalized` is
        False).

    """
    system, module_parameters = set_up_system(
        technology="cpv", surface_azimuth=surface_azimuth,
        surface_tilt=surface_tilt, cpv_type=cpv_type
    )

    peak = module_parameters["i_mp"] * module_parameters["v_mp"]
    if normalized == True:
        logging.info("Normalized CPV time series is calculated.")
        return (
            greco_technologies.cpv.cpv.create_cpv_time_series(
                lat=lat, lon=lon, weather=weather, surface_tilt=surface_tilt,
                surface_azimuth=surface_azimuth, cpv_type=cpv_type
            )
            / peak
        ).clip(0)
    else:
        logging.info("Absolute CPV time series is calculated.")
        return greco_technologies.cpv.cpv.create_cpv_time_series(
            lat=lat, lon=lon, weather=weather, surface_tilt=surface_tilt,
            surface_azimuth=surface_azimuth, cpv_type=cpv_type
        )


# def create_psi_time_series(lat, lon, weather, surface_azimuth, surface_tilt):


def nominal_values_pv(technology, area, surface_azimuth, surface_tilt,
                      cpv_type):

    """
    The nominal value for each PV technology is constructed by the size of
    the module, its peak power and the total available area. The nominal value
    functions as a limit for the potential installed capacity of pv in oemof.

    Parameters
    ----------
    technology: str
        possible values are: si, cpv or psi
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

    system, module_parameters = set_up_system(
        technology=technology,
        surface_azimuth=surface_azimuth,
        surface_tilt=surface_tilt, cpv_type=cpv_type
    )
    if technology == 'si':
        peak = module_parameters["Impo"] * module_parameters["Vmpo"]
    else:
        peak = module_parameters["i_mp"] * module_parameters["v_mp"]
    module_size = module_parameters["Area"]
    nominal_value = round(area / module_size * peak) / 1000
    logging.info(
        "The nominal value for %s" % type  # todo technology instead of type?
        + " is %s" % nominal_value
        + " kWp for an area of %s" % area
        + " qm."
    )
    return nominal_value


def check_mvs_energy_production_file(
    pv_setup, mvs_input_directory=None, overwrite=True
):
    """
    This function compares the number of powerplants in
    data/mvs_inputs/elements/csv/energyProduction.csv with the number of rows
    in pv_setup.csv. If the number differs and overwrite=True, a new
    energyProduction.csv file is created with the correct number of columns and
    default values. The old file is overwritten. If overwrite=False, the
    process throws an error.


    Parameters
    ----------
    pv_setup: dict
    directory_energy_production: str
    overwrite: boolean

    Returns
    ---------
    None
    """

    if mvs_input_directory == None:
        mvs_input_directory = os.path.join(DEFAULT_MVS_INPUT_DIRECTORY)
    energy_production_filename = os.path.join(
        mvs_input_directory, "csv_elements/" "energyProduction.csv"
    )
    if os.path.isfile(energy_production_filename):
        energy_production = pd.read_csv(energy_production_filename, index_col=0)

        if len(energy_production.columns) - 1 == len(pv_setup.index):
            logging.info(
                "mvs_input file energyProduction.csv contains the correct"
                "number of pv powerplants."
            )
        elif overwrite == False:
            raise ValueError(
                "The number of pv powerplants in energyProduction.csv"
                " differs from the number of powerplants listed in "
                "pv_setup.csv. Please check energyProduction.csv or "
                "allow overwrite=True to have energyProduction.csv "
                "set up automatically with default values. "
            )
        else:
            logging.warning(
                "The number of pv powerplants in energyProduction.csv"
                " differs from the number of powerplants listed in "
                "pv_setup.csv. The file energyProduction.csv will thus "
                "be overwritten and created anew with default values."
            )
            create_mvs_energy_production_file(pv_setup, energy_production_filename)

    elif overwrite == False:
        raise ValueError(
            "The file %s" % energy_production_filename + " does not"
            "exist. Please create energyProduction.csv or "
            "allow overwrite=True to have energyProduction.csv "
            "set up automatically with default values."
        )
    else:
        logging.warning(
            "The file %s" % energy_production_filename + "does not"
            "exist. It will thus be created anew with default "
            "values."
        )


def create_mvs_energy_production_file(pv_setup, energy_production_filename):

    """
    creates a new energyProduction.csv file with the correct number of pv
    powerplants as defined in pv_setup.py and saves it into ./data/mvs_inputs/
    csv_elements/csv/energyProduction.csv

    Parameters
    ----------
    pv_setup: dict
    energy_production_filename: str

    Returns
    ---------
    None
    """
    # hardcoded list of parameters
    data = {
        "index": [
            "age_installed",
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
            "energyVector",
        ],
        "unit": [
            "year",
            "currency",
            "currency/unit",
            "str",
            "kWp",
            "str",
            "year",
            "currency/unit/year",
            "currency/kWh",
            "bool",
            "str",
            "str",
            "str",
            "str",
        ],
    }
    df = pd.DataFrame(data, columns=["index", "unit"])
    df.set_index("index", inplace=True)
    for i, row in pv_setup.iterrows():
        # hardcoded default parameters
        pp = [
            "0",
            "10000",
            "7200",
            "0",
            "0",
            "PV plant (mono)",
            "30",
            "80",
            "0",
            "True",
            "PV plant (mono)",
            "source",
            "kWp",
            "Electricity",
        ]
        df["pv_plant_0" + str(i + 1)] = pp

    df.to_csv(energy_production_filename)


def add_parameters_to_energy_production_file(
    pp_number, ts_filename, nominal_value, mvs_input_directory=None
):

    """
    enters the calculated installedCap and file_name parameters of one
    pv-powerplant in energyProduction.csv

    :param pp_number: int
        number of powerplants / columns in pv_setup
    :param ts_filename: str
        file name of the pv time series
    :param nominal_value: float
    :param directory_energy_production: str
    :return: None
    """

    if mvs_input_directory == None:
        mvs_input_directory = DEFAULT_MVS_INPUT_DIRECTORY
    energy_production_filename = os.path.join(
        mvs_input_directory, "csv_elements/energyProduction.csv"
    )
    # load energyProduction.csv
    energy_production = pd.read_csv(energy_production_filename, index_col=0)
    # insert parameter values
    energy_production.loc[
        ["installedCap"], ["pv_plant_0" + str(pp_number)]
    ] = nominal_value
    logging.info(
        "The installed capacity of pv_plant_0%s" % pp_number + " has "
        "been added to energyProduction.csv."
    )
    energy_production.loc[["file_name"], ["pv_plant_0" + str(pp_number)]] = \
        ts_filename
    energy_production.loc[["label"], ["pv_plant_0" + str(pp_number)]] = \
        "PV plant " + str(pp_number)
    logging.info(
        "The file_name of the time series of pv_plant_0%s" % pp_number
        + " has been added to energyProduction.csv."
    )
    # save energyProduction.csv
    energy_production.to_csv(energy_production_filename)


def add_evaluated_period_to_simulation_settings(time_series,
                                                mvs_input_directory):
    """
    count the numer of days in time series and add it into
    simulation_settings.csv

    :param time_series: pd.Dataframe()
        pv time series
    :param mvs_input_directory: str
    :return: none
    """

    if mvs_input_directory == None:
        mvs_input_directory = DEFAULT_MVS_INPUT_DIRECTORY
    simulation_settings_filename = os.path.join(
        mvs_input_directory, "csv_elements/simulation_settings.csv")
    # load simulation_settings.csv
    simulation_settings = pd.read_csv(simulation_settings_filename,
                                      index_col=0)
    length=len(time_series.index)/24
    simulation_settings.loc[
        ["evaluated_period"], ["simulation_settings"]] = int(length)
    simulation_settings.to_csv(simulation_settings_filename)




if __name__ == "__main__":

    filename = os.path.abspath(
        "./data/inputs/weatherdata.csv"
    )
    weather_df = pd.read_csv(
        filename, index_col=0, date_parser=lambda idx: pd.to_datetime(idx, utc=True)
    )
    weather_df.index = pd.to_datetime(weather_df.index).tz_convert("Europe/Berlin")
    weather_df["dni"] = weather_df["ghi"] - weather_df["dhi"]

    create_pv_components(
        lat=40.3, lon=5.4, weather=weather_df, population=600
    )

    # weather_df = pd.DataFrame()
    # weather_df["temp_air"] = [4, 5]
    # weather_df["wind_speed"] = [2, 2.5]
    # weather_df["dhi"] = [100, 120]
    # weather_df["dni"] = [120, 150]
    # weather_df["ghi"] = [200, 220]
    # weather_df.index = ["2014-01-01 13:00:00+00:00",
    #                     "2014-01-01 14:00:00+00:00"]
    # weather_df.index = pd.to_datetime(weather_df.index)
    # weather = weather_df
    #
    # lat = 40.0
    # lon = 5.2
    # surface_azimuth = 180
    # surface_tilt = 30
    #
    # output = create_cpv_time_series(
    #     lat=lat, lon=lon, weather=weather, surface_azimuth=surface_azimuth,
    #     surface_tilt=surface_tilt, normalized=True, cpv_type='m300'
    # )
    # print(output.sum())
    #
    # output=get_optimal_pv_angle(lat=40.0)
    #
    # print(output)