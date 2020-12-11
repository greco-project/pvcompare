from pvcompare import main


#DEFINE USER INPUTS
latitude = 52.5243700  # Madrid: 40.416775 # berlin: 52.5243700 oslo: 59.9127300 athens: 37.983810, Paris: 48.864716
longitude = 13.4105300  # M: -3.703790 # berlin 13.4105300 oslo:10.7460900 	athens: 23.727539, paris: 2.349014
year = 2014
population = 48000
country = "Germany"
scenario_name = "Scenario_Z1"

# DEFAULT PARAMETERS
input_directory=None
mvs_input_directory=None
pv_setup=None
output_directory=None
mvs_input_directory=None

#RUN PVCOMPARE PRE-CALCULATIONS:
# - calculate PV timeseries
# - if sectorcoupling: calculate heat pump generation
# - calculate electricity and heat demand

main.apply_pvcompare(
    population = population,
    country=country,
    latitude=latitude,
    longitude=longitude,
    year=year,
    input_directory=input_directory,
    mvs_input_directory=mvs_input_directory,
    plot=False,
    pv_setup=pv_setup,
)

#RUN MVS OEMOF SIMULATTION
main.apply_mvs(
    scenario_name=scenario_name, output_directory=output_directory,
    mvs_input_directory=mvs_input_directory
)