.. _parameters:

Parameters of pvcompare: Definitions and Default Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Within the ``pvcompare/pvcompare/data/`` directory, two separate categories of inputs can be observed.

1. *MVS* parameters (found in the CSVs within the ``data/user_inputs/mvs_inputs/csv_elements/`` directory)
2. *pvcompare*-specific parameters (found in the CSVs within the ``data/user_inputs/pvcompare_inputs/`` directory)

As *pvcompare* imports the `Multi-vector Simulation (MVS) <https://github.com/rl-institut/mvs_eland>`_ tool, the definitions of all the
relevant parameters of *MVS* can be found in the `documentation of MVS <https://mvs-eland.readthedocs.io/en/latest/MVS_parameters.html>`_.
The default values and it's sources are described below.

The values used by default in *pvcompare* for the above parameters in each CSV, are detailed below.


1. MVS Parameters
=================
Some parameters can be calculated automatically by *pvcompare* and do not need to be filled in by hand. These parameters are marked with * *auto_calc*.


project_data.csv
----------------
    1. **country**: str, Spain (the country in which the project is located), * *auto_calc*
    2. **latitude**: str, 45.641603 * *auto_calc*
    3. **longitude**: str, 5.875387 * *auto_calc*
    4. **project_id**: str, 1
    5. **project_name**: str, net zero energy community
    6. **scenario_id**,str,1
    7. **scenario_name**,str, Scenario_A
    8. **scenario_description**: str, Simulation of scenario scenario_name

economic_data.csv
-----------------
    1. **curency**: str, EUR (stands for euro; can be replaced by SEK, if the system is located in Sweden, for instance).
    2. **project_duration**: year, 25 (number of years).
    3. **discount_factor**: factor, 0.07 (see `discussion paper <http://bpie.eu/wp-content/uploads/2015/10/Discount_rates_in_energy_system-discussion_paper_2015_ISI_BPIE.pdf>`_.)
    4. **tax**: factor, 0 (see `documentation of MVS <https://mvs-eland.readthedocs.io/en/latest/MVS_parameters.html>`_)

simulation_settings.csv
-----------------------
    1. **evaluated_period**: days, 365 (number of days),  * *auto_calc*
    2. **start_date**: str, 2013-01-01 00:00:00,  * *auto_calc*
    3. **timestep**: minutes, 60 (hourly time-steps, 60 minutes)
    4. **output_lp_file**: bool ,False

fixcost.csv
-----------
By default in *pvcompare* no fixcosts are considered. The lifetime of all assets is set to 1 only to prevent errors in MVS. This lifetime has no effect
on the simulation unless costs are defined.


    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    |                      |        Unit       |        distribution_grid         | engineering      |       operation       |
    +======================+===================+==================================+==================+=======================+
    |  **age_installed**   | 	    year       |               0                  |         0        |           0           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    | **development_costs**|      currency     |               0                  |         0        |           0           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    |  **specific_cost**   |      currency     |               0                  |         0        |           0           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    |     **lifetime**     |        year       |               1                  |         1        |           1           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+
    | **specific_cost_om** |    currency/year  |               0                  |         0        |           0           |
    +----------------------+-------------------+----------------------------------+------------------+-----------------------+

energyConsumption.csv
---------------------
    1. **unit**: str, kW
    2. **inflow_direction**: str, Electricity
    3. **file_name**: str, electricity_load_2017_Spain_8.csv, * *auto_calc*
    4. **energyVector**: str, Electricity
    5. **type_oemof**: str, sink
    6. **type_asset**: str, demand
    7. **dsm**: str, False (dsm stands for Demand Side Management. This feature has not been implement in MVS as of now.)

energyConversion.csv
--------------------
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

energyProduction.csv
--------------------
    1. **age_installed**: year, 0 (for all the components)
    2. **development_costs**: currency, 0 (for all the components)
    3. **specific_costs**: currency/unit, 934 (SI), 1019 (CPV) ,813 (PSI)
    4. **file_name**: str, * *auto_calc*
    5. **installedCap**: kWp, 0.0 (for all components)
    6. **maximumCap**: kWp,  * *auto_calc*
    7. **lifetime**: year, 25 (for all the components)
    8. **specific_costs_om**: currency/unit, 20 (SI) ,15 (CPV), 17 (PSI)
    9. **dispatch_price**: currency/kWh, 0 (this is because there are no fuel costs associated with photovoltaics)
    10. **optimizeCap**: bool, True (for all components)
    11. **outflow_direction**: str, PV bus1 (for all of the components)
    12. **type_oemof**: str, source (for all of the components)
    13. **unit**: str, kWp (for all of the components)
    14. **energyVector**: str, Electricity (for all of the components)
    15. **emission_factor**: kgCO2eq/unit, * *auto_calc*
    16. **renewableAsset**: bool, True (for all of the components)

energyProviders.csv
-------------------
All default values of the energy price, feed-in tariff, renewable share and emission factor of European countries are stored in
``data/static_inputs/local_grid_parameters.xlsx``

    1. **unit**: str,kW
    2. **optimizeCap**: bool, True (for all of the components)
    3. **energy_price**: currency/kWh,
        a. **Electricity grid**: * *auto_calc*, `EUROSTAT electricity, <https://ec.europa.eu/eurostat/databrowser/view/ten00117/default/table?lang=en>`_
        b. **Gas plant**: * *auto_calc* `EUROSTAT Gas <https://ec.europa.eu/eurostat/databrowser/view/ten00118/default/table?lang=en>`_
    4. **feedin_tariff**: currency/kWh,
        a. **Electricity grid**: * *auto_calc* `feed-in tariff <https://www.pv-magazine.com/features/archive/solar-incentives-and-fits/feed-in-tariffs-in-europe/>`_
        b. **Gas plant**: 0
    5. **peak_demand_pricing**: currency/kW, 0 (for all of the components)
    6. **peak_demand_pricing_period**: 	times per year (1,2,3,4,6,12), 1 (for all of the components)
    7. **renewable_share**,factor, * *auto_calc* `EUROSTAT renewable share <https://ec.europa.eu/eurostat/web/energy/data/shares>`_
    8. **inflow_direction**: str,
        a. **Electricity grid**: Electricity
        b. **Gas plant**: Gas bus
    9. **outflow_direction**: str,
        a. **Electricity grid**: Electricity
        b. **Gas plant**: Heat bus
    10. **energyVector**: str,
        a. **Electricity grid**: Electricity
        b. **Gas plant**: Heat
    11. **type_oemof**: str, source (for all of the components)

    12. **emission factor**: kgCO2eq/kWh
        a. **Electricity grid**: * *auto_calc* `EEA EUROPA <https://www.eea.europa.eu/data-and-maps/indicators/overview-of-the-electricity-production-3/assessment>`_
        b. **Gas plant**: 0.2 (Obtained from `Quaschning 06/2015 <https://www.volker-quaschning.de/datserv/CO2-spez/index_e.php>`_.)

energyStorage.csv
-----------------
    1. **inflow_direction**: str, ESS Li-Ion
    2. **label**: str, ESS Li-Ion
    3. **optimizeCap**: bool, True
    4. **outflow_direction**: str, ESS Li-Ion
    5. **type_oemof**: str, storage
    6. **storage_filename**: str, storage_01.csv
    7. **energyVector**: str, Electricity

storage_01.csv
--------------
*This storage example describes a battery storage*

    1. **unit**, str, kWh
    2. **installedCap**: unit, 0 (for all components)
    3. **age_installed**: year, 0 (for all components)
    4. **lifetime**: year, 20 (for all components), (see `Moosmoar S.3 <https://iewt2019.eeg.tuwien.ac.at/download/contribution/presentation/112/112_presentation_20190215_102253.pdf>`_)
    5. **development_costs**: currency, 0 (for all components)
    6. **specific_costs**: currency/unit
        a. **storage capacity**: 250 - 550 (`ZHB S.46 ff <https://www.zhb-flensburg.de/fileadmin/content/spezial-einrichtungen/zhb/dokumente/dissertationen/fluri/fluri-2019-wirtschaftlichkeit-dez-stromspeicher.pdf>`_)
        b. **input power** and **output power**: 0
    7. **specific_costs_om**: currency/unit/year
        a. **storage capacity**: 0.2 (`energieheld <https://www.energieheld.de/solaranlage/photovoltaik/stromspeicher/kosten#preis-pro-kilowattstunde-berechnen>`_)
        b. **input power** and **output power**: 0
    8. **dispatch_price**: currency/kWh
        a. **storage capacity**: NA (does not apply)
        b. **input power** and **output power**: 0
    9. **c_rate**: factor of total capacity (kWh)
        a. **storage capacity**: NA (does not apply)
        b. **input power** and **output power**: 1 (this just means that the whole capacity of the battery would be used during charging and discharging cycles)
    10. **efficiency**: factor
        a. **storage capacity**: 1
        b. **input power** and **output power**: 0.95 (Charging and discharging efficiency. The value has been sourced from `MVS efficiency <https://multi-vector-simulator.readthedocs.io/en/stable/MVS_parameters.html#efficiency-label>`_.)
    11. **soc_initial**: None or factor
        a. **storage capacity**: None
        b. **input power** and **output power**: NA
    12. **soc_max**: factor
        a. **storage capacity**: 0.98 (`Solar charge controllers <https://www.morningstarcorp.com/solar-charge-controllers>`_)
        b. **input power** and **output power**: NA
    13. **soc_min**: factor
        a. **storage capacity**: 0.2 (Figure from this research `article <https://www.sciencedirect.com/science/article/pii/S0378775319310043>`_.)
        b. **input power** and **output power**: NA

.. _storage_02.csv:

storage_02.csv
--------------
*This storage example describes a stratified thermal storage*

    1. **age_installed**: year, 0 (for all components of the stratified thermal storage)
    2. **development_costs**: currency, 0 (for all components of the stratified thermal storage)
    3. **specific_costs**: currency/unit
        a. **storage capacity**: 410, (see `Danish energy agency's technology data of small-scale hot water tanks [dea_swt] <https://ens.dk/sites/ens.dk/files/Analyser/technology_data_catalogue_for_energy_storage.pdf>`_ on p.66 - However investment costs of stratified TES could be higher.)
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
        a. **storage capacity**: 16.67, ([dea_swt] p.66 - however fix om costs of stratified TES could differ)
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

In order to run *pvcompare*, a number of input parameters are needed; many of which are stored in csv files with default values in ``data/user_inputs/pvcompare_inputs/``.
The following list will give a brief introduction into the description of the csv files and the source of the given default parameters.

Some parameters can be calculated automatically by *pvcompare* and do not need to be filled it by hand. These parameters are marked with * *auto_calc*.


.. _pv_setup:

pv_setup.csv
------------
    *The pv_setup.csv defines the number of facades that are covered with pv-modules.*

    1. **surface_type**: str, optional values are "flat_roof", "gable_roof", "south_facade", "east_facade" and "west_facade"
    2. **surface_azimuth**: integer, between -180 and 180, where 180 is facing south, 90 is facing east and -90 is facing west
    3. **surface_tilt**: integer, between 0 and 90, where 90 represents a vertical module and 0 a horizontal.
    4. **technology**: str, optional values are "si" for a silicone module, "cpv" for concentrator photovoltaics and "psi" for a perovskite silicone module

.. _building_parameters:

building_parameters.csv
-----------------------
    *Parameters that describe the characteristics of the building that should be considered in the simulation. The default values are taken from [1].*

    1. **number of storeys**,int, 5
    2. **number of houses**: int, 20
    3. **population per storey**: int, 32 (number of habitants per storey)
    4. **total storey area**: int, 1232 (total area of one storey, equal to the flat roof area in m²)
    5. **length south facade**: int, 56 (length of the south facade in m)
    6. **length eastwest facade**:int, 22 (length of the east/west facade in m)
    7. **hight storey**: int, 3 (hight of each storey in m)
    8. **room temperature**: int, 20 (average room temperature inside the building, default: 20 °C)
    9. **heating limit temperature**: int, 15 (temperature limit for space heating in °C, default: `15 °C <http://wiki.energie-m.de/Heizgrenztemperatur>`_)
    10. **include warm water**: bool, False (condition about whether warm water is considered in the heat demand, default: False. If False, the warm water demand is neglected in the simulation.)
    11. **filename_total_SH**: str, total_consumption_SH_residential.xlsx (name of the csv file that contains the total energy consumption for space heating of countries in the European Union [2])
    12. **filename_total_WH**: str, total_consumption_WH_residential.xlsx (name of the csv file that contains the total energy consumption for water heating of countries in the European Union [2])
    13. **filename_elect_SH**: str, electricity_consumption_SH_residential.xlsx (name of the csv file that contains the electrical energy consumption of space heating of countries in the European Union countries [2])
    14. **filename_elect_WH**: str, electricity_consumption_WH_residential.xlsx (name of the csv file that contains the electrical energy consumption of warm water heating of countries in the European Union [2])
    15. **filename_residential_electricity_demand**: str, electricity_consumption_residential.xlsx (name of the csv file that contains the total electricity energy consumption in residential sector of countries in the European Union [2])
    16. **filename_total_cooking_consumption**: str, total_consumption_cooking_residential.xlsx (name of the csv file that contains the total energy consumption for cooking in residential sector of countries in the European Union [2])
    17. **filename_electricity_cooking_consumption**: str,electricity_consumption_cooking_residential.xlsx (name of the csv file that contains the electrical residential cooking demand of countries in the European Union [2])
    18. **filename_country_population**: str, EUROSTAT_population.csv (name of the csv file with total population of each country in the European Union [2])

.. _HP_parameters:

heat_pumps_and_chillers.csv
---------------------------
    *Parameters that describe characteristics of the heat pumps and chillers in the simulated energy system.*
    *Values below assumed for each heat pump technology from research and comparison of three models, each of a different manufacturer.*
    *For each technology the quality grade has been calculated from the mean quality grade of the three models.*

    1. **mode**: str, options: 'heat_pump' or 'chiller'
    2. **technology**: str, options: 'air-air', 'air-water' or 'brine-water' (These three technologies can be processed so far. Default: If missing or different the plant will be modeled as air source)
    3. **quality_grade**: float, scale-down factor to determine the COP of a real machine (Can be calculated from COP provided by manufacturer under nominal conditions and nominal temperatures. Required equations can be found in the `oemof.thermal documentation of compression heat pump and chiller <https://oemof-thermal.readthedocs.io/en/latest/compression_heat_pumps_and_chillers.html>`_.)
        a. **air-to-air heat pump**: default: 0.1852, Average quality grade of the following heat pump models: (`RAC-50WXE Hitachi, Ltd.  <https://www.hitachi-hvac.co.uk/ranges/residential-air-conditioning/premium-s-series-wall-mounted>`_, `MSZ-GL50 Mitsubishi Electric Corporation <https://www.mitsubishi-electric.co.nz/materials/aircon/brochures/@MSZ-GL.pdf>`_ and `KIT-E18-PKEA of Panasonic Corporation <https://www.panasonicproclub.com/uploads/general/default_catalogues/enduser_leaflets_english/2014/Panasonic_PKEA_14.pdf>`_)
        b. **air-to-water heat pump**: default: 0.4030, Average quality grade of the following heat pump models: (`WPLS6.2 of Bosch Thermotechnik GmbH – Buderus <https://productsde.buderus.com/buderus/productsde.buderus.com/broschueren/buderus-broschuere-logatherm-wpls.2-110920.pdf>`_, `WPL 17 ICS classic of STIEBEL ELTRON GmbH & Co. KG <https://www.stiebel-eltron.de/de/home/produkte-loesungen/erneuerbare_energien/waermepumpe/luft-wasser-waermepumpen/wpl_09_17_ics_ikcsclassic/wpl_17_ikcs_classic/technische-daten.product.pdf>`_ and `221.A10 of Viessmann Climate Solutions SE <https://www.viessmann.de/de/wohngebaeude/waermepumpe/luft-wasser-waermepumpen/vitocal-222-a-mb.html>`_)
        c. **brine-to-water heat pump**: default: 0.53, Average quality grade of the following heat pump models: (`WPS 6K-1 of Bosch Thermotechnik GmbH – Buderus <https://productsde.buderus.com/buderus/productsde.buderus.com/broschueren/buderus-broschuere-logatherm-wps1-wpsk1-wsw196itts-110920.pdf>`_, `WPF 05 of STIEBEL ELTRON GmbH & Co. KG <https://www.stiebel-eltron.de/de/home/produkte-loesungen/erneuerbare_energien/waermepumpe/sole-wasser-waermepumpen/wpf_04_05_07_10_1316/wpf_16/technische-daten.product.pdf>`_ and `5008.5Ai of WATERKOTTE GmbH <https://www.waterkotte.de/fileadmin/data/editor/6_systempartner/Prospekt/EcoTouch_5029_Ai_D_0519.pdf>`_)
        d. **air-to-air chiller**: 0.3 (Obtained from `monitored data <https://oemof-thermal.readthedocs.io/en/latest/validation_compression_heat_pumps_and_chillers.html>`_ of the GRECO project)
    4. **temp_high**: float, temperature in °C of the sink (external outlet temperature at the condenser),
        a. **air-to-air heat pump**: 38, Internal condensor temperature assuming a room temperature of 20 °C, adding a dT of 2 K to heat exchange between air and external circuit, considering temperature spread of 6 K of the external medium [4] and assuming a 10 K temperature difference between external and internal condensor flow
        b. **air-to-water heat pump**: 50, Internal condensor temperature assuming a surface heating temperature of 40 °C (see for instance this `advisor of Vaillant <https://www.vaillant.de/heizung/heizung-verstehen/tipps-rund-um-ihre-heizung/vorlauf-rucklauftemperatur/>`_) and a 10 K temperature difference between external and internal condensor flow
        c. **brine-to-water heat pump**: 50, Internal condensor temperature assuming a surface heating temperature of 40 °C (see for instance this `advisor of Vaillant <https://www.vaillant.de/heizung/heizung-verstehen/tipps-rund-um-ihre-heizung/vorlauf-rucklauftemperatur/>`_) and a 10 K temperature difference between external and internal condensor flow
        d. **air-to-air chiller**: Passed empty or with *NaN* in order to model from ambient temperature
    5. **temp_low**: float, temperature in °C of the source (external outlet temperature at the evaporator),
        a. **air source heat pump**: Passed empty or with *NaN* in order to model from ambient temperature
        b. **air-to-water heat pump**: Passed empty or with *NaN* in order to model from ambient temperature
        c. **brine-to-water heat pump**: Passed empty or with *NaN* in order to model from mean yearly ambient temperature as simplifying assumption of the ground temperature from depths of approximately 15 meters (see `brandl_energy_2006 <https://www.icevirtuallibrary.com/doi/full/10.1680/geot.2006.56.2.81>`_)
        d. **air-to-air chiller**: 15 (The low temperature has been set for now to 15° C, a temperature lower the comfort temperature of 20–22 °C. The chiller has not been implemented in the model yet. However, should it been done so in the future, these temperatures must be researched and adjusted.)
    6. **factor_icing**: float or None, COP reduction caused by icing, only for `mode` 'heat_pump', default: None
    7. **temp_threshold_icing**: float or None, Temperature below which icing occurs, only for `mode` 'heat_pump', default: None

.. _stratTES_parameters:

stratified_thermal_storage.csv
------------------------------
    *Parameters that describe characteristics of the stratified thermal storage in the simulated energy system.*
    *The parameters have been set on the example of the stratified thermal storage TH 1000 of Schindler+Hofmann GmbH &  Co. KG*

    1. **var_name**: var_value, var_unit
    2. **height**: Empty to model investment optimization or numeric to model with a fix storage size, m
    3. **diameter**: 0.79 (cf. inner diameter in data sheet of `[TH 1000] <https://www.schindler-hofmann.de/content/pdf/prospekte/S+H_Pufferspeicher+Kombispeicher.pdf>`_ ), m
    4. **temp_h**: 40 (Assuming a surface heating temperature of 40 °C), degC
    5. **temp_c**: 34 (Considering temperature spread of 6 K of inlet and outlet temperature [4]), degC
    6. **s_iso**: 100 (cf. [TH 1000]), mm
    7. **lamb_iso**: 0.03 (Assumption taken from [5]), W/(m*K)
    8. **alpha_inside**: 4.3 (Calculated with calculations in [6]), W/(m2*K)
    9. **alpha_outside** 3.17 (Calculated with calculations in [6]), W/(m2*K)



2. Static inputs parameters
==========================

list_of_workalendar_countries.csv
---------------------------------
    *list of countries for which a python.workalendar [3] exists with the column name "country".*


EUROSTAT_population.csv
-----------------------
    *"Population on 1 January by age, sex and broad group of citizenship for European countries" of the years 2008 to 2019 obtained from [7]*


Energetic demands
-----------------

    *Energetic demands were obtained from* `Odyssee Project of Enerdata <https://odyssee.enerdata.net/database/>`_

    * electricity_consumption_residential.xlsx [8]
    * electricity_consumption_SH_residential.xlsx [9]
    * electricity_consumption_WH_residential.xlsx [10]
    * total_consumption_cooking_residential.xlsx [11]
    * electricity_consumption_cooking_residential.xlsx [12]
    * total_consumption_SH_residential.xlsx [13]
    * total_consumption_WH_residential.xlsx [14]

local_grid_parameters.xlsx
--------------------------

    1. **electricity_price**: default: 0.18 else *auto_calc*, EUR/kWh, Obtained from [15]
    2. **gas_price**: default: 0.05 else *auto_calc*, EUR/kWh, Gas prices of European countries obtained from [16]
    3. **feedin_tariff**: default: 0.05 else *auto_calc*, EUR/kWh, Feed-in tariff obtained from [17]
    4. **emission_factor**: default: 0.25, kgCO2eq/kWh, Emission factor of the electricity grid obtained from [18]
    5. **renewable_share**: default: 0.15, factor, Share of renewables in the electricity grid obtained from [19]




[1] Hachem, 2014: Energy performance enhancement in multistory residential buildings. DOI: 10.1016/j.apenergy.2013.11.018

[2] EUROSTAT: https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use

[3] Workalendar https://pypi.org/project/workalendar/

[4] Felix Ziegler, Dr. Ing, 1997: Sorptionswärmepumpen. Erding, Forschungsberichte des Deutschen Kälte- und Klimatechnischen Vereins Nr. 57, habilitation

[5] Beikircher, Thomas & Buttinger, Frank & Rottmann, Matthias & Herzog, Fabian & Konrad, Martin & Reuß, Manfred & Beikircher, Redaktion, 2013: Superisolierter Heißwasser-Langzeitwärmespeicher : Abschlussbericht zu BMU-Projekt Förderkennzeichen 0325964A, Projektlaufzeit: 01.05.2010 - 31.10.2012. 10.2314/GBV:749701188.

[6] In:Klan, H, 2002: Wärmeübergang durch freie Konvektion an umströmten Körpern. Berlin, Heidelberg: Springer Berlin Heidelberg, ISBN 978-3-662-10743-0, 567-591

[7] Eurostat, the Statistical Office of the European Union: Population on 1 January by age, sex and broad group of citizenship. https://ec.europa.eu/eurostat/databrowser/view/migr pop2ctz/default/table?lang=en

[8] Enerdata: Electricity consumption of residential sector. https://odyssee.enerdata.net/database/

[9] Enerdata: Electricity consumption of residential for space heating. https://odyssee.enerdata.net/database/

[10] Enerdata: Electricity consumption of households for water heating. https://odyssee.enerdata.net/database/

[11] Enerdata: Final consumption of residential for cooking. https://odyssee.enerdata.net/database/

[12] Enerdata: Electricity consumption of residential for cooking. https://odyssee.enerdata.net/database/

[13] Enerdata: Final consumption of residential for space heating. https://odyssee.enerdata.net/database/

[14] Enerdata: Final consumption of households for water heating. https://odyssee.enerdata.net/database/

[15] Eurostat, the Statistical Office of the European Union: Electricity prices by type of user. https://ec.europa.eu/eurostat/databrowser/view/ten00117/default/table?lang=en

[16] Eurostat, the Statistical Office of the European Union: Gas prices by type of user. https://ec.europa.eu/eurostat/databrowser/view/ten00118/default/table?lang=en

[17] magazine, pv: Feed-in taris (FITs) in Europe. https://www.pv-magazine.com/features/archive/solar-incentives-and-ts/feed-in-taris-in-europe/

[18] Hans Bruyninckx: Greenhouse gas emission intensity of electricity generation in Europe | European Environment Agency. https://www.eea.europa.eu/data-and-maps/indicators/overview-of-the-electricity-production-3/assessment

[19] Eurostat, the Statistical Office of the European Union: Share of renewable energy in gross nal energy consumption. https://ec.europa.eu/eurostat/databrowser/view/t2020 31/default/table?lang=en