# PERO
Ns = 20000  # Number of cells in series
A = (0.53 * Ns) + (
    ((0.53 * Ns) / 100) * 15
)  # Area of the solar cell in cm² + 15 % for connection and deviced
A_cell = 0.49
I_0 = (7.6 / (10 ** (15)))*A_cell
Isc_ref = (22.3 / 1000) *A_cell  # A for 700 nm thickness

rs = 1.7
rsh = 1000 # calculated was 6230
eg = (1.636 * 1.602176634) / (10 ** 19)  # eV
n = 1.5
temp_ref = 25  # °C
alpha = -0.0017  # 1/K  temperature coefficient of Jsc

losses = 20  # 5% CTM losses + 5 % cell connection losses
p_mp = 0.00919 * Ns
EQE_filename = "CHEN_2020_EQE_curve_pero_corrected.csv"
