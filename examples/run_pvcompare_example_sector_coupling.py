import os
from pvcompare import main
from pvcompare import constants


# DEFINE USER INPUTS
latitude = 52.5243700  # Madrid: 40.416775 # berlin: 52.5243700 oslo: 59.9127300 athens: 37.983810, Paris: 48.864716
longitude = 13.4105300  # M: -3.703790 # berlin 13.4105300 oslo:10.7460900 	athens: 23.727539, paris: 2.349014
year = 2017
storeys = 5
country = "Germany"
scenario_name = "Scenario_example_sector_coupling"

# DEFAULT PARAMETERS
user_inputs_pvcompare_directory = constants.EXAMPLE_USER_INPUTS_PVCOMPARE
static_inputs_directory = None
user_inputs_mvs_directory = constants.EXAMPLE_USER_INPUTS_MVS_SECTOR_COUPLING
pv_setup = None
outputs_directory = constants.EXAMPLE_OUTPUTS_DIRECTORY

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
