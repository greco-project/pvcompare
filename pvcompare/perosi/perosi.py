import pandas as pd
import logging
import sys
import os
import matplotlib.pyplot as plt
import decimal

import pvlib
import pvcompare.perosi.pvlib_smarts as smarts
import pvcompare.perosi.era5 as era5


# Reconfiguring the logger here will also affect test running in the PyCharm IDE
log_format = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)


def calculate_smarts_parameters(
    year,
    lat,
    lon,
    number_hours,
    cell_type,
    surface_tilt,
    surface_azimuth,
    atmos_data,
    WLMN=350,
    WLMX=1200,
):

    """
    calculates the short current density Jsc for each timestep.

    For each timestep the spectrum is calculated using SMARTS. After that the
    short current density is calculated by multiplying the number of photons on
    the tilted surface by the EQE of the given cell. A dataframe is returned
    with ghi, temperature, wind_speed and the Jsc for each time step

    Parameters
    ----------
    year: int
        year of interest
    lat: str
        latitude ending with a ".", e.g. "45."
    lon: int
        longitude
    number_hours: int
        number of hours until simulation stops. For one year enter 8760.
    cell_type: list
        list of cells for which the Jsc should be calculated.
    atmos_data: :pandas:`pandas.DataFrame<frame>`
        with datetimeindex and columns for 'temp_air' and 'wind_speed' and 'ghi'
    WLMN: int
        minimum wavelength of the spectrum. By default this is 280 nm.
    WLMX: int
        maximum wavelength of the spectrum. By default this is 1200 nm.


    Returns
    --------
    :pandas:`pandas.DataFrame<frame>`
        including ghi, temperature, wind_speed, Jsc for each cell_type
    """

    # check if atmos_data is in given as an input variable
    if atmos_data is None:
        logging.info("loading atmos data from era5 data set")
        atmos_data = era5.load_era5_weatherdata(lat, lon, year, variable="perosi")
    #    delta = pd.to_timedelta(30, unit="m")
    #    atmos_data.index = atmos_data.index + delta
    atmos_data.index = pd.to_datetime(atmos_data.index)
    atmos_data["davt"] = atmos_data["temp_air"].resample("D").mean()
    atmos_data = atmos_data.fillna(method="ffill")

    # calculate poa_total for tilted surface
    spa = pvlib.solarposition.spa_python(
        time=atmos_data.index, latitude=lat, longitude=lon
    )

    poa = pvlib.irradiance.get_total_irradiance(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        solar_zenith=spa["zenith"],
        solar_azimuth=spa["azimuth"],
        dni=atmos_data["dni"],
        ghi=atmos_data["ghi"],
        dhi=atmos_data["dhi"],
    )

    atmos_data["poa_global"] = poa["poa_global"]

    # define constant
    q = 1.602176634 / (10 ** 19)  # in Coulomb = A*s
    # define output data format
    iout = "8 12"
    # define counter for number of hours to be calculated
    c = 0
    # define time interval of one year
    # time = pd.date_range(start=f'1/1/{year}', end=f'31/12/{year}', freq='H')
    # calculate Jsc for every timestep
    result = pd.DataFrame()
    logging.info(
        "loading spectral weather data from SMARTS Nrel and "
        "calculating Isc for every timestep"
    )
    for index, row in atmos_data.iterrows():
        if index.month in range(3, 8):
            season = "SUMMER"
        else:
            season = "WINTER"

        # load spectral data from SMARTS

        d = decimal.Decimal(str(lat))
        decimals_lat = d.as_tuple().exponent
        lat_spectrum = str(lat)[:decimals_lat]
        spectrum = smarts.SMARTSSpectra(
            IOUT=iout,
            YEAR=str(year),
            MONTH=str(index.month),
            DAY=str(index.day),
            HOUR=str(index.hour),
            LATIT=lat_spectrum,
            LONGIT=str(lon),
            WLMN=WLMN,
            WLMX=WLMX,
            TAIR=str(atmos_data.at[index, "temp_air"]),
            TDAY=str(atmos_data.at[index, "davt"]),
            SEASON=season,
            ZONE=0,
            TILT=str(surface_tilt),
            WAZIM=str(surface_azimuth),
            W=str(atmos_data.at[index, "precipitable_water"]),
        )

        # load EQE data
        for x in cell_type:
            if x == "Korte_pero":
                import pvcompare.perosi.data.cell_parameters_korte_pero as param
            elif x == "Korte_si":
                import pvcompare.perosi.data.cell_parameters_korte_si as param
            elif x == "Chen_pero":
                import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_pero as param

                url = "https://raw.githubusercontent.com/greco-project/pvcompare/dev/pvcompare/perosi/data/CHEN_2020_EQE_curve_pero_corrected.csv"
            elif x == "Chen_si":
                import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_si as param

                url = "https://raw.githubusercontent.com/greco-project/pvcompare/dev/pvcompare/perosi/data/CHEN_2020_EQE_curve_si_corrected.csv"
            else:
                logging.error(
                    "The cell type is not recognized. Please "
                    "choose either 'Korte_si', 'Korte_pero', 'Chen_si' "
                    "or 'Chen_pero."
                )
            EQE_filename = param.EQE_filename
            path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "data", EQE_filename
            )

            EQE = pd.read_csv(path, sep=",", index_col=0)

            EQE = EQE / 100

            # return Jsc and ghi = 0 if the spectrum is empty
            if spectrum.empty == True:
                result.at[index, "Jsc_" + str(x)] = 0
                result.at[index, "ghi"] = 0

            else:
                if not spectrum.index.name == "Wvlgth":
                    spectrum.set_index("Wvlgth", inplace=True)

                # scale spectrum to era5-ghi
                spectral_ghi_sum = spectrum["Global_tilted_irradiance"].sum()
                ghi_corrected = spectral_ghi_sum - (
                    spectral_ghi_sum - atmos_data.at[index, "poa_global"]
                )
                diff_percent = ghi_corrected / (spectral_ghi_sum / 100)
                spectrum["Global_tilt_photon_corrected"] = (
                    spectrum["Global_tilt_photon_irrad"] / 100 * diff_percent
                )  # pro cm²
                spectrum["Global_tilted_irradiance_corrected"] = (
                    spectrum["Global_tilted_irradiance"] / 100 * diff_percent
                )

                # calculate Jsc
                Jsc_lambda = (
                    spectrum["Global_tilt_photon_corrected"] * EQE["EQE"]
                ) * q  # Jsc pro cm²
                Jsc_lambda.fillna(0, inplace=True)
                result.at[index, "Jsc_" + str(x)] = Jsc_lambda.sum()  # in A/cm²
                result.at[index, "ghi"] = atmos_data.at[index, "poa_global"]  # in W/m²
                result.at[index, "ghi_spectrum_corrected"] = spectrum[
                    "Global_tilted_irradiance_corrected"
                ].sum()  # in W/m²

        result.at[index, "temp"] = atmos_data.at[index, "temp_air"]
        result.at[index, "wind_speed"] = atmos_data.at[index, "wind_speed"]

        # check if number of hours is reached
        c = c + 1
        if c == number_hours:
            break
    return result


def create_timeseries(
    lat, lon, surface_azimuth, surface_tilt, atmos_data, year, cell_type, number_hours
):
    """
    Calculates a timeseries for each cell type in list cell_type.

    The spectrum is calculated with calculate_smarts_parameters(). After that
    the specific cell parameters are loaded. Finally the p_mp of each timestep
     is calculated by the pvlib.singlediode() fuction.

    Parameters
    ----------
    year: int
        year of interest
    lat: str
        latitude ending with a ".", e.g. "45."
    lon: int
        longitude
    number_hours: int
        number of hours until simulation stops. For one year enter 8760.
    cell_type: list
        list of cells for which the Jsc should be calculated. Allowed values:
        'Korte_pero', 'Korte_si', 'Chen_si', 'Chen_pero'
    surface_azimuth: int
        surface azimuth
    surface_tilt: int
        surface tilt
    atmos_data: :pandas:`pandas.DataFrame<frame>`
        with datetimeindex and columns for 'temp_air' and 'wind_speed' and 'ghi'

    Returns
    -------
    :pandas:`pandas.DataFrame<frame>`
        maximum power point of each time step for each cell type
    """
    q = 1.602176634 / (10 ** (19))  # in Coulomb = A/s
    kB = 1.380649 / 10 ** 23  # J/K

    # calculate spectral parameters from smarts and era5
    smarts_parameters = calculate_smarts_parameters(
        year=year,
        lat=lat,
        lon=lon,
        number_hours=number_hours,
        cell_type=cell_type,
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        atmos_data=atmos_data,
    )

    # calculate cell temperature characteristics
    t_cell = pvlib.temperature.pvsyst_cell(
        smarts_parameters["ghi"],
        smarts_parameters["temp"],
        smarts_parameters["wind_speed"],
    )

    result = pd.DataFrame()
    for x in cell_type:
        if x == "Korte_pero":
            import pvcompare.perosi.data.cell_parameters_korte_pero as param
        elif x == "Korte_si":
            import pvcompare.perosi.data.cell_parameters_korte_si as param
        elif x == "Chen_pero":
            import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_pero as param
        elif x == "Chen_si":
            import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_si as param

        nNsVth = param.n * (kB * (t_cell + 273.15) / q)

        Isc = smarts_parameters["Jsc_" + str(x)] * param.A_cell
        singlediode = pvlib.pvsystem.singlediode(
            photocurrent=Isc,
            saturation_current=param.I_0,
            resistance_series=param.rs,
            resistance_shunt=param.rsh,
            nNsVth=nNsVth,
            ivcurve_pnts=None,
            method="lambertw",
        )
        result[str(x) + "_p_mp"] = singlediode["p_mp"]
        # add temperature correction
        result[str(x) + "_p_mp"] = result[str(x) + "_p_mp"] * (
            1 + (param.alpha * (t_cell - param.temp_ref))
        )

    return result


def create_pero_si_timeseries(
    year,
    lat,
    lon,
    surface_azimuth,
    surface_tilt,
    number_hours,
    atmos_data=None,
    psi_type="Chen",
):

    """
    Creates a time series for the output power of a pero-si module.

    Wrapper for create_timeseries() function.

    Parameters
    ----------
    year: int
        year of interest
    lat: str
        latitude
    lon: int
        longitude
    number_hours: int
        number of hours until simulation stops. For one year enter 8760.
    surface_azimuth: int
        surface azimuth
    surface_tilt: int
        surface tilt
    atmos_data: :pd.Dataframe().
        weather data with datetimeindex and columns for 'temp_air' and
        'wind_speed' and 'ghi'. If None weather data is loaded from era5 weather data set.
    psi_type: str
        Type of pero_si cell. Either "Chen" or "Korte"

    Returns
    ---------
    :pandas:`pandas.Series<series>`
        time series of the output power
    """
    if psi_type == "Chen":
        cell_type = ["Chen_pero", "Chen_si"]
    elif psi_type == "Korte":
        cell_type = ["Korte_pero", "Korte_si"]
    else:
        logging.warning(
            f"The cell_type is {psi_type}. It is not recognized. Please "
            "choose between 'Korte' and 'Chen'."
        )
    for x in cell_type:
        if x == "Korte_pero":
            import pvcompare.perosi.data.cell_parameters_korte_pero as param
        elif x == "Korte_si":
            import pvcompare.perosi.data.cell_parameters_korte_si as param
        elif x == "Chen_pero":
            import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_pero as param
        elif x == "Chen_si":
            import pvcompare.perosi.data.cell_parameters_Chen_2020_4T_si as param

    timeseries = create_timeseries(
        lat=lat,
        lon=lon,
        surface_azimuth=surface_azimuth,
        surface_tilt=surface_tilt,
        atmos_data=atmos_data,
        year=year,
        cell_type=cell_type,
        number_hours=number_hours,
    )
    output = (timeseries.iloc[:, 0] + timeseries.iloc[:, 1]) * param.Ns

    return output
