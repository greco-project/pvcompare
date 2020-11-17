=========================================================
Parameters of pvcompare: Definitions and Default Values
=========================================================
.. _parameters:

Within the ``pvcompare/pvcompare/data/`` directory, two separate categories of inputs can be observed.

1. *MVS* parameters (found in the CSVs within the ``data/mvs_inputs/csv_elements/`` directory)
2. *pvcompare*-specific parameters (found in the CSVs within the ``data/inputs`` directory)

------------------
1. MVS Parameters
------------------

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
    1. **age_installed**: year, 0 (for all components such as charge controllers and inverters)
    2. **development_costs**: currency, 0 (for all components)
    3. **specific_costs**: currency/kW
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 46 (According to this `source <https://alteredenergy.com/wholesale-cost-of-solar-charge-controllers/>`_, a 12 Volts, 80 Amperes Solar Charge Controller costs about 50 USD, which is about 46 €/kW.)
        b. **solar_inverter_01**: 230 (Per `this <https://www.solaranlage-ratgeber.de/photovoltaik/photovoltaik-wirtschaftlichkeit/photovoltaik-anschaffungskosten>`_, the cost of inverters are around 230 Euro/kW.)
    4. **efficiency**: factor
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 1
        b. **solar_inverter_01**: 0.95 (European efficiency is around 0.95, per several sources. `Fronius <https://www.fronius.com/en/photovoltaics/products>`_, for example.)
    5. **inflow_direction**: str
        a. **storage_charge_controller_in**: Electricity
        b. **storage_charge_controller_out**: ESS Li-Ion
        c. **solar_inverter_01**: PV bus1 (if there are more inverters such as **solar_inverter_02**, then the buses from which the electricity flows into the inverter happens, will be named accordingly. E.g.: PV bus2.)
    6. **installedCap**: kW, 0 (for all components)
    7. **label**: str
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: Charge Contoller ESS Li-Ion (charge)
        b. **solar_inverter_01**: Solar inverter 1 (if there are more inverters, then will be named accordingly. E.g.: Solar inverter 2)
    8. **lifetime**: year
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 15 (According to this `website <https://www.google.com/url?q=https://solarpanelsvenue.com/what-is-a-charge-controller/&sa=D&ust=1591697986335000&usg=AFQjCNE54Zbsv-Gd2UZb-_SY_QNG5Ig2fQ>`_, the lifetime of charge controllers is around 15 years.)
        b. **solar_inverter_01**: 10 (`Lifetime <https://thosesolarguys.com/how-long-do-solar-inverters-last/>`_ of solar (string) inverters is around 10 years.)
    9. **specific_costs_om**: currency/kW
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 0 (According to `AM Solar <https://amsolar.com/diy-rv-solar-instructions/edmaintenance>`_, maintainence work on charge controllers is minimal. So we can consider the costs to be covered by specific_cost_om in fixcost.csv, which is just the system O&M cost.)
        b. **solar_inverter_01**: 6 (From page 11 in this 2015 Sandia `document <https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/2016/160649r.pdf>`_, assuming one maintainence activity per year, we can take 7 USD/kW or 6 €/kW.)
    10. **dispatch_price**: currency/kWh, 0 (for all components)
    11. **optimizeCap**: bool, True (for all components)
    12. **outflow_direction**: str
        a. **storage_charge_controller_in**: ESS Li-Ion
        b. **storage_charge_controller_out**: Electricity
        c. **solar_inverter_01**: Electricity (if there are more solar inverters, this value applies for them as well)
    13. **energyVector**: str, Electricity (same for all the components)
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
    1. **energy_price**: currency/kWh, 0.24  * *auto_calc* (0.24 €/kWh is the average household electricity price of Spain for 2019S1. Obtained from `Eurostat <https://ec.europa.eu/eurostat/statistics-explained/images/d/d9/Electricity_prices%2C_first_semester_of_2017-2019_%28EUR_per_kWh%29.png>`_.)
    2. **feedin_tariff**: currency/kWh, (0.10 €/kWh is for Germany. We do not have data for Spain yet.)
    3. **inflow_direction**: str, Electricity
    4. **label**: str, Electricity grid feedin
    5. **optimizeCap**: bool, True
    6. **outflow_direction**: str, Electricity
    7. **peak_demand_pricing**: currency/kW, 0
    8. **peak_demand_pricing_period**: 	times per year (1,2,3,4,6,12), 1
    9. **type_oemof**: str, source
    10. **energyVector**: str, Electricity
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

---------------------------------
2. pvcompare-specific parameters
---------------------------------

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
    7. **heating limit temperature**: int, temperature limit for space heating in °C, default: `15 °C <http://wiki.energie-m.de/Heizgrenztemperatur>`_
    8. **filename_total_consumption**: str, name of the csv file that contains the total electricity and heat consumption for EU countries in different years from [2] *
    9. **filename_total_SH**: str, name of the csv file that contains the total space heating for EU countries in different years [2] *
    10. **filename_total_WH**: str, name of the csv file that contains the total water heating for EU countries in different years [2] *
    11. **filename_elect_SH**: str, name of the csv file that contains the electrical space heatig for EU countries in different years [2] *
    12. **filename_elect_WH**: str, name of the csv file that contains the electrical water heating for EU countries in different years [2] *
    13. **filename_residential_electricity_demand**: str, name of the csv file that contains the total residential electricity demand for EU countries in different years [2] *
    14. **filename_country_population**: str, name of the csv file that contains population for EU countries in different years [2] *

* heat_pumps_and_chillers:
    *Parameters that describe characteristics of the heat pumps and chillers in the simulated energy system.*

    1. **mode**: str, options: 'heat_pump' or 'chiller'
    2. **quality_grade**: float, scale-down factor to determine the COP of a real machine, default: heat pump: 0.2, chiller 0.25 (tests were made with monitored data from the GRECO project, reference follows)
    3. **room_temperature**: float, mean temperature of the room that is heated/cooled, will be adapted with issue #59
    4. **start_temperature**: float, temperature at which the heating/cooling period starts, default: heating 17 °C (`Reference <https://www.hotmaps-project.eu/wp-content/uploads/2018/03/D2.3-Hotmaps_for-upload_revised-final_.pdf>`_)
    5. **factor_icing**: float or None, COP reduction caused by icing, only for ``mode`` 'heat_pump', default: None
    6. **temp_threshold_icing**: float or None, Temperature below which icing occurs, only for ``mode`` 'heat_pump', default: None

* list_of_workalendar:
    *list of countries for which a python.workalendar [3] exists with the column name "country".*



[1] Hachem, 2014: Energy performance enhancement in multistory residential buildings. DOI: 10.1016/j.apenergy.2013.11.018

[2] EUROSTAT: https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use

[3] Workalendar https://pypi.org/project/workalendar/

\* the described csv files are to be added to the input folder accordingly.
