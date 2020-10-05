"""
This module is designed for the use with the pvlib.

The weather data set has to be a DataFrame with the following columns:

pvlib:
 * ghi - global horizontal irradiation [W/m2]
 * dni - direct normal irradiation [W/m2]
 * dhi - diffuse horizontal irradiation [W/m2]
 * temp_air - ambient temperature [�C]
 * wind_speed - wind speed [m/s]
"""

from pvlib.location import Location
import pvlib.atmosphere
from pvlib.pvsystem import PVSystem
from pvlib.modelchain import ModelChain
import pandas as pd
import os
import pvlib
import logging
import sys

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

import greco_technologies.cpv.inputs
import greco_technologies.perosi.perosi
from pvcompare import area_potential
from pvcompare import check_inputs
from pvcompare import constants

from cpvlib import cpvlib

from greco_technologies.cpv import apply_cpvlib_StaticHybridSystem

log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)


def create_pv_components(
    lat,
    lon,
    weather,
    population,
    year,
    pv_setup=None,
    plot=True,
    input_directory=None,
    mvs_input_directory=None,
    directory_energy_production=None,
    psi_type="Chen",
):
    """
    creates feedin time series for all surface types in pv_setup.csv

    Reads pv_setup.csv, for each surface_type listed in pv_setup,
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
        if pv_setup is None, it is loaded from the input_directory
    plot: bool
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
            input_directory = constants.DEFAULT_INPUT_DIRECTORY

        data_path = os.path.join(input_directory, "pv_setup.csv")
        pv_setup = pd.read_csv(data_path)
        logging.info("setup conditions successfully loaded.")

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
    check_inputs.check_mvs_energy_production_file(pv_setup, directory_energy_production)

    #  define time series directory
    if mvs_input_directory is None:
        mvs_input_directory = constants.DEFAULT_MVS_INPUT_DIRECTORY
    time_series_directory = os.path.join(mvs_input_directory, "time_series")

    # parse through pv_setup file and create time series for each technology
    for i, row in pv_setup.iterrows():
        j = row["surface_azimuth"]
        k = row["surface_tilt"]
        k = pd.to_numeric(k, errors="ignore")
        if k == "optimal":
            k = get_optimal_pv_angle(lat)

        # check if timeseries already exists
        # define the name of the output file of the time series
        ts_csv = f"{row['technology']}_{j}_{k}_{year}_{lat}_{lon}.csv"
        output_csv = os.path.join(time_series_directory, ts_csv)

        if not os.path.isfile(output_csv):
            logging.info(
                "The timeseries does not exist yet and is therefore " "calculated."
            )

            if row["technology"] == "si":
                time_series = create_si_time_series(
                    lat=lat, lon=lon, weather=weather, surface_azimuth=j, surface_tilt=k
                )
            elif row["technology"] == "cpv":
                time_series = create_cpv_time_series(
                    lat=lat,
                    lon=lon,
                    weather=weather,
                    surface_azimuth=j,
                    surface_tilt=k,
                )
            elif row["technology"] == "psi":
                time_series = create_psi_time_series(
                    lat=lat,
                    lon=lon,
                    year=year,
                    weather=weather,
                    surface_azimuth=j,
                    surface_tilt=k,
                )
            else:
                raise ValueError(
                    row["technology"],
                    "is not in technologies. Please " "choose 'si', 'cpv' or " "'psi'.",
                )
            #create tieseries directory if it does not exists
            if not os.path.isdir(time_series_directory):
                os.mkdir(time_series_directory)

            # save time series into mvs_inputs
            time_series.fillna(0, inplace=True)
            time_series.to_csv(output_csv, header=["kW"], index=False)
            logging.info(
                "%s" % row["technology"] + " time series is saved as csv "
                "into output directory"
            )
        else:
            time_series = pd.read_csv(output_csv)
            logging.info(
                f"The timeseries {output_csv}"
                "already exists and is therefore not calculated again."
            )

        # add "evaluated_period" to simulation_settings.csv
        check_inputs.add_evaluated_period_to_simulation_settings(
            time_series=time_series, mvs_input_directory=mvs_input_directory
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
            technology=row["technology"],
            area=area,
            surface_azimuth=j,
            surface_tilt=k,
            psi_type=psi_type,
        )
        # save the file name of the time series and the nominal value to
        # mvs_inputs/elements/csv/energyProduction.csv
        check_inputs.add_parameters_to_energy_production_file(
            pp_number=i + 1, ts_filename=ts_csv, nominal_value=nominal_value,
        )
    if plot == True:
        plt.show()


def get_optimal_pv_angle(lat):

    """
    Calculates the optimal tilt angle depending on the latitude.

    e.G. about 27° to 34° from ground in Germany.
    The pvlib uses tilt angles horizontal=90� and up=0�. Therefore 90� minus
    the angle from the horizontal.

    Parameters
    ---------
    lat: float
        latitude

    Returns
    -------
    int
        rounded angle for surface tilt

    """
    return round(lat - 15)


def set_up_system(technology, surface_azimuth, surface_tilt):

    """
    Sets up pvlibPVSystems.

    Initializes the pvlib.PVSystem for the given type of technology and returns
    the system and the module parameters as a dictionary.


    Parameters
    ----------
    technology: str
        possible technologies are: si, cpv or psi
    surface_azimuth: float
        surface azimuth of the module
    surface_tilt: float
        surface tilt of the module

    Returns
    -------
    PVSystem: :pandas:`pandas.Series<series>`
        Initialized PV system and module parameters.
    """

    if technology == "si":

        sandia_modules = pvlib.pvsystem.retrieve_sam("cecmod")
        sandia_module = sandia_modules["Aleo_Solar_S59y280"]
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
            "cpv module parameters are loaded from greco_technologies/inputs.py"
        )
        mod_params_cpv = greco_technologies.cpv.inputs.mod_params_cpv
        mod_params_flatplate = greco_technologies.cpv.inputs.mod_params_flatplate

        static_hybrid_sys = cpvlib.StaticHybridSystem(
            surface_tilt=surface_tilt,
            surface_azimuth=surface_azimuth,
            module_cpv=None,
            module_flatplate=None,
            module_parameters_cpv=mod_params_cpv,
            module_parameters_flatplate=mod_params_flatplate,
            modules_per_string=1,
            strings_per_inverter=1,
            inverter=None,
            inverter_parameters=None,
            racking_model="insulated",
            losses_parameters=None,
            name=None,
        )

        return (
            static_hybrid_sys,
            mod_params_cpv,
            mod_params_flatplate,
        )

    elif technology == "psi":
        pass
    else:
        logging.warning(
            f"{technology} is not in technologies. Please chose si, cpv or psi."
        )


def create_si_time_series(
    lat, lon, weather, surface_azimuth, surface_tilt, normalized=True
):

    """
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
    weather: :pandas:`pandas.DataFrame<frame>`
    surface_azimuth: float
        surface azimuth of the modules
    surface_tilt: float
        surface tilt of the modules
    normalized: boolean

    Returns
    -------
    :pandas:`pandas.Series<series>`
    """

    system, module_parameters = set_up_system(
        technology="si", surface_azimuth=surface_azimuth, surface_tilt=surface_tilt
    )
    location = Location(latitude=lat, longitude=lon)

    peak = module_parameters["I_mp_ref"] * module_parameters["V_mp_ref"]

    mc = ModelChain(
        system,
        location,
        orientation_strategy=None,
        aoi_model="ashrae",
        spectral_model="no_loss",
    )
    mc.run_model(weather=weather)
    output = mc.dc
    if normalized == True:
        logging.info("normalized si time series is calculated.")
        return (output["p_mp"] / peak).clip(0)
    else:
        logging.info("si time series is calculated in kW without normalization.")
        return output["p_mp"] / 1000


def create_cpv_time_series(
    lat, lon, weather, surface_azimuth, surface_tilt, normalized=True
):

    """
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
        `wind_speed` in m/s, `dni`, `dhi` and `ghi` in W/m²
    surface_azimuth : float
        Surface azimuth of the modules (180° for south, 270° for west, etc.).
    surface_tilt: float
        Surface tilt of the modules. (horizontal=90° and vertical=0°)
    normalized: bool
        If True, the time series is divided by the peak power of the CPV
        module. Default: False.

    Returns
    -------
    :pandas:`pandas.Series<series>`
        Power output of CPV module in W (if parameter `normalized` is False) or todo: check unit.
        normalized power output of CPV module (if parameter `normalized` is
        False).

    """

    system, mod_params_cpv, mod_params_flatplate = set_up_system(
        technology="cpv", surface_azimuth=surface_azimuth, surface_tilt=surface_tilt,
    )

    peak = (mod_params_cpv["i_mp"] * mod_params_cpv["v_mp"]) + (
        mod_params_flatplate["i_mp"] * mod_params_flatplate["v_mp"]
    )
    if normalized == True:
        logging.info("Normalized CPV time series is calculated in kW.")
        return (
            apply_cpvlib_StaticHybridSystem.create_cpv_time_series(
                lat, lon, weather, surface_azimuth, surface_tilt
            )
            / peak
        ).clip(0)
    else:
        logging.info("Absolute CPV time series is calculated in kW.")
        return (
            apply_cpvlib_StaticHybridSystem.create_cpv_time_series(
                lat, lon, weather, surface_azimuth, surface_tilt
            )
            / 1000
        )


def create_psi_time_series(
    lat,
    lon,
    year,
    surface_azimuth,
    surface_tilt,
    weather,
    normalized=True,
    psi_type="Chen",
):

    """
         Creates power time series of a Perovskite-Silicone module.

         The PSI time series is created for a given weather data frame
         (`weather`). If `normalized` is set to True, the time
         series is divided by the peak power of the module.


         Parameters
         ----------
         lat : float
             Latitude of the location for which the time series is calculated.
         lon : float
             Longitude of the location for which the time series is calculated.
         weather : :pandas:`pandas.DataFrame<frame>`
             DataFrame with time series for temperature `temp_air` in C°, wind speed
             `wind_speed` in m/s, `dni`, `dhi` and `ghi` in W/m^2
         surface_azimuth : float
             Surface azimuth of the modules (180° for south, 270° for west, etc.).
         surface_tilt: float
             Surface tilt of the modules. (horizontal=90° and vertical=0°)
         psi_type  : str
             Defines the type of module of which the time series is calculated.
             Options: "Korte", "Chen"
         normalized: bool
             If True, the time series is divided by the peak power of the CPV
             module. Default: False.

         Returns
         -------
         :pandas:`pandas.Series<series>`
             Power output of PSI module in W (if parameter `normalized` is False) or todo check unit.
             normalized power output of CPV module (if parameter `normalized` is
             False).

         """
    atmos_data = weather[["ghi", "wind_speed", "temp_air"]]

    if normalized == False:
        logging.info("Absolute PSI time series is calculated in kW.")
        return (
            greco_technologies.perosi.perosi.create_pero_si_timeseries(
                year,
                lat,
                lon,
                surface_azimuth,
                surface_tilt,
                atmos_data=atmos_data,
                number_hours=8760,
                psi_type=psi_type,
            )
            / 1000
        )
    else:
        logging.info("Normalized PSI time series is calculated.")
        if psi_type == "Korte":
            import greco_technologies.perosi.data.cell_parameters_korte_pero as param1
            import greco_technologies.perosi.data.cell_parameters_korte_si as param2
        elif psi_type == "Chen":
            import greco_technologies.perosi.data.cell_parameters_Chen_2020_4T_pero as param1
            import greco_technologies.perosi.data.cell_parameters_Chen_2020_4T_si as param2

        # calculate peak power with 5 % CTM losses
        peak = (param1.p_mp + param2.p_mp) - ((param1.p_mp + param2.p_mp) / 100) * 5

        return (
            greco_technologies.perosi.perosi.create_pero_si_timeseries(
                year,
                lat,
                lon,
                surface_azimuth,
                surface_tilt,
                atmos_data=atmos_data,
                number_hours=8760,
                psi_type=psi_type,
            )
            / peak
        ).clip(0)


def nominal_values_pv(technology, area, surface_azimuth, surface_tilt, psi_type):

    """
    calculates the maximum installed capacity for each pv module.

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

    if technology == "si":
        system, module_parameters = set_up_system(
            technology=technology,
            surface_azimuth=surface_azimuth,
            surface_tilt=surface_tilt,
        )
        peak = module_parameters["I_mp_ref"] * module_parameters["V_mp_ref"]
        module_size = module_parameters["A_c"]
        nominal_value = round(area / module_size * peak) / 1000
    elif technology == "cpv":
        system, mod_params_cpv, mod_params_flatplate = set_up_system(
            technology=technology,
            surface_azimuth=surface_azimuth,
            surface_tilt=surface_tilt,
        )
        peak = (
            mod_params_cpv["i_mp"] * mod_params_cpv["v_mp"]
            + mod_params_flatplate["i_mp"]
            * mod_params_flatplate["v_mp"]  # todo: adjust pmp flatplate
        )
        module_size = mod_params_cpv["Area"]
        nominal_value = round(area / module_size * peak) / 1000
    elif technology == "psi":  # todo: correct nominal value
        if psi_type == "Korte":
            import greco_technologies.perosi.data.cell_parameters_korte_pero as param1
            import greco_technologies.perosi.data.cell_parameters_korte_si as param2
        elif psi_type == "Chen":
            import greco_technologies.perosi.data.cell_parameters_Chen_2020_4T_pero as param1
            import greco_technologies.perosi.data.cell_parameters_Chen_2020_4T_si as param2

        # calculate peak power with 5 % CTM losses
        peak = (param1.p_mp + param2.p_mp) - ((param1.p_mp + param2.p_mp) / 100) * 5
        module_size = param1.A / 10000  # in m^2
        nominal_value = round((area / module_size) * peak) / 1000

    logging.info(
        "The nominal value for %s" % technology  # todo technology instead of type?
        + " is %s" % nominal_value
        + " kWp for an area of %s" % area
        + " qm."
    )
    return nominal_value


if __name__ == "__main__":
    area = area_potential.calculate_area_potential(
        population=48000,
        input_directory=constants.DEFAULT_INPUT_DIRECTORY,
        surface_type="flat_roof",
    )

    nominal_value_psi = nominal_values_pv(
        technology="psi",
        area=area,
        surface_azimuth=180,
        surface_tilt=30,
        psi_type="Chen",
    )
    print(nominal_value_psi)

    # filename = os.path.abspath("./data/inputs/weatherdata.csv")
    # weather_df = pd.read_csv(
    #     filename, index_col=0, date_parser=lambda idx: pd.to_datetime(idx, utc=True)
    # )
    # weather_df.index = pd.to_datetime(weather_df.index).tz_convert("Europe/Berlin")
    # weather_df["dni"] = weather_df["ghi"] - weather_df["dhi"]
    #
    # create_pv_components(lat=40.3, lon=5.4, weather=weather_df, population=600)

    weather_df = pd.DataFrame()
    weather_df["temp_air"] = [4, 5]
    weather_df["wind_speed"] = [2, 2.5]
    weather_df["dhi"] = [100, 120]
    weather_df["dni"] = [120, 150]
    weather_df["ghi"] = [200, 220]
    weather_df.index = ["2014-01-01 13:00:00+00:00", "2014-01-01 14:00:00+00:00"]
    weather_df.index = pd.to_datetime(weather_df.index)
    weather = weather_df
    year = 2014

    lat = 40.0
    lon = 5.2
    surface_azimuth = 180
    surface_tilt = 30

    output = create_psi_time_series(
        lat=lat,
        lon=lon,
        year=year,
        weather=weather,
        surface_azimuth=surface_azimuth,
        surface_tilt=surface_tilt,
        normalized=True,
        psi_type="Chen",
    )
    print(output.sum())
    #
    # output=get_optimal_pv_angle(lat=40.0)
    #
    # print(output)
