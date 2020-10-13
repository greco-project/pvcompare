import pvlib

module_params = {
    "alpha_sc": 0.00,
    "a_ref": 0.070984414,
    "I_L_ref": 3.346,
    "I_o_ref": 0.000000000004,
    "R_sh_ref": 4400,
    "R_s": 0.007094,
}

psisys = pvlib.pvsystem.PVSystem(
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

dc = psisys.singlediode(
    photocurrent=20.565332,
    saturation_current=2.0189074e-11,
    resistance_series=0.007094,
    resistance_shunt=3.3576071,
    nNsVth=0.070984414,
    ivcurve_pnts=None,
)


print(dc["p_mp"])
