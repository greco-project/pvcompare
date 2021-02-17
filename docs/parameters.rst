.. _parameters:

Parameters of pvcompare: Definitions and Default Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Within the ``pvcompare/pvcompare/data/`` directory, two separate categories of inputs can be observed.

1. *MVS* parameters (found in the CSVs within the ``data/mvs_inputs/csv_elements/`` directory)
2. *pvcompare*-specific parameters (found in the CSVs within the ``data/inputs`` directory)


1. MVS Parameters
=================

As *pvcompare* makes use of the `Multi-vector Simulation (MVS) <https://github.com/rl-institut/mvs_eland>`_ tool, the definitions of all the
relevant parameters of *MVS* can be found in the `documentation of MVS <https://mvs-eland.readthedocs.io/en/latest/MVS_parameters.html>`_.

The values used by default in *pvcompare* for the above parameters in each CSV, are detailed below.
Some parameters can be calculated automatically by *pvcompare* and do not need to be filled it by hand. These parameters are marked with * *auto_calc*.

* project_data.csv
    1. **country**: str, Spain (the country in which the project is located), * *auto_calc*
    2. **label**: str, project_data
    3. **latitude**: str, 45.641603 * *auto_calc*
    4. **longitude**: str, 5.875387 * *auto_calc*
    5. **project_id**: str, 1
    6. **project_name**: str, net zero energy community
    7. **scenario_description**: str, Simulation of scenario scenario_name

* economic_data.csv
    1. **curency**: str, EUR (stands for euro; can be replaced by SEK, if the system is located in Sweden, for instance).
    2. **discount_factor**: factor, 0.06 (most recent data is from 2018, as documented by this market `survey <https://www.grantthornton.co.uk/insights/renewable-energy-discount-rate-survey-2018/>`_.
    3. **label**: str, economic_data
    4. **project_duration**: year, 1 (number of years)
    5. **tax**: factor, 0 (this feature has not been implemented yet, as per MVS documentation)

* simulation_settings.csv
    1. **evaluated_period**: days, 365 (number of days),  * *auto_calc*
    2. **label**: str, simulation_settings
    3. **output_lp_file**: bool, False
    4. **restore_from_oemof_file**: bool, False
    5. **start_date**: str, 2013-01-01 00:00:00,  * *auto_calc*
    6. **store_oemof_results**: bool, True
    7. **timestep**: minutes, 60 (hourly time-steps, 60 minutes)
    8. **display_nx_graph**: bool, False
    9. **store_nx_graph**: bool ,True

* fixcost.csv
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    |                      |        Unit       |        distribution_grid         | engineering      |       operation       |
    +======================+===================+==================================+==================+=======================+
    |  **age_installed**   | 	    year       |               10                 |         0        |           0           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    | **development_costs**|      currency     |               10                 |         0        |           0           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    |  **specific_cost**   |      currency     |               10                 |         0        |         4600          |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    |       **label**      |         str       | distribution grid infrastructure | R&D, engineering | Fix project operation |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    |     **lifetime**     |        year       |               30                 |        20        |          20           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    | **specific_cost_om** |    currency/year  |               10                 |         0        |           0           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    |  **dispatch_price**  |    currency/kWh   |                0                 |         0        |           0           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
* energyConsumption.csv
    1. **dsm**: str, False (dsm stands for Demand Side Management. This feature has not been implement in MVS as of now.)
    2. **file_name**: str, electricity_load.csv
    3. **label**: str, Households
    4. **type_asset**: str, demand
    5. **type_oemof**: str, sink
    6. **energyVector**: str, Electricity
    7. **inflow_direction**: str, Electricity
    8. **unit**: str, kW

* energyConversion.csv
    1. **age_installed**: year, 0 (for all components such as charge controllers, inverters, heat pumps, gas boilers)
    2. **development_costs**: currency, 0 (for all components)
    3. **specific_costs**: currency/kW
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 46 (According to this `source <https://alteredenergy.com/wholesale-cost-of-solar-charge-controllers/>`_, a 12 Volts, 80 Amperes Solar Charge Controller costs about 50 USD, which is about 46 €/kW.)
        b. **solar_inverter_01**: 230 (Per `this <https://www.solaranlage-ratgeber.de/photovoltaik/photovoltaik-wirtschaftlichkeit/photovoltaik-anschaffungskosten>`_, the cost of inverters are around 230 Euro/kW.)
        c. **heat_pump_air_air_2015**: 450 (According to `Danish energy agency's technology data of an air-to-air heat pump [dea_hp_aa] <https://ens.dk/sites/ens.dk/files/Analyser/technology_data_catalogue_for_individual_heating_installations.pdf>`_ on page 87.)
        d. **heat_pump_air_air_2020**: 425 (According to dea_hp_aa)
        e. **heat_pump_air_air_2030**: 316.67 (According to dea_hp_aa)
        f. **heat_pump_air_air_2050**: 300 (According to dea_hp_aa)
        g. **heat_pump_air_water_2015**: 1000 (According to `Danish energy agency's technology data of an air-to-air heat pump [dea_hp_aw] <https://ens.dk/sites/ens.dk/files/Analyser/technology_data_catalogue_for_individual_heating_installations.pdf>`_ on page 89.)
        h. **heat_pump_air_water_2020**: 940 (According to dea_hp_aw)
        i. **heat_pump_air_water_2030**: 850 (According to dea_hp_aw)
        j. **heat_pump_air_water_2050**: 760 (According to dea_hp_aw)
        k. **heat_pump_brine_water_2015**: 1600 (According to `Danish energy agency's technology data of an air-to-air heat pump [dea_hp_bw] <https://ens.dk/sites/ens.dk/files/Analyser/technology_data_catalogue_for_individual_heating_installations.pdf>`_ on page 93.)
        l. **heat_pump_brine_water_2020**: 1500 (According to dea_hp_bw)
        m. **heat_pump_brine_water_2030**: 1400 (According to dea_hp_bw)
        n. **heat_pump_brine_water_2050**: 1200 (According to dea_hp_bw)
        o. **natural_gas_boiler_2015**: 320 (According to `Danish energy agency's technology data of a natural gas boiler [dea_ngb] <https://ens.dk/sites/ens.dk/files/Analyser/technology_data_catalogue_for_individual_heating_installations.pdf>`_ on page 36.)
        p. **natural_gas_boiler_2020**: 310 (According to dea_ngb)
        q. **natural_gas_boiler_2030**: 300 (According to dea_ngb)
        r. **natural_gas_boiler_2050**: 270 (According to dea_ngb)
    4. **efficiency**: factor
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 1
        b. **solar_inverter_01**: 0.95 (European efficiency is around 0.95, per several sources. `Fronius <https://www.fronius.com/en/photovoltaics/products>`_, for example.)
        c. **heat_pump**: "{'file_name': 'None', 'header': 'no_unit', 'unit': ''}"
        d. **natural_gas_boiler_2015**: 0.97 (According to dea_ngb)
        e. **natural_gas_boiler_2020**: 0.97 (According to dea_ngb)
        f. **natural_gas_boiler_2030**: 0.98 (According to dea_ngb)
        g. **natural_gas_boiler_2050**: 0.99 (According to dea_ngb)
    5. **inflow_direction**: str
        a. **storage_charge_controller_in**: Electricity
        b. **storage_charge_controller_out**: ESS Li-Ion
        c. **solar_inverter_01**: PV bus1 (if there are more inverters such as **solar_inverter_02**, then the buses from which the electricity flows into the inverter happens, will be named accordingly. E.g.: PV bus2.)
        d. **heat_pump**: Electricity bus
        e. **natural_gas_boiler**: Gas bus
    6. **installedCap**: kW, 0 (for all components)
    7. **label**: str
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: Charge Contoller ESS Li-Ion (charge)
        b. **solar_inverter_01**: Solar inverter 1 (if there are more inverters, then will be named accordingly. E.g.: Solar inverter 2)
    8. **lifetime**: year
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 15 (According to this `website <https://www.google.com/url?q=https://solarpanelsvenue.com/what-is-a-charge-controller/&sa=D&ust=1591697986335000&usg=AFQjCNE54Zbsv-Gd2UZb-_SY_QNG5Ig2fQ>`_, the lifetime of charge controllers is around 15 years.)
        b. **solar_inverter_01**: 10 (`Lifetime <https://thosesolarguys.com/how-long-do-solar-inverters-last/>`_ of solar (string) inverters is around 10 years.)
        c. **heat_pump_air_air**: 12 (According to dea_hp_aa)
        d. **heat_pump_air_water**: 18 (According to dea_hp_aw)
        e. **heat_pump_brine_water**: 20 (According to dea_hp_bw)
        f. **natural_gas_boiler**: 20 (According to dea_ngb)
    9. **specific_costs_om**: currency/kW
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 0 (According to `AM Solar <https://amsolar.com/diy-rv-solar-instructions/edmaintenance>`_, maintainence work on charge controllers is minimal. So we can consider the costs to be covered by specific_cost_om in fixcost.csv, which is just the system O&M cost.)
        b. **solar_inverter_01**: 6 (From page 11 in this 2015 Sandia `document <https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/2016/160649r.pdf>`_, assuming one maintainence activity per year, we can take 7 USD/kW or 6 €/kW.)
        c. **heat_pump_air_air_2015**: 42.5 (According to dea_hp_aa)
        d. **heat_pump_air_air_2020**: 40.5 (According to dea_hp_aa)
        e. **heat_pump_air_air_2030**: 24.33 (According to dea_hp_aa)
        f. **heat_pump_air_air_2050**: 22 (According to dea_hp_aa)
        g. **heat_pump_air_water_2015**: 29.1 (According to dea_hp_aw)
        h. **heat_pump_air_water_2020**: 27.8 (According to dea_hp_aw)
        i. **heat_pump_air_water_2030**: 25.5 (According to dea_hp_aw)
        j. **heat_pump_air_water_2050**: 23.9 (According to dea_hp_aw)
        k. **heat_pump_brine_water_2015**: 29.1 (According to dea_hp_bw)
        l. **heat_pump_brine_water_2020**: 27.8 (According to dea_hp_bw)
        m. **heat_pump_brine_water_2030**: 25.5 (According to dea_hp_bw)
        n. **heat_pump_brine_water_2050**: 23.9 (According to dea_hp_bw)
        o. **natural_gas_boiler_2015**: 20.9 (According to dea_ngb)
        p. **natural_gas_boiler_2020**: 20.5 (According to dea_ngb)
        q. **natural_gas_boiler_2030**: 19.9 (According to dea_ngb)
        r. **natural_gas_boiler_2050**: 18.1 (According to dea_ngb)
    10. **dispatch_price**: currency/kWh, 0 (for all components)
    11. **optimizeCap**: bool, True (for all components)
    12. **outflow_direction**: str
         a. **storage_charge_controller_in**: ESS Li-Ion
         b. **storage_charge_controller_out**: Electricity
         c. **solar_inverter_01**: Electricity (if there are more solar inverters, this value applies for them as well)
         d. **heat_pump**: Heat bus
         e. **natural_gas_boiler**: Heat bus
    13. **energyVector**: str
         a. **storage_charge_controller_in**: Electricity
         b. **storage_charge_controller_out**: Electricity
         c. **solar_inverter_01**: Electricity
         d. **heat_pump**: Heat
         e. **natural_gas_boiler**: eHeat (Because of convention to define energyVector based on output flow for an energy conversion asset. See `mvs documentation on parameters <https://multi-vector-simulator.readthedocs.io/en/stable/MVS_parameters.html#list-of-parameters>`_)
    14. **type_oemof**: str, transformer (same for all the components)
    15. **unit**: str, kW (applies to all the components)

* energyProduction.csv:
    1. **age_installed**: year, 0 (for all the components)
    2. **development_costs**: currency, 0 (**TO BE DECIDED**)
    3. **specific_costs**: currency/unit, (**TO BE DECIDED**)
    4. **file_name**: str,  * *auto_calc*
        a. **pv_plant_01**: si_180_31.csv
        b. **pv_plant_02**: cpv_180_31.csv
        c. **pv_plant_03**: cpv_90_90.csv
    5. **installedCap**: kWp, 0.0 (for all components)
    6. **maximumCap**: kWp  * *auto_calc*
        a. **pv_plant_01**: 25454.87
        b. **pv_plant_02**: 55835.702
        c. **pv_plant_03**: 23929.586
    7. **label**: str
        a. **pv_plant_01**: PV si_180_31
        b. **pv_plant_02**: PV cpv_180_31
        c. **pv_plant_03**: PV cpv_90_90
    8. **lifetime**: year, 25 (for all the components)
    9. **specific_costs_om**: currency/unit, 50 (same for all the components; 50 €/kWp is the value that is arrived at after accounting for the yearly inspection and cleaning. Here is the detailed `explanation <https://github.com/greco-project/pvcompare/issues/13>`_.)
    10. **dispatch_price**: currency/kWh, 0 (this is because there are no fuel costs associated with Photovoltaics)
    11. **optimizeCap**: bool, True (for all components)
    12. **outflow_direction**: str, PV bus1 (for all of the components)
    13. **type_oemof**: str, source (for all of the components)
    14. **unit**: str, kWp (for all of the components)
    15. **energyVector**: str, Electricity (for all of the components)
* energyProviders.csv:
    1. **energy_price**: currency/kWh,
        a. **Electricity grid**: 0.24  * *auto_calc* (0.24 €/kWh is the average household electricity price of Spain for 2019S1. Obtained from `Eurostat <https://ec.europa.eu/eurostat/statistics-explained/images/d/d9/Electricity_prices%2C_first_semester_of_2017-2019_%28EUR_per_kWh%29.png>`_.)
        b. **Gas plant**: 0.0598 * *auto_calc* (0,0598 €/kWh for Germany and 0.072 €/kWh for Spain (2019 / 2020) - Values read in depending on location obtained from `Eurostat's statistic of gas prices <https://ec.europa.eu/eurostat/databrowser/view/ten00118/default/table?lang=en>`_)
    2. **feedin_tariff**: currency/kWh,
        a. **Electricity grid**: (0.10 €/kWh is for Germany. We do not have data for Spain yet.)
        b. **Gas plant**: 0
    3. **inflow_direction**: str,
        a. **Electricity grid**: Electricity
        b. **Gas plant**: Gas bus
    4. **label**: str, Electricity grid feedin
    5. **optimizeCap**: bool, True (for all of the components)
    6. **outflow_direction**: str,
        a. **Electricity grid**: Electricity
        b. **Gas plant**: Heat bus
    7. **peak_demand_pricing**: currency/kW, 0 (for all of the components)
    8. **peak_demand_pricing_period**: 	times per year (1,2,3,4,6,12), 1 (for all of the components)
    9. **type_oemof**: str, source (for all of the components)
    10. **energyVector**: str,
        a. **Electricity grid**: Electricity
        b. **Gas plant**: Heat
    11. **emission factor**: kgCO2eq/kWh
        a. **Electricity grid**: 0.338
        b. **Gas plant**: 1.9 (Obtained from `mvs documentation of emission factors <https://multi-vector-simulator.readthedocs.io/en/stable/Model_Assumptions.html#emission-factors>`_.)
* energyStorage.csv:
    1. **inflow_direction**: str, ESS Li-Ion
    2. **label**: str, ESS Li-Ion
    3. **optimizeCap**: bool, True
    4. **outflow_direction**: str, ESS Li-Ion
    5. **type_oemof**: str, storage
    6. **storage_filename**: str, storage_01.csv
    7. **energyVector**: str, Electricity
* storage_01.csv:
    1. **age_installed**: year, 0 (for all components)
    2. **development_costs**: currency, 0 (for all components)
    3. **specific_costs**: currency/unit
        a. **storage capacity**: 0.2 (Consult this reference `<https://www.energieheld.de/solaranlage/photovoltaik/kosten#vergleich>`_ for details.)
        b. **input power** and **output power**: 0
    4. **c_rate**: factor of total capacity (kWh)
        a. **storage capacity**: NA (does not apply)
        b. **input power** and **output power**: 1 (this just means that the whole capacity of the battery would be used during charging and discharging cycles)
    5. **efficiency**: factor
        a. **storage capacity**: 0
        b. **input power** and **output power**: 0.9 (Charging and discharging efficiency. The value has been sourced from this `page <https://en.wikipedia.org/wiki/Lithium-ion_battery>`_.)
    6. **installedCap**: unit, 0 (applies for all the parameters of the battery storage)
    7. **label**: str, Same as the column headers (storage capacity, input power, output power)
    8. **lifetime**: year, 10 (applies for all the parameters of the battery storage)
    9. **specific_costs_om**: currency/unit/year, 0 (applies for all the parameters of the battery storage)
    10. **dispatch_price**: currency/kWh

        a. **storage capacity**: NA (does not apply)

        b. **input power** and **output power**: 0
    11. **soc_initial**: None or factor

        a. **storage capacity**: None

        b. **input power** and **output power**: NA
    12. **soc_max**: factor

        a. **storage capacity**: 0.8 (Took the Fronius 4.5 battery which has a rated capacity 4.5 kW, but 3.6 kW is the usable capacity.So SoC max would be 80% or 0.8.)

        b. **input power** and **output power**: NA
    13. **soc_min**: factor

        a. **storage capacity**: 0.1 (Figure from this research `article <https://www.sciencedirect.com/science/article/pii/S0378775319310043>`_.)

        b. **input power** and **output power**: NA
    14. **unit**: str
        a. **storage capacity**: kWh

        b. **input power** and **output power**: kW

* storage_02.csv:
    1. **age_installed**: year, 0 (for all components of the stratified thermal storage)
    2. **development_costs**: currency, 0 (for all components of the stratified thermal storage)
    3. **specific_costs**: currency/unit
        a. **storage capacity**: 410, See `Danish energy agency's technology data of small-scale hot water tanks [dea_swt] <https://ens.dk/sites/ens.dk/files/Analyser/technology_data_catalogue_for_energy_storage.pdf>`_ on p.66 - However investment costs of stratified TES could be higher.
        b. **input power** and **output power**: 0
    4. **c_rate**: factor of total capacity (kWh)
        a. **storage capacity**: NA (does not apply)
        b. **input power** and **output power**: 1 (this just means that the whole capacity of the stratified thermal storage would be used during charging and discharging cycles)
    5. **efficiency**: factor
        a. **storage capacity**: 1, or "NA" if calculated
        b. **input power** and **output power**: 1
    6. **installedCap**: unit 0, or "NA" if calculated
        a. **storage capacity**: 0, or "NA" if calculated
        b. **input power** and **output power**: 0
    7. **lifetime**: year, 30 (applies for all the parameters of the stratified thermal energy storage)
    8. **specific_costs_om**: currency/unit/year
        a. **storage capacity**: 16.67, [dea_swt] p.66 - however fix om costs of stratified TES could differ
        b. **input power** and **output power**: 0
    9. **dispatch_price**: currency/kWh
        a. **storage capacity**: NA (does not apply)
        b. **input power** and **output power**: 0
    10. **soc_initial**: None or factor

        a. **storage capacity**: None

        b. **input power** and **output power**: NA
    11. **soc_max**: factor

        a. **storage capacity**: 0.925 (7.5% unused volume see `European Commission study large-scale heating and cooling in EU [EUC_heat] <https://op.europa.eu/en/publication-detail/-/publication/312f0f62-dfbd-11e7-9749-01aa75ed71a1/language-en>`_ p.168 - This applies for large scale TES but could be validated for a small scale storage too.)

        b. **input power** and **output power**: NA
    12. **soc_min**: factor

        a. **storage capacity**: 0.075 (7.5% unused volume see [EUC_heat] p.168 - This applies for large scale TES but could be validated for a small scale storage too.)

        b. **input power** and **output power**: NA
    13. **unit**: str

        a. **storage capacity**: kWh

        b. **input power** and **output power**: kW
    14. **fixed_thermal_losses_relative**: factor

        a. **storage capacity**: "{'file_name': 'None', 'header': 'no_unit', 'unit': ''}", is calculated in pvcompare

        b. **input power** and **output power**: NA (does not apply)
    15. **fixed_thermal_losses_absolute**: kWh

        a. **storage capacity**: "{'file_name': 'None', 'header': 'no_unit', 'unit': ''}", is calculated in pvcompare

        b. **input power** and **output power**: NA (does not apply)



2. pvcompare-specific parameters
================================

In order to run *pvcompare*, a number of input parameters are needed; many of which are stored in csv files with default values in ``pvcompare/pvcompare/inputs/``.
The following list will give a brief introduction into the description of the csv files and the source of the given default parameters.

* pv_setup.csv:
    *The pv_setup.csv defines the number of facades that are covered with pv-modules.*

    1. **surface_type**: str, optional values are "flat_roof", "gable_roof", "south_facade", "east_facade" and "west_facade"
    2. **surface_azimuth**: integer, between -180 and 180, where 180 is facing south, 90 is facing east and -90 is facing west
    3. **surface_tilt**: integer, between 0 and 90, where 90 represents a vertical module and 0 a horizontal.
    4. **technology**: str, optional values are "si" for a silicone module, "cpv" for concentrator photovoltaics and "psi" for a perovskite silicone module

* building_parameters:
    *Parameters that describe the characteristics of the building that should be considered in the simulation. The default values are taken from [1].*

    1. **number of storeys**: int
    2. **population per storey**: int, number of habitants per storey
    3. **total storey area**: int, total area of one storey, equal to the flat roof area in m²
    4. **length south facade**: int, length of the south facade in m
    5. **length eastwest facade**:int, length of the east/west facade in m
    6. **hight storey**: int, hight of each storey in m
    7. **room temperature**: int, average room temperature inside the building, default: 20 °C
    8. **heating limit temperature**: int, temperature limit for space heating in °C, default: `15 °C <http://wiki.energie-m.de/Heizgrenztemperatur>`_
    9. **include warm water**: bool, condition about whether warm water is considered or not, default: False
    10. **filename_total_consumption**: str, name of the csv file that contains the total electricity and heat consumption for EU countries in different years from [2] *
    11. **filename_total_SH**: str, name of the csv file that contains the total space heating for EU countries in different years [2] *
    12. **filename_total_WH**: str, name of the csv file that contains the total water heating for EU countries in different years [2] *
    13. **filename_elect_SH**: str, name of the csv file that contains the electrical space heatig for EU countries in different years [2] *
    14. **filename_elect_WH**: str, name of the csv file that contains the electrical water heating for EU countries in different years [2] *
    15. **filename_residential_electricity_demand**: str, name of the csv file that contains the total residential electricity demand for EU countries in different years [2] *
    16. **filename_country_population**: str, name of the csv file that contains population for EU countries in different years [2] *

* heat_pumps_and_chillers:
    *Parameters that describe characteristics of the heat pumps and chillers in the simulated energy system.*

    1. **mode**: str, options: 'heat_pump' or 'chiller'
    2. **quality_grade**: float, scale-down factor to determine the COP of a real machine, default: heat pump: 0.35, chiller 0.3 (Obtained from `monitored data <https://oemof-thermal.readthedocs.io/en/latest/validation_compression_heat_pumps_and_chillers.html>`_ of the GRECO project)
    3. **temp_high**: float, temperature in °C of the sink (external outlet temperature at the condenser), default: heat pump: 35 (For the heat pump temp_high has been chosen from the highest value of the evaporators temperature in the `monitored data <https://oemof-thermal.readthedocs.io/en/latest/validation_compression_heat_pumps_and_chillers.html>`_. )
    4. **temp_low**: float, temperature in °C of the source (external outlet temperature at the evaporator), default: chiller: 15 (The low temperature has been set for now to 15° C, a temperature lower the comfort temperature of 20–22 °C. The chiller has not been implemented in the model yet. However, should it been done so in the future, these temperatures must be researched and adjusted.)
    5. **factor_icing**: float or None, COP reduction caused by icing, only for `mode` 'heat_pump', default: None
    6. **temp_threshold_icing**: float or None, Temperature below which icing occurs, only for `mode` 'heat_pump', default: None

* list_of_workalendar:
    *list of countries for which a python.workalendar [3] exists with the column name "country".*



[1] Hachem, 2014: Energy performance enhancement in multistory residential buildings. DOI: 10.1016/j.apenergy.2013.11.018

[2] EUROSTAT: https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use

[3] Workalendar https://pypi.org/project/workalendar/

\* the described csv files are to be added to the input folder accordingly.
