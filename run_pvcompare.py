from pvcompare import main


# DEFINE USER INPUTS
# the following parameters are needed to run pvcompare, you can adapt them to your needs
latitude = 52.5243700
longitude = 13.4105300
year = 2017
storeys = 5
country = "Germany"
scenario_name = "My_Scenario"

# FOR DEFAULT PARAMETERS SEE pvcompare/constants.py
user_inputs_pvcompare_directory = None
static_inputs_directory = None
user_inputs_mvs_directory = None
pv_setup = None
outputs_directory = None

# RUN PVCOMPARE PRE-CALCULATIONS:
# - calculate PV timeseries
# - if sectorcoupling: calculate heat pump generation
# - calculate electricity and heat demand

main.apply_pvcompare(
    storeys=storeys,
    country=country,
    latitude=latitude,
    longitude=longitude,
    year=year,
    static_inputs_directory=static_inputs_directory,
    user_inputs_pvcompare_directory=user_inputs_pvcompare_directory,
    user_inputs_mvs_directory=user_inputs_mvs_directory,
    plot=False,
    pv_setup=pv_setup,
    overwrite_grid_costs=True,
    overwrite_pv_parameters=True,
)

# RUN MVS OEMOF SIMULATTION
main.apply_mvs(
    scenario_name=scenario_name,
    outputs_directory=outputs_directory,
    user_inputs_mvs_directory=user_inputs_mvs_directory,
)
