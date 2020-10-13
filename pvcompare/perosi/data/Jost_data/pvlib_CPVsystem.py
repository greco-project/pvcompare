import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from pvlib.tools import _build_kwargs
from pvlib import pvsystem
from sklearn.metrics import mean_squared_error


class CPVSystem(object):
    """
    The CPVSystem class defines a set of CPV system attributes and modeling
    functions. This class describes the collection and interactions of CPV
    system components installed on a Dual Axis Tracker.

    The class supports basic system topologies consisting of:

        * `N` total modules arranged in series
          (`modules_per_string=N`, `strings_per_inverter=1`).
        * `M` total modules arranged in parallel
          (`modules_per_string=1`, `strings_per_inverter=M`).
        * `NxM` total modules arranged in `M` strings of `N` modules each
          (`modules_per_string=N`, `strings_per_inverter=M`).

    The attributes should generally be things that don't change about
    the system, such the type of module and the inverter. The instance
    methods accept arguments for things that do change, such as
    irradiance and temperature.

    Parameters
    ----------
    module : None or string, default None
        The model name of the modules.
        May be used to look up the module_parameters dictionary
        via some other method.

    module_parameters : None, dict or Series, default None
        Module parameters as defined by the SAPM, CEC, or other.

    modules_per_string: int or float, default 1
        See system topology discussion above.

    strings_per_inverter: int or float, default 1
        See system topology discussion above.

    inverter : None or string, default None
        The model name of the inverters.
        May be used to look up the inverter_parameters dictionary
        via some other method.

    inverter_parameters : None, dict or Series, default None
        Inverter parameters as defined by the SAPM, CEC, or other.

    racking_model : None or string, default 'open_rack_cell_glassback'
        Used for cell and module temperature calculations.

    losses_parameters : None, dict or Series, default None
        Losses parameters as defined by PVWatts or other.

    name : None or string, default None

    **kwargs
        Arbitrary keyword arguments.
        Included for compatibility, but not used.
    """

    def __init__(
        self,
        module=None,
        module_parameters=None,
        modules_per_string=1,
        strings_per_inverter=1,
        inverter=None,
        inverter_parameters=None,
        racking_model="open_rack_cell_glassback",
        losses_parameters=None,
        name=None,
        **kwargs
    ):

        self.name = name

        # could tie these together with @property
        self.module = module
        if module_parameters is None:
            self.module_parameters = {}
        else:
            self.module_parameters = module_parameters

        self.modules_per_string = modules_per_string
        self.strings_per_inverter = strings_per_inverter

        self.inverter = inverter
        if inverter_parameters is None:
            self.inverter_parameters = {}
        else:
            self.inverter_parameters = inverter_parameters

        if losses_parameters is None:
            self.losses_parameters = {}
        else:
            self.losses_parameters = losses_parameters

        self.racking_model = racking_model

    def __repr__(self):
        attrs = ["name", "module", "inverter", "racking_model"]
        return "CPVSystem: \n  " + "\n  ".join(
            ("{}: {}".format(attr, getattr(self, attr)) for attr in attrs)
        )

    def calcparams_pvsyst(self, effective_irradiance, temp_cell):
        """
        Use the :py:func:`pvsystem.calcparams_pvsyst` function, the input
        parameters and ``self.module_parameters`` to calculate the
        module currents and resistances.

        Parameters
        ----------
        effective_irradiance : numeric
            The irradiance (W/m2) that is converted to photocurrent.

        temp_cell : float or Series
            The average cell temperature of cells within a module in C.

        Returns
        -------
        See pvsystem.calcparams_pvsyst for details
        """

        kwargs = _build_kwargs(
            [
                "gamma_ref",
                "mu_gamma",
                "I_L_ref",
                "I_o_ref",
                "R_sh_ref",
                "R_sh_0",
                "R_sh_exp",
                "R_s",
                "alpha_sc",
                "EgRef",
                "irrad_ref",
                "temp_ref",
                "cells_in_series",
            ],
            self.module_parameters,
        )

        return pvsystem.calcparams_pvsyst(effective_irradiance, temp_cell, **kwargs)

    def pvsyst_celltemp(self, poa_global, temp_air, wind_speed=1.0):
        """
        Uses :py:func:`pvsystem.pvsyst_celltemp` to calculate module
        temperatures based on ``self.racking_model`` and the input parameters.

        Parameters
        ----------
        See pvsystem.pvsyst_celltemp for details

        Returns
        -------
        See pvsystem.pvsyst_celltemp for details
        """

        kwargs = _build_kwargs(["eta_m", "alpha_absorption"], self.module_parameters)

        return pvsystem.pvsyst_celltemp(
            poa_global, temp_air, wind_speed, model_params=self.racking_model, **kwargs
        )

    def singlediode(
        self,
        photocurrent,
        saturation_current,
        resistance_series,
        resistance_shunt,
        nNsVth,
        ivcurve_pnts=None,
    ):
        """Wrapper around the :py:func:`pvsystem.singlediode` function.

        Parameters
        ----------
        See pvsystem.singlediode for details

        Returns
        -------
        See pvsystem.singlediode for details
        """

        return pvsystem.singlediode(
            photocurrent,
            saturation_current,
            resistance_series,
            resistance_shunt,
            nNsVth,
            ivcurve_pnts=ivcurve_pnts,
        )

    def optical_transmission_losses(self, aoi):

        """
        optical transmission losses caused by the lens

        :param numeric: dni at a certain timestep
        :param numeric: aoi at a certain timestep
        :return: float, new dni minus optical tranmission losses
        """

        c0 = 4.54545455e-09
        c1 = -2.21212121e-06
        c2 = 8.09090909e-05
        c3 = -2.68463203e-03
        c4 = 8.62948052e-01

        if aoi >= 60:
            return 0
        else:
            ot = c4 + c3 * aoi + c2 * aoi ** 2 + c1 * aoi ** 3 + c0 * aoi ** 4
            return ot

    def glass_transmission_losses(self, aoi):  # todo: find mistake for aoi=59°

        # this is an insolight specific anti-reflection coating
        glass_ar_offset = 0.015
        n1 = 1.0
        n2 = 1.5

        if aoi <= 90:
            theta = aoi
        else:
            return 0

        Rs = (
            abs(
                (
                    n1 * math.cos(math.radians(theta))
                    - n2 * np.sqrt(1 - ((n1 / n2) * np.sin(math.radians(theta))) ** 2.0)
                )
                / (
                    n1 * np.cos(math.radians(theta))
                    + n2 * np.sqrt(1 - ((n1 / n2) * np.sin(math.radians(theta))) ** 2.0)
                )
            )
            ** 2
        )

        Rp = (
            abs(
                (
                    n1 * np.sqrt(1 - ((n1 / n2) * np.sin(math.radians(theta))) ** 2.0)
                    - n2 * np.cos(math.radians(theta))
                )
                / (
                    n1 * np.sqrt(1 - ((n1 / n2) * np.sin(math.radians(theta))) ** 2.0)
                    + n2 * np.cos(math.radians(theta))
                )
            )
            ** 2
        )

        Reff = 0.5 * (Rs + Rp)
        glass_transmission = (1.0 - Reff + glass_ar_offset) ** 2
        return glass_transmission

    def ufam(self, am):

        a0 = 1.0015288
        a1 = -0.00878182
        a2 = -0.00146694

        return a0 + a1 * am + a2 * am ** 2

    def ufdni(self, dni):

        d0 = 0
        d1 = 0
        d2 = 0

        return d0 + d1 * dni + d2 * dni ** 2

    def uftamb(self, t_ambient):

        t0 = 8.43234532e-01
        t1 = 1.04128138e-02
        t2 = -1.73841969e-04

        return t0 + t1 * t_ambient + t2 * t_ambient ** 2

    def UF_corrected_DNI(self, am, t_ambient, dni):

        """
        The approach follows the model of Gerstmaier (Quelle), promoting a Utilization Faktor
        that reflects the spectral (AM), temperature (Tamb) and DNI dependencies of
        multijunction cells. The Utilization Factor is multiplied with the DNI.

        UF = c1 * UF(AM) + c2 * UF(DNI) + c3 * UF(Tamb)

        Parameters
        --------------
        am: float or Series
            airmass
        t_ambient: float or Series
            ambient temperature
        dni: float or Series
            direct normal irradiance


        :return: The altered DNI that includes the parametrization of multijunction
                cells
        """

        uf_am = ufam(am)
        uf_dni = ufdni(dni)
        uf_tamb = uftamb(t_ambient)
        c1 = 1
        c2 = 1
        c3 = 1

        df_new = pd.concat([uf_am, uf_dni, uf_tamb], axis=1)
        df = df_new.sum(axis=1)

        #    UF = c1 * uf_am + c2 * uf_dni + c3 * uf_tamb

        return dni * df


class StaticCPVSystem(CPVSystem):
    """
    The StaticCPVSystem class defines a set of CPV system attributes and
    modeling functions. This class describes the collection and interactions of
    Static CPV system components installed on a Fixed Panel.

    The class supports basic system topologies consisting of:

        * `N` total modules arranged in series
          (`modules_per_string=N`, `strings_per_inverter=1`).
        * `M` total modules arranged in parallel
          (`modules_per_string=1`, `strings_per_inverter=M`).
        * `NxM` total modules arranged in `M` strings of `N` modules each
          (`modules_per_string=N`, `strings_per_inverter=M`).

    The attributes should generally be things that don't change about
    the system, such the type of module and the inverter. The instance
    methods accept arguments for things that do change, such as
    irradiance and temperature.

    Parameters
    ----------
    surface_tilt: float or array-like, default 0
        Surface tilt angles in decimal degrees.
        The tilt angle is defined as degrees from horizontal
        (e.g. surface facing up = 0, surface facing horizon = 90)

    surface_azimuth: float or array-like, default 180
        Azimuth angle of the module surface.
        North=0, East=90, South=180, West=270.

    module : None or string, default None
        The model name of the modules.
        May be used to look up the module_parameters dictionary
        via some other method.

    module_parameters : None, dict or Series, default None
        Module parameters as defined by the SAPM, CEC, or other.

    modules_per_string: int or float, default 1
        See system topology discussion above.

    strings_per_inverter: int or float, default 1
        See system topology discussion above.

    inverter : None or string, default None
        The model name of the inverters.
        May be used to look up the inverter_parameters dictionary
        via some other method.

    inverter_parameters : None, dict or Series, default None
        Inverter parameters as defined by the SAPM, CEC, or other.

    racking_model : None or string, default 'open_rack_cell_glassback'
        Used for cell and module temperature calculations.

    losses_parameters : None, dict or Series, default None
        Losses parameters as defined by PVWatts or other.

    name : None or string, default None

    **kwargs
        Arbitrary keyword arguments.
        Included for compatibility, but not used.
    """

    def __init__(
        self,
        surface_tilt=0,
        surface_azimuth=180,
        module=None,
        module_parameters=None,
        modules_per_string=1,
        strings_per_inverter=1,
        inverter=None,
        inverter_parameters=None,
        racking_model="open_rack_cell_glassback",
        losses_parameters=None,
        name=None,
        **kwargs
    ):

        self.surface_tilt = surface_tilt
        self.surface_azimuth = surface_azimuth

        CPVSystem.__init__(
            self,
            module,
            module_parameters,
            modules_per_string,
            strings_per_inverter,
            inverter,
            inverter_parameters,
            racking_model,
            losses_parameters,
            name,
            **kwargs
        )

    def __repr__(self):
        attrs = ["name", "module", "inverter", "racking_model"]
        return "StaticCPVSystem: \n  " + "\n  ".join(
            ("{}: {}".format(attr, getattr(self, attr)) for attr in attrs)
        )


def optical_transmission_losses(aoi):

    """
    optical transmission losses caused by the lens

    :param numeric: dni at a certain timestep
    :param numeric: aoi at a certain timestep
    :return: float, new dni minus optical tranmission losses
    """

    c0 = 4.54545455e-09
    c1 = -2.21212121e-06
    c2 = 8.09090909e-05
    c3 = -2.68463203e-03
    c4 = 8.62948052e-01

    if aoi >= 60:
        return 0
    else:
        ot = c4 + c3 * aoi + c2 * aoi ** 2 + c1 * aoi ** 3 + c0 * aoi ** 4
        return ot


def glass_transmission_losses(aoi):  # todo: find mistake for aoi=59°

    # this is an insolight specific anti-reflection coating
    glass_ar_offset = 0.015
    n1 = 1.0
    n2 = 1.5

    if aoi <= 90:
        theta = aoi
    else:
        return 0

    Rs = (
        abs(
            (
                n1 * math.cos(math.radians(theta))
                - n2 * np.sqrt(1 - ((n1 / n2) * np.sin(math.radians(theta))) ** 2.0)
            )
            / (
                n1 * np.cos(math.radians(theta))
                + n2 * np.sqrt(1 - ((n1 / n2) * np.sin(math.radians(theta))) ** 2.0)
            )
        )
        ** 2
    )

    Rp = (
        abs(
            (
                n1 * np.sqrt(1 - ((n1 / n2) * np.sin(math.radians(theta))) ** 2.0)
                - n2 * np.cos(math.radians(theta))
            )
            / (
                n1 * np.sqrt(1 - ((n1 / n2) * np.sin(math.radians(theta))) ** 2.0)
                + n2 * np.cos(math.radians(theta))
            )
        )
        ** 2
    )

    Reff = 0.5 * (Rs + Rp)
    glass_transmission = (1.0 - Reff + glass_ar_offset) ** 2
    return glass_transmission


def ufam(am):
    a0 = 3.14343721e-03
    a1 = 1.02361039e-05
    a2 = -8.37260985e-08

    return a0 + a1 * am + a2 * am ** 2


def ufdni(dni):

    if not (dni is None):
        d0 = 0
        d1 = 0
        d2 = 0

        return d0 + d1 * dni + d2 * dni ** 2
    else:
        return 0


def uftamb(t_ambient):
    t0 = 3.18368513e-03
    t1 = 6.47684709e-06

    return t0 + t1 * t_ambient


def get_single_util_factor(x, thld, m_low, m_high):
    """
    Retrieves the utilization factor for a variable.

    Parameters
    ----------
    x : variable value for the utilization factor calc.

    thld : numeric
        limit between the two regression lines of the utilization factor.

    m_low : numeric
        inclination of the first regression line of the utilization factor.

    m_high : numeric
        inclination of the second regression line of the utilization factor.

    Returns
    -------
    single_uf : numeric
        utilization factor for the x variable.
    """

    if x <= thld:
        single_uf = 1 + (x - thld) * m_low

    else:
        single_uf = 1 + (x - thld) * m_high

    return single_uf


def calculate_utilization_factor(
    uf_am, uf_temp, weight_am, weight_temp, calculate_ufdni=False
):

    """
    The approach follows the model of Gerstmaier (Quelle), promoting a Utilization Faktor
    that reflects the spectral (AM), temperature (Tamb) and DNI dependencies of
    multijunction cells. The Utilization Factor is multiplied with the DNI.

    UF = c1 * UF(AM) + c2 * UF(DNI) + c3 * UF(Tamb)

    Parameters
    --------------
    am: float or Series
        airmass
    t_ambient: float or Series
        ambient temperature
    dni: float or Series
        direct normal irradiance
    uf_dni: Boolean
        dni-Utilization factor is consideres or not


    :return: The altered DNI that includes the parametrization of multijunction
            cells
    """

    #    UF = c1 * uf_am + c2 * uf_dni + c3 * uf_tamb

    # calculate weights
    if not calculate_ufdni:
        UF = np.multiply(weight_am, uf_am) + np.multiply(weight_temp, uf_temp)
    else:
        UF = (
            np.multiply(weight_am, uf_am)
            + np.multiply(weight_dni, uf_dni)
            + np.multiply(weight_temp, uf_temp)
        )

    return UF


########helpers functions################


def fit_sde_sandia(V, I, Voc, Isc, Vmp, Imp, vlim=0.2, ilim=0.1):
    """ Fits the single diode equation to an IV curve.
    If fitting fails, returns NaN in each parameter.
    Parameters
    ----------
    V : numeric
        Voltage at each point on the IV curve, from 0 to Voc
    I : numeric
        Current at each point on the IV curve, from Isc to 0
    Voc : float
        Open circuit voltage
    Isc : float
        Short circuit current
    Vmp : float
        Voltage at maximum power point
    Imp : float
        Current at maximum power point
    vlim : float, default 0.2
        defines linear portion of IV curve i.e. V <= vlim * Voc
    ilim : float, default 0.1
        defines exponential portion of IV curve i.e. I > ilim * Isc
    Returns
    -------
    IL : float
        photocurrent, A
    I0 : float
        dark (saturation) current, A
    Rs : float
        series resistance, ohm
    Rsh : float
        shunt (parallel) resistance, ohm
    nNsVth : float
        product of diode (ideality) factor n (unitless) x number of
        cells in series Ns (unitless) x cell thermal voltage Vth (V), V
    References
    ----------
    [1] C. B. Jones, C. W. Hansen, Single Diode Parameter Extraction from
    In-Field Photovoltaic I-V Curves on a Single Board Computer, 46th IEEE
    Photovoltaic Specialist Conference, Chicago, IL, 2019
    """
    # Find intercept and slope of linear portion of IV curve.
    # Start with V < vlim * Voc, extend by adding points until slope is
    # acceptable
    beta = [np.nan for i in range(5)]
    beta[0] = np.nan
    beta[1] = np.nan
    idx = len(V <= vlim * Voc)
    while np.isnan(beta[1]) and (idx <= len(V)):
        try:
            p = np.polyfit(V[:idx], I[:idx], deg=1)
            if p[1] < 0:
                beta[0] = p[0]
                beta[1] = -p[1]  # sign change to get positive parameter value
        except:
            pass
        if np.isnan(beta[1]):
            idx += 1

    if not np.isnan(beta[0]):
        # Find parameters from exponential portion of IV curve
        Y = beta[0] - beta[1] * V - I
        X = np.array([V, I])
        idx = len(Y <= ilim * Isc)
        try:
            p = np.linalg.lstsq(X, Y)
            beta[3] = p[1]
            beta[4] = p[2]
        except:
            pass

    if not any([np.isnan(beta[i]) for i in [0, 1, 3, 4]]):
        # calculate parameters
        nNsVth = 1.0 / beta[3]
        Rs = beta[4] / beta[3]
        Gp = beta[1] / (1.0 - Rs * beta[1])
        Rsh = 1.0 / Gp
        IL = (1 + Gp * Rs) * beta[0]
        # calculate I0
        I0_Vmp = _calc_I0(IL, Imp, Vmp, Gp, Rs, beta[3])
        I0_Voc = _calc_I0(IL, 0, Voc, Gp, Rs, beta[3])
        if (I0_Vmp > 0) and (I0_Voc > 0):
            I0 = 0.5 * (I0_Vmp + I0_Voc)
        elif I0_Vmp > 0:
            I0 = I0_Vmp
        elif I0_Voc > 0:
            I0 = I0_Voc
        else:
            I0 = np.nan

    return IL, I0, Rs, Rsh, nNsVth


def _calc_I0(IL, I, V, Gp, Rs, beta3):
    return (IL - I - Gp * V - Gp * Rs * I) / np.exp(beta3 * (V + Rs * I))


if __name__ == "__main__":

    aoi_list = {}
    gt_list = {}
    aoi = 1
    while aoi < 200:
        gt = glass_transmission_losses(aoi)
        aoi_list[aoi] = gt
        aoi = aoi + 1

    # print(gt)
    # get=pd.DataFrame.from_dict(aoi_list, orient='index')
    # print(get)
    plt.plot(aoi_list)
    plt.show()
