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
import logging
import sys

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

import pvcompare.cpv.inputs
import pvcompare.perosi.perosi
from pvcompare import area_potential
from pvcompare import check_inputs
from pvcompare import constants

from cpvlib import cpvlib

from pvcompare.cpv import apply_cpvlib_StaticHybridSystem

log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)


def create_pv_components(
    lat,
    lon,
    weather,
    storeys,
    year,
    pv_setup=None,
    plot=True,
    user_inputs_pvcompare_directory=None,
    user_inputs_mvs_directory=None,
    psi_type="Chen",
    normalization=True,
):
    r"""
    Creates feed-in time series for all surface types in `pv_setup` or 'pv_setup.csv'.

    Reads 'pv_setup.csv', for each `surface_type` listed in `pv_setup`,
    one PV time series is created with regard to the technology and its
    orientation. All time series are normalized with the method specified in
    `normalization` and stored as csv files in `user_inputs_mvs_directory/time_series`.
    Further the area potential of the `surface_type` with regard to the building
    parameters defined in 'building_parameters.csv' in `input_directory` is calculated
    and the maximum installed capacity (nominal value) is calculated. Both parameters
    are stored into `user_inputs_mvs_directory/csv_elements/energyProduction.csv`.

    Further information for the cell parameter efficiency for "Chen" and "Korte" see
    `psi_type <https://pvcompare.readthedocs.io/en/latest/model_assumptions.html#input-data>`_.

    Parameters
    ----------
    lat: float
        Latitude of location
    lon: float
        Longitude of location
    weather: :pandas:`pandas.DataFrame<frame>`
        Hourly weather data frame with the columns:
        time, latitude, longitude, wind_speed, temp_air, ghi, dhi, dni,
        precipitable_water.
    storeys: int
        The number of storeys of a building.
    pv_setup: dict or None
        Specifies the PV technologies and their installation details used in the
        simulation. The dictionary contains columns: surface_type, technology,
        surface_azimuth, surface_tilt.
        A tilt of 0 resembles a vertical orientation.
        If `pv_setup` is None, it is loaded from the `input_directory/pv_setup.cvs`.
    plot: bool
        if true plots created pv times series
    user_inputs_pvcompare_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used as user_inputs_pvcompare_directory.
        Default: None.
    user_inputs_mvs_directory: str or None
        Directory of the multi-vector simulation inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
        Default: None.
    psi_type: str
        "Korte" or "Chen".
        Default: "Chen"
    normalization: bool
        If True: Time series is normalized. Otherwise absolute time series is
        returned. Default: True.

    Returns
    -------
    None
        Time series: :pandas:`pandas.DataFrame<frame>`
            Time series are normalized with the method specified in
            `normalization` and stored in `user_inputs_mvs_directory/time_series`.
        Area potential: float
            Area potential of the `surface_type` with regard to the building
            parameters defined in 'building_parameters.csv' in `input_directory` is calculated
            and stored into `user_inputs_mvs_directory/csv_elements/energyProduction.csv`
        Maximum installed capacity (nominal value): float
            The maximum installed capacity (nominal value) is calculated
            and stored into `user_inputs_mvs_directory/csv_elements/energyProduction.csv`.
    """

    if pv_setup is None:
        # read example pv_setup file
        logging.info("loading pv setup conditions from input directory.")

        if user_inputs_pvcompare_directory == None:
            user_inputs_pvcompare_directory = (
                constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
            )

        data_path = os.path.join(user_inputs_pvcompare_directory, "pv_setup.csv")
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

    #  define time series directory
    if user_inputs_mvs_directory is None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    time_series_directory = os.path.join(user_inputs_mvs_directory, "time_series")

    # parse through pv_setup file and create time series for each technology
    counter = 0
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
                    lat=lat,
                    lon=lon,
                    weather=weather,
                    surface_azimuth=j,
                    surface_tilt=k,
                    normalization=normalization,
                )
            elif row["technology"] == "cpv":
                time_series = create_cpv_time_series(
                    lat=lat,
                    lon=lon,
                    weather=weather,
                    surface_azimuth=j,
                    surface_tilt=k,
                    normalization=normalization,
                )
            elif row["technology"] == "psi":
                time_series = create_psi_time_series(
                    lat=lat,
                    lon=lon,
                    year=year,
                    weather=weather,
                    surface_azimuth=j,
                    surface_tilt=k,
                    normalization=normalization,
                )
            else:
                raise ValueError(
                    row["technology"],
                    "is not in technologies. Please " "choose 'si', 'cpv' or " "'psi'.",
                )
            # create time series directory if it does not exists
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
            time_series=time_series, user_inputs_mvs_directory=user_inputs_mvs_directory
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
                storeys,
                user_inputs_pvcompare_directory,
                surface_type=row["surface_type"],
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
        column_name = row["technology"]
        # check if the technology appears multiple times
        count_duplicates = (
            pv_setup.groupby(["technology"]).size().reset_index(name="count")
        )
        for index, r in count_duplicates.iterrows():
            if str(r["technology"]) == column_name and r["count"] > 1:
                counter += 1
                column_name = str(column_name) + str(counter)

            check_inputs.add_parameters_to_energy_production_file(
                technology=column_name,
                ts_filename=ts_csv,
                nominal_value=nominal_value,
                user_inputs_mvs_directory=user_inputs_mvs_directory,
            )
    if plot == True:
        plt.show()


def get_optimal_pv_angle(lat):

    r"""
    Calculates the optimal tilt angle depending on the latitude.

    e.g. about 27° to 34° from ground in Germany.
    The `pvlib <https://pvlib-python.readthedocs.io/en/stable/index.html>`_. uses
    tilt angles horizontal=90° and up=0°. Therefore 90° minus
    the angle from the horizontal.

    Parameters
    ---------
    lat: float
        latitude

    Returns
    -------
    int
        Angle for optimal surface tilt of `lat`, rounded to zero decimal places.
    """

    return round(lat - 15)


def set_up_system(technology, surface_azimuth, surface_tilt):

    r"""
    Sets up pvlibPVSystems.

    Initializes the pvlib.PVSystem for the given type of technology and returns
    the system and the module parameters as a dictionary.
    TODO: Reference to the pvlibPVSystems?

    Parameters
    ----------
    technology: str
        Possible technologies are: si, cpv or psi.
    surface_azimuth: float
        Surface azimuth of the module.
    surface_tilt: float
        Surface tilt of the module.

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

        logging.debug("cpv module parameters are loaded from pvcompare/cpv/inputs.py")
        mod_params_cpv = pvcompare.cpv.inputs.mod_params_cpv
        mod_params_flatplate = pvcompare.cpv.inputs.mod_params_flatplate

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

        return (static_hybrid_sys, mod_params_cpv, mod_params_flatplate)

    elif technology == "psi":
        pass
    else:
        logging.warning(
            f"{technology} is not in technologies. Please chose si, cpv or psi."
        )


def create_si_time_series(
    lat, lon, weather, surface_azimuth, surface_tilt, normalization
):
    r"""
    Calculates feed-in time series for a silicon PV module.

    The cpv time series is created for a given weather data frame, at a given
    orientation for the flat plate module 'Canadian_Solar_CS5P_220M___2009_'.
    If `normalization` is True the time series is normalized.

    Parameters
    ----------
    lat: float
        Latitude of the location.
    lon: float
        Longitude of the location.
    weather: :pandas:`pandas.DataFrame<frame>`
    surface_azimuth: float
        Surface azimuth of the modules.
    surface_tilt: float
        Surface tilt of the modules.
    normalization: bool
        If True: Time series is normalized. Otherwise absolute time series is
        returned.

    Returns
    -------
    :pandas:`pandas.Series<series>`
        Feed-in time series of silicon module.
    """

    system, module_parameters = set_up_system(
        technology="si", surface_azimuth=surface_azimuth, surface_tilt=surface_tilt
    )
    location = Location(latitude=lat, longitude=lon)

    mc = ModelChain(
        system,
        location,
        orientation_strategy=None,
        aoi_model="ashrae",
        spectral_model="first_solar",
        temperature_model="sapm",
        losses_model="pvwatts",
    )

    mc.run_model(weather=weather)
    output = mc.dc
    if normalization is False:
        logging.info("Absolute si time series is calculated in kW.")
        return output["p_mp"] / 1000
    else:
        logging.info("Normalized SI time series is calculated in kW/kWp.")
        peak = get_peak(
            technology="si",
            module_parameters_1=module_parameters,
            module_parameters_2=None,
        )
        return (output["p_mp"] / peak).clip(0)


def create_cpv_time_series(
    lat, lon, weather, surface_azimuth, surface_tilt, normalization
):
    r"""
    Creates power time series of a CPV module.

    The CPV time series is created for a given weather data frame `weather`
    for the INSOLIGHT CPV module. If `normalization` is True the time
    series is normalized.

    Parameters
    ----------
    lat : float
        Latitude of the location for which the time series is calculated.
    lon : float
        Longitude of the location for which the time series is calculated.
    weather : :pandas:`pandas.DataFrame<frame>`
        DataFrame with time series for temperature `temp_air` in C°, wind speed
        'wind_speed' in m/s, 'dni', 'dhi', and 'ghi' in W/m².
    surface_azimuth : float
        Surface azimuth of the modules (180° for south, 270° for west, etc.).
    surface_tilt: float
        Surface tilt of the modules (horizontal=90° and vertical=0°).
    normalization: bool
        If True: Time series is normalized. Otherwise absolute time series is
        returned.

    Returns
    -------
    :pandas:`pandas.Series<series>`
        Power output time series of CPV module in W.
    """

    system, mod_params_cpv, mod_params_flatplate = set_up_system(
        technology="cpv", surface_azimuth=surface_azimuth, surface_tilt=surface_tilt
    )

    if normalization is False:
        logging.info("Absolute CPV time series is calculated in kW.")
        return (
            apply_cpvlib_StaticHybridSystem.create_cpv_time_series(
                lat, lon, weather, surface_azimuth, surface_tilt
            )
            / 1000
        )

    else:
        logging.info("Normalized CPV time series is calculated in kW/kWp.")
        peak = get_peak(
            technology="cpv",
            module_parameters_1=mod_params_cpv,
            module_parameters_2=mod_params_flatplate,
        )
        return (
            apply_cpvlib_StaticHybridSystem.create_cpv_time_series(
                lat, lon, weather, surface_azimuth, surface_tilt
            )
            / peak
        ).clip(0)


def create_psi_time_series(
    lat,
    lon,
    year,
    surface_azimuth,
    surface_tilt,
    weather,
    normalization,
    psi_type="Chen",
):

    r"""
    Creates power time series of a perovskite-silicone (PSI) module.

    The PSI time series is created for a given weather data frame
    `weather`. If `normalization` is True the time series is normalized.

    Further information for the cell parameter efficiency for "Chen" and "Korte" see
    `psi_type <https://pvcompare.readthedocs.io/en/latest/model_assumptions.html#input-data>`_.

    Parameters
    ----------
    lat : float
        Latitude of the location for which the time series is calculated.
    lon : float
        Longitude of the location for which the time series is calculated.
    weather : :pandas:`pandas.DataFrame<frame>`
        DataFrame with time series for temperature 'temp_air' in C°, wind speed
        'wind_speed' in m/s, 'dni', 'dhi' and 'ghi' in W/m².
    surface_azimuth : float
        Surface azimuth of the modules (180° for south, 270° for west, etc.).
    surface_tilt: float
        Surface tilt of the modules. (horizontal=90° and vertical=0°)
    psi_type  : str
        Defines the type of module of which the time series is calculated.
        Options: "Korte", "Chen".
        Default: "Chen".
    normalization: bool
        If True: Time series is normalized. Otherwise absolute time series is
        returned.

    Returns
    -------
    :pandas:`pandas.Series<series>`
        Power output of PSI module in W (if parameter `normalized` is False) or TODO: check unit.
        normalized power output of CPV module (if parameter `normalized` is
        False).
    """

    atmos_data = weather[
        ["ghi", "dhi", "dni", "wind_speed", "temp_air", "precipitable_water"]
    ]
    number_rows = atmos_data["ghi"].count()

    if normalization is False:
        logging.info("Absolute PSI time series is calculated in kW.")
        return (
            pvcompare.perosi.perosi.create_pero_si_timeseries(
                year,
                lat,
                lon,
                surface_azimuth,
                surface_tilt,
                atmos_data=atmos_data,
                number_hours=number_rows,
                psi_type=psi_type,
            )
            / 1000
        )
    else:
        logging.info("Normalized CPV time series is calculated in kW/kWp.")
        if psi_type == "Korte":
            import pvcompare.perosi.data.cell_parameters_korte_pero as param1
            import pvcompare.perosi.data.cell_parameters_korte_si as param2
        elif psi_type == "Chen":
            import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_pero as param1
            import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_si as param2

        peak = get_peak(
            technology="psi",
            module_parameters_1=param1,
            module_parameters_2=param2,
        )
        output = pvcompare.perosi.perosi.create_pero_si_timeseries(
            year,
            lat,
            lon,
            surface_azimuth,
            surface_tilt,
            atmos_data=atmos_data,
            number_hours=number_rows,
            psi_type=psi_type,
        )
        # substract losses 45% in order to get to a realistic performance ratio
        output = output - output * 0.45

        return (output / peak).clip(0)


def nominal_values_pv(
        technology,
        area,
        surface_azimuth,
        surface_tilt,
        psi_type
):
    r"""
    calculates the maximum installed capacity for each pv module.

    The nominal value for each PV technology is constructed by the size of
    the module, its peak power and the total available area. It is given in
    the unit of kWp. The nominal value functions as a limit for the potential
    maximum installed capacity of PV in the energy system optimization.

    Further information for the cell parameter efficiency for "Chen" and "Korte" see
    `psi_type <https://pvcompare.readthedocs.io/en/latest/model_assumptions.html#input-data>`_.

    Parameters
    ----------
    technology: str
        Possible values are: si, cpv or psi.
    area: float
        total available surface area.
    surface_azimuth: float
        Surface azimuth of the modules.
    surface_tilt: float
        Surface tilt of the modules.
    psi_type  : str
        Defines the type of module of which the time series is calculated.
        Options: "Korte", "Chen".

    Returns
    -------
    nominal_value: int
        The rounded possible installed capacity for an area.
    """

    if technology == "si":
        system, module_parameters = set_up_system(
            technology=technology,
            surface_azimuth=surface_azimuth,
            surface_tilt=surface_tilt,
        )
        peak = get_peak(
            technology,
            module_parameters_1=module_parameters,
            module_parameters_2=None,
        )
        module_size = module_parameters["A_c"]
        nominal_value = round((area / module_size) * peak) / 1000
    elif technology == "cpv":
        system, mod_params_cpv, mod_params_flatplate = set_up_system(
            technology=technology,
            surface_azimuth=surface_azimuth,
            surface_tilt=surface_tilt,
        )
        peak = get_peak(
            technology,
            module_parameters_1=mod_params_cpv,
            module_parameters_2=mod_params_flatplate,
        )
        module_size = mod_params_cpv["Area"]
        nominal_value = round((area / module_size) * peak) / 1000
    elif technology == "psi":
        if psi_type == "Korte":
            import pvcompare.perosi.data.cell_parameters_korte_pero as param1
            import pvcompare.perosi.data.cell_parameters_korte_si as param2
        elif psi_type == "Chen":
            import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_pero as param1
            import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_si as param2

        # calculate peak power with 5 % CTM losses nad 5 % cell connection losses
        peak = get_peak(
            technology,
            module_parameters_1=param1,
            module_parameters_2=param2,
        )
        module_size = param1.A / 10000  # in m^2
        nominal_value = round((area / module_size) * peak) / 1000

    logging.info(
        "The nominal value for %s" % technology
        + " is %s" % nominal_value
        + " kWp for an area of %s" % area
        + " qm."
    )
    return nominal_value


def get_peak(technology, module_parameters_1, module_parameters_2):
    r"""
    This function returns the peak value for the given `technology`.

    Parameter
    ---------
    technology: str
        Possible values are: si, cpv or psi.
    module_parameters_1: dict
        Module parameters of cell 1 or module.
    module_parameters_2: dict
        If `technology` is 'si', set parameter to None

    Returns
    --------
    peak: float
        Peak value of the `technology`.
    """

    if technology == "si":
        peak = module_parameters_1["I_mp_ref"] * module_parameters_1["V_mp_ref"]
        return peak
    elif technology == "cpv":
        peak = module_parameters_1["p_mp"] + module_parameters_2["p_mp"]
        return peak
    elif technology == "psi":
        # calculate peak power with 10 % CTM losses
        peak = (
            module_parameters_1.p_mp
            + module_parameters_2.p_mp
            - (module_parameters_1.p_mp + module_parameters_2.p_mp) * 0.1
        )
        return peak
