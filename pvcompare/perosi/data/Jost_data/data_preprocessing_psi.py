# Carga y Procesado de Datos sin influencia de la Temperatura Ambiente
import numpy as np
import regression_analysis as reg
import pandas as pd

# Cálculos de la Masa de Aire
import numpy as np
import pvlib
import datetime

data = pd.read_csv(
    "/home/local/RL-INSTITUT/inia.steinbach/rl-institut/04_Projekte/220_GRECO/03-Projektinhalte/AP4_High_Penetration_of_Photovoltaics/T4_2_Perovskit-Silicon/Data_Marko/RE%3a_AM-abh%c3%a4ngiger_Eenrgieertrag_von_Perowskit-Tandemsolarzellen/complete_dataset_colorado_filtered.csv",
    sep=",",
    index_col=0,
)

panel_location = pvlib.location.Location(
    latitude=39.21, longitude=-106.3, tz="America/Swift_Current", altitude=3036
)

# airmass = data['relative_airmass']

fixtemp = pd.read_csv(
    "/home/local/RL-INSTITUT/inia.steinbach/rl-institut/04_Projekte/220_GRECO/03-Projektinhalte/AP4_High_Penetration_of_Photovoltaics/T4_2_Perovskit-Silicon/Data_Marko/RE%3a_AM-abh%c3%a4ngiger_Eenrgieertrag_von_Perowskit-Tandemsolarzellen/complete_dataset_colorado_fixtemp.csv",
    sep=",",
    index_col=0,
)

fixtemp_Pmp = fixtemp["output"]
fixtemp_am = fixtemp["relative_airmass"]

median_df = pd.Series()
for j in np.arange(1, 5, 0.1):
    am_data = fixtemp[
        (fixtemp["relative_airmass"] > j - 0.05)
        & (fixtemp["relative_airmass"] > j + 0.05)
    ]
    median_df[j] = am_data["output"].median()
    median_Isc = median_df.tolist()

m_low_am, n_low_am, m_high_am, n_high_am, thld_am = reg.calc_two_regression_lines(
    median_df.index, median_Isc, limit=1.6
)
# m_low, n_low, error1 = calc_regression_line(Airmass_aux[:10],
# IscDNI_medians[:10])
# m_high, n_high, error2 = calc_regression_line(Airmass_aux[10:],
# IscDNI_medians[10:])
# thld = (n_high - n_low) / (m_low - m_high)

x1 = np.arange(1, 5, 0.1)
y1 = m_low_am * x1 + n_low_am
x2 = np.arange(4, 12, 0.1)
y2 = m_high_am * x2 + n_high_am

import matplotlib.pyplot as plt

plt.plot(
    fixtemp_am,
    fixtemp_Pmp,
    "b+",
    median_df.index,
    median_df,
    "r.",
    x1,
    y1,
    "g",
    x2,
    y2,
    "r",
)
plt.show()

IscDNI_ast = 20
uf_am = pd.Series()

print(
    "thld_am = ",
    thld_am,
    "\n" "m_low_am = ",
    m_low_am / IscDNI_ast,
    "\n" "m_high_am = ",
    m_high_am / IscDNI_ast,
)

for i, row in data.iterrows():
    uf_am[i] = reg.get_single_util_factor(
        row["relative_airmass"], thld_am, m_low_am / IscDNI_ast, m_high_am / IscDNI_ast
    )

# Carga y Procesado de Datos sin influencia de la Masa de Aire

fixairmass = pd.read_csv(
    "/home/local/RL-INSTITUT/inia.steinbach/rl-institut/04_Projekte/220_GRECO/03-Projektinhalte/AP4_High_Penetration_of_Photovoltaics/T4_2_Perovskit-Silicon/Data_Marko/RE%3a_AM-abh%c3%a4ngiger_Eenrgieertrag_von_Perowskit-Tandemsolarzellen/complete_dataset_colorado_fixairmass.csv",
    sep=",",
    index_col=0,
)

fixairmass_Pmp = fixairmass["output"]
fixairmass_temp = fixairmass["temp"]
m_low, n_low, m_high, n_high, thld = reg.calc_uf_lines(
    fixairmass_temp, fixairmass_Pmp, "temp_air"
)

x = np.arange(-10, 25, 1)
y1 = m_low * x + n_low

plt.plot(fixairmass["temp"], fixairmass["output"], "g+", x, y1, "b")
plt.xlabel("Temperature")
plt.ylabel("Isc/DNI")
plt.show()

uf_at = pd.Series()
for i, row in data.iterrows():
    uf_at[i] = reg.get_single_util_factor(
        row["temp"], thld, m_low / IscDNI_ast, m_high / IscDNI_ast
    )
print(
    "thld_temp = ",
    thld,
    "\n" "m_low_temp = ",
    m_low / IscDNI_ast,
    "\n" "m_high_temp = ",
    m_high / IscDNI_ast,
)
