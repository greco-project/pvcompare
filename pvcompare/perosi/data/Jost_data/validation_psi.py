# Carga y Procesado de Datos sin influencia de la Temperatura Ambiente
import numpy as np
import regression_analysis as reg

# Cálculos de la Masa de Aire
import numpy as np
import pvlib
import pandas as pd
import datetime
import pvlib_CPVsystem as cpv
import math
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly


df = pd.read_csv(
    "/home/local/RL-INSTITUT/inia.steinbach/rl-institut/04_Projekte/220_GRECO/03-Projektinhalte/AP4_High_Penetration_of_Photovoltaics/T4_2_Perovskit-Silicon/Data_Marko/RE%3a_AM-abh%c3%a4ngiger_Eenrgieertrag_von_Perowskit-Tandemsolarzellen/complete_dataset_colorado_filtered.csv",
    sep=",",
    index_col=0,
)

# div = pd.read_csv('/home/local/RL-INSTITUT/inia.steinbach/rl-institut/04_Projekte/220_GRECO/03-Projektinhalte/AP4_High_Penetration_of_Photovoltaics/T4_2_Perovskit-Silicon/Data_Marko/RE%3a_AM-abh%c3%a4ngiger_Eenrgieertrag_von_Perowskit-Tandemsolarzellen/IV_curve_only.csv',
#                   sep=',', index_col=None)

# na=pvlib_CPVsystem.fit_sde_sandia(V=div['V'], I=div['I'], Voc=-1.77, Isc=19.45, Vmp=-1.48, Imp=19.92, vlim=0.4, ilim=0.3)


module_params = {
    "gamma_ref": 2.4,  # todo: The diode ideality factor
    "mu_gamma": 0.0,  # todo: The temperature coefficient for the diode ideality factor, 1/K
    "I_L_ref": 24,  # todo: correct this number
    "I_L": 20.601,
    #                'I_o': 0.000000000006934,
    "I_o_ref": 0.000000000005,  # todo: correct this number
    "R_sh_0": 2000,  # todo: correct this number
    "R_sh_ref": 5000,  # todo: correct this number
    "R_sh": 3.357,
    "R_s": 0.007094,
    "alpha_sc": 0.01,
    "cells_in_series": 1,
    "p_mp": 26.515789,
    "I_mp": 17.916074,
    "V_mp": -1.48,
    "i_sc": 19.451288,
    "v_sc": -1.769,
}

# module_params = {'gamma_ref' : 5.524, 'mu_gamma' : 0.003, 'I_L_ref' : 0.96,
#                  'I_o_ref' : 0.00000000017, 'R_sh_ref' : 5226,
#                  'R_sh_0': 21000, 'R_sh_exp' : 5.50, 'R_s' : 0.01,
#                  'alpha_sc' : 0.00, 'EgRef' : 3.91, 'irrad_ref' : 1000,
#                  'temp_ref' : 25, 'cells_in_series' : 12, 'eta_m' : 0.32,
#                  'alpha_absorption' : 0.9}

csys = cpv.StaticCPVSystem(
    module=None,
    module_parameters=module_params,
    modules_per_string=1,
    strings_per_inverter=1,
    inverter=None,
    inverter_parameters=None,
    racking_model="freestanding",
    losses_parameters=None,
    name=None,
)
df["temp"] = 0
celltemp = csys.pvsyst_celltemp(df["GHI"], df["temp"], df["wind speed"])
celltemp = 0

(
    photocurrent,
    saturation_current,
    resistance_series,
    resistance_shunt,
    nNsVth,
) = csys.calcparams_pvsyst(df["DNI"], celltemp)

csys.diode_params = (
    photocurrent,
    saturation_current,
    resistance_series,
    resistance_shunt,
    nNsVth,
)

csys.dc = csys.singlediode(
    photocurrent, saturation_current, resistance_series, resistance_shunt, nNsVth
)

real_power = df["output"]
estimation = csys.dc["p_mp"]


plt.plot(real_power, "r--")
plt.plot(estimation, "b--")
plt.show()


thld_am = 1.5454089143794985
m_low_am = 0.6237142857142854
m_high_am = 0.006807868601986238
thld_temp = 200
m_low_temp = 0.017495740078881793
m_high_temp = 0.0

uf_am = []
for i, v in df["relative_airmass"].items():
    uf_am.append(cpv.get_single_util_factor(v, thld_am, m_low_am, m_high_am))

uf_temp = []
for i, v in df["temp"].items():
    uf_temp.append(cpv.get_single_util_factor(v, thld_temp, m_low_temp, m_high_temp))


weight_am_final = 1.0
rmsd = 10000
rmsd_list = []

for weight_am in np.arange(0, 1, 0.05):
    weight_temp = 1.0 - weight_am

    modeled_power = estimation * (
        np.multiply(weight_am, uf_am) + np.multiply(weight_temp, uf_temp)
    )
    rmsd_temp = math.sqrt(mean_squared_error(real_power, modeled_power))
    rmsd_list.append(rmsd_temp)
    if rmsd_temp < rmsd:
        weight_am_final = weight_am
        weight_temp_final = weight_temp
        rmsd = rmsd_temp

print(weight_am_final, weight_temp_final)


modeled_power = estimation * (
    np.multiply(weight_am_final, uf_am) + np.multiply(weight_temp_final, uf_temp)
)

residualUF = modeled_power - real_power
residualwithoutUF = estimation - real_power

plt.plot(real_power, "r--", label="real_power")
plt.plot(estimation, "g", label="estimation")
plt.plot(modeled_power, "b", label="modeled_power")
plt.xlabel("Time in Days")
plt.ylabel("Power in W")
plt.legend()
plt.show()

p1 = poly.polyfit(real_power, modeled_power, 1)

plt.plot(real_power, real_power, "g", label="real power")
plt.plot(
    real_power,
    modeled_power,
    "bo",
    markersize=1,
    label="modeled_power with UF over measured power",
)
plt.plot(
    real_power,
    estimation,
    "ro",
    markersize=1,
    label="modeled_power_without UF over measured power",
)
plt.plot(real_power, poly.polyval(real_power, p1), "y-", label="model_power_fit")
plt.xlabel("Power in W")
plt.ylabel("Power in W")
plt.legend()
plt.show()
#
#
# plt.plot(df['relative_airmass'], residualwithoutUF, 'go', markersize=1, label='Airmass residual without UF')
# plt.plot(df['relative_airmass'].fillna(0), residualUF, 'ro', markersize=1, label='Airmass residual with UF')
# plt.xlabel("Airmass")
# plt.ylabel("Residual Pmpp in %")
# plt.legend()
# plt.show()
#
#
# plt.plot(df['temp'], residualUF, 'ro', markersize=1, label='Temperature residual with UF')
# plt.plot(df['temp'], residualwithoutUF, 'go', markersize=1, label='Temperature residual without UF')
# plt.xlabel("Air Temperature in T")
# plt.ylabel("Residual Pmpp in %")
# plt.legend()
# plt.show()
