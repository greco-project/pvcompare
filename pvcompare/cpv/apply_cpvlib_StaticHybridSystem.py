import matplotlib.pyplot as plt

import pvlib
import pandas as pd
from cpvlib import cpvlib
from pvcompare.cpv.inputs import mod_params_cpv, mod_params_flatplate
import os
import pvcompare.constants as constants


def create_cpv_time_series(
    lat, lon, weather, surface_azimuth, surface_tilt, plot=False
):
    r"""
    Calculates time series for a CPV module.

    Notice: Right now only module parameters for the hybrid INSOLIGHT module are
    provided. If you want to add your own module data please add it to `cpv/inputs.py`.
    The CPV module is modelled with the `cpvlib <https://cpvlib.readthedocs.io/en/latest/>`_.
    The solar position is defined with the use of `pvlib <https://pvlib-python.readthedocs.io/en/stable/index.html>`_.

    Parameters
    ----------
    lat: float
        Latitude of the location.
    lon: float
        Longitude of the location.
    weather: :pandas:`pandas.DataFrame<frame>`
        Weather dataframe according to pvlib standards.
    surface_azimuth: float
        surface azimuth of the module.
    surface_tilt: float
        surface tilt of the module.
    plot: bool
        If True, the time series is plotted and saved to `constants.DEFAULT_MVS_OUTPUT_DIRECTORY`.
        Default: False.

    Returns
    --------
    total: :pandas:`pandas.DataFrame<frame>`
        Time series of a CPV module.
    """

    location = pvlib.location.Location(latitude=lat, longitude=lon, tz="utc")

    weather.index = pd.to_datetime(weather.index)

    solar_zenith = location.get_solarposition(weather.index).zenith
    solar_azimuth = location.get_solarposition(weather.index).azimuth

    #%%
    # StaticHybridSystem
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

    # get_effective_irradiance
    (
        weather["dii_effective"],
        weather["poa_flatplate_static_effective"],
    ) = static_hybrid_sys.get_effective_irradiance(
        solar_zenith,
        solar_azimuth,
        #       iam_param=0.7,
        #       aoi_limit=60,
        dii=None,
        ghi=weather["ghi"],
        dhi=weather["dhi"],
        dni=weather["dni"],
    )

    # pvsyst_celltemp
    (
        weather["temp_cell_35"],
        weather["temp_cell_flatplate"],
    ) = static_hybrid_sys.pvsyst_celltemp(
        dii=weather["dii_effective"],
        poa_flatplate_static=weather["poa_flatplate_static_effective"],
        temp_air=weather["temp_air"],
        wind_speed=weather["wind_speed"],
    )

    weather.fillna(0, inplace=True)
    # calcparams_pvsyst
    (
        diode_parameters_cpv,
        diode_parameters_flatplate,
    ) = static_hybrid_sys.calcparams_pvsyst(
        dii=weather["dii_effective"],
        poa_flatplate_static=weather["poa_flatplate_static_effective"],
        temp_cell_cpv=weather["temp_cell_35"],
        temp_cell_flatplate=weather["temp_cell_flatplate"],
    )

    # singlediode
    dc_cpv, dc_flatplate = static_hybrid_sys.singlediode(
        diode_parameters_cpv, diode_parameters_flatplate
    )

    # uf_global (uf_am, uf_temp_air)
    weather["am"] = location.get_airmass(weather.index).airmass_absolute

    uf_cpv = static_hybrid_sys.get_global_utilization_factor_cpv(
        weather["am"], weather["temp_air"]
    )

    # plot power
    if plot == True:
        if weather.count()[0] > 5:
            cpv_days = dc_cpv["2014-06-15":"2014-06-20"]
            uf_cpv_days = uf_cpv["2014-06-15":"2014-06-20"]
            flatplate_days = dc_flatplate["2014-06-15":"2014-06-20"]
            data_days = weather["2014-06-15":"2014-06-20"]

            fig, axs = plt.subplots(2)

            (cpv_days.p_mp * uf_cpv_days).plot(ax=axs[0], label="CPV").legend(
                bbox_to_anchor=(1.1, 1), loc=3, borderaxespad=0.0
            )
            flatplate_days.p_mp.plot(
                ax=axs[0], secondary_y=True, label="Flat plate"
            ).legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
            data_days[["dni", "dhi"]].plot(ax=axs[1], linewidth=1).legend(
                bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0
            )
            axs[1].set_xlabel("time")
            axs[1].set_ylabel("Wh/m")
            axs[0].set_ylabel("Wh")

            plt.savefig(
                os.path.join(
                    constants.DEFAULT_MVS_OUTPUT_DIRECTORY, f"plot_cpv_timeseries.png"
                ),
                bbox_inches="tight",
            )

    # Energy
    energy_cpv = dc_cpv["p_mp"] * uf_cpv
    energy_flatplate = dc_flatplate["p_mp"]

    # add temperature correction -> not, because its already covered in uf_temp

    total = energy_cpv + energy_flatplate

    return total


def calculate_efficiency_ref():
    r"""
    Calculates maximum power output and efficiency for the CPV and flat plate module.

    The P_mp and efficiency are calculated at its reference conditions

    The reference conditions are:
    Temp_air = 20 ° C
    DII = 900 W/m² for cpv
    POA = 950 W/m² for flatplate

    Returns
    ------
    None
        Prints efficiency and p_mp for the flatplate and the cpv
        module and total efficiency.

    """

    surface_tilt = 30
    surface_azimuth = 180
    # StaticHybridSystem
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

    A = 0.1  # m2
    I_cpv = 900  # W/m2
    I_flat = 950  # W/m2
    temp_cell_35, temp_cell_flatplate = static_hybrid_sys.pvsyst_celltemp(
        dii=I_cpv, poa_flatplate_static=I_flat, temp_air=20, wind_speed=1
    )
    (
        diode_parameters_cpv,
        diode_parameters_flatplate,
    ) = static_hybrid_sys.calcparams_pvsyst(
        dii=I_cpv,
        poa_flatplate_static=I_flat,
        temp_cell_cpv=temp_cell_35,
        temp_cell_flatplate=temp_cell_flatplate,
    )

    p_cpv, p_flat = static_hybrid_sys.singlediode(
        diode_parameters_cpv, diode_parameters_flatplate
    )
    eff_cpv = p_cpv["p_mp"] / (I_cpv * A)
    eff_flat = p_flat["p_mp"] / (I_flat * A)

    print(p_cpv["p_mp"])
    print(p_flat["p_mp"])
    print(eff_cpv)
    print(eff_flat)
    print("total:", eff_cpv + eff_flat)
