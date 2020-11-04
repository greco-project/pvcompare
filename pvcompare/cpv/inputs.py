import pandas as pd


mod_params_cpv = {
    "gamma_ref": 5.524,
    "mu_gamma": 0.003,
    "I_L_ref": 0.96,
    "I_o_ref": 0.00000000017,
    "R_sh_ref": 5226,
    "R_sh_0": 21000,
    "R_sh_exp": 5.50,
    "R_s": 0.01,
    "alpha_sc": 0.00,
    "EgRef": 3.91,
    "irrad_ref": 1000,
    "temp_ref": 25,
    "cells_in_series": 12,
    "cells_in_parallel": 48,
    "eta_m": 0.32,
    "alpha_absorption": 0.9,
    "Area": 0.131,
    "v_mp": 33.5,
    "i_mp": 0.893,
    "u_c": 29.0,  # default value from https://pvlib-python.readthedocs.io/en/latest/generated/pvlib.temperature.pvsyst_cell.html#pvlib.temperature.pvsyst_cell
    "u_v": 0.00,
    "alpha": 0.11,  # temperature coefficient for the whole module see INS datasheet not used
    "intended_efficiency": 32
}

UF_parameters_cpv = {
    "IscDNI_top": 0.96 / 1000,
    "am_thld": 4.574231933073185,
    "am_uf_m_low": 3.906372068620377e-06,
    "am_uf_m_high": -3.0335768119184845e-05,
    "ta_thld": 50,
    "ta_uf_m_low": 4.6781224141650075e-06,
    "ta_uf_m_high": 0,
    "weight_am": 0.2,
    "weight_temp": 0.8,
}

mod_params_cpv.update(UF_parameters_cpv)

# example (NO Insolight) PV module from:
# https://pvpmc.sandia.gov/PVLIB_Matlab_Help/html/pvl_calcparams_PVsyst_help.html
mod_params_flatplate = {
    "gamma_ref": 1.1,
    "mu_gamma": -0.0003,
    "I_L_ref": 8,
    "I_o_ref": 2.2e-9,
    "R_sh_ref": 200,
    "R_sh_0": 8700,
    "R_sh_exp": 5.5,
    "R_s": 0.33,
    "alpha_sc": -0.002,
    "EgRef": 1.121,
    "irrad_ref": 1000,
    "temp_ref": 25,
    "cells_in_series": 4,  # 60,
    "eta_m": 0.95,  # pvsyst_celltemp() default value
    "alpha_absorption": 0.97,  # pvsyst_celltemp() default value
    "i_mp": 3.51,
    "v_mp": 1.26,
    "p_mp": 4.44,
}


# elif cpv_type == "m300":
#
#     module_params = {
#         "gamma_ref": 4.456,
#         "mu_gamma": 0.0012,
#         "I_L_ref": 3.346,
#         "I_o_ref": 0.000000000004,
#         "R_sh_ref": 4400,
#         "R_sh_0": 17500,
#         "R_sh_exp": 5.50,
#         "R_s": 0.736,
#         "alpha_sc": 0.00,
#         "irrad_ref": 1000,
#         "temp_ref": 25,
#         "cells_in_series": 42,
#         "v_mp": 116.63,
#         "i_mp": 3.082,
#         "Area": 1.269,
#     }
#
#     UF_parameters = {
#         "IscDNI_top": 1,
#         "thld_am": 2.022411098853249,
#         "m_low_am": 0.0423037910485609,
#         "m_high_am": -0.0210539236615148,
#         "thld_temp": 200,
#         "m_low_temp": 0.000923828521724516,
#         "m_high_temp": 0.0,
#         "weight_am": 0.2,
#         "weight_temp": 0.8,
#     }
# module_params.update(UF_parameters)
