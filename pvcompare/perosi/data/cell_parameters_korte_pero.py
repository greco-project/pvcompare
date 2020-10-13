# pero
Ns = 2  # Number of cells in series
A = 0.78 * Ns  # Area of the solar cell in cm²
I_0 = (3.5248 / 10 ** (15)) * A
Isc_ref = (22.6 / 1000) * A
rs = 7.6 / A
rsh = 6230 / A
eg = 1.636 * 1.602176634 / 10 ** 19  # eV
n = 1.5
temp_ref = 25  # °C
alpha = -0.0017  # 1/K  temperature coefficient of Jsc
p_mp = 0.013 * Ns  # Watt/Zelle perovskite + silicone
EQE_filename = "EQE_3T_peroskit_measured_corrected.csv"
