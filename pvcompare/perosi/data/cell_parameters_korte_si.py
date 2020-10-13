Ns = 2  # Number of cells in series
A = 0.78 * Ns  # Area of the solar cell in cm²
I_0 = (7.1142 / 10 ** (14)) * A
Isc_ref = (39.62 / 1000) * A
ghi_ref = 1000  # W/m²
rs = 3.0 / A
rsh = 981 / A
eg = 1.24 * 1.602176634 / 10 ** 19  # eV -> Volt
n = 1

temp_ref = 25  # °C
alpha = -0.0037  # 1/K  temperature coefficient of Jsc
EQE_filename = "EQE_3T_silicone_measured_corrected.csv"
p_mp = 0.009 * Ns
