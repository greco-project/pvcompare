=========================================================
Parameters of PVCompare: Definitions and Default Values
=========================================================

Within the pvcompare/pvcompare/data/ directory, two separate cateogies of inputs can be observed.

1. MVS parameters (found in the CSVs within the data/mvs_inputs/csv_elements/ directory)
2. PVCompare-specific parameters (found in the CSVs within the data/inputs directory)

------------------
1. MVS Parameters
------------------

As PVCompare makes use of the `MVS <https://github.com/rl-institut/mvs_eland>`_ tool, the definitions of all the
relevant parameters of MVS can be found `here <https://mvs-eland.readthedocs.io/en/latest/MVS_parameters.html>`_. Note
that some parameters of MVS (for instance, all parameters concerning a diesel generator) are not applicable for PVCompare.

The values used by default in PVCompare for the above parameters in each CSV, are detailed below:

* project_data.csv
    1. **country**: Spain (the country in which the project is located)
    2. **label**: project_data
    3. **latitude**: 45.641603
    4. **longitude**: 5.875387
    5. **project_id**: 1
    6. **project_name**: net zero energy community

* economic_data.csv
    1. **curency**: EUR (stands for euro; can be replaced by SEK, if the system is located in Sweden, for instance).
    2. **discount_factor**: 0.06 (most recent data is from 2018, as documented by this market `survey <https://www.grantthornton.co.uk/insights/renewable-energy-discount-rate-survey-2018/>`_.
    3. **label**: economic_data
    4. **project_duration**: 1 (number of years)
    5. **tax**: 0 (this feature has not been implemented yet, as per MVS documentation)

* simulation_settings.csv
    1. **evaluated_period**: 365 (number of days)
    2. **label**: simulation_settings
    3. **output_lp_file**: False
    4. **restore_from_oemof_file**: False
    5. **start_date**: 2013-01-01 00:00:00
    6. **store_oemof_results**: True
    7. **timestep**: 60 (hourly time-steps, 60 minutes)
    8. **display_nx_graph**: False
    9. **store_nx_graph**: True

* fixcost.csv
    +----------------------+---------------------------------+------------------+-------------------------------+
    |                      | distribution_grid               | engineering      | operation                     |
    +======================+=================================+==================+===============================+
    |  **age_installed**   |         10                      |       0          |     0                         |
    +----------------------+---------------------------------+------------------+-------------------------------+
    | **cost_development** |         10                      |       0          |     0                         |
    +----------------------+---------------------------------+------------------+-------------------------------+
    |  **specific_cost**   |         10                      |       0          |     4600                      |
    +----------------------+---------------------------------+------------------+-------------------------------+
    |       **label**      |distribution grid infrastructure | R&D, engineering |     Fix project operation     |
    +----------------------+---------------------------------+------------------+-------------------------------+
    |  **lifetime**        |         30                      |       20         |     20                        |
    +----------------------+---------------------------------+------------------+-------------------------------+
    | **specific_cost_om** |         10                      |       0          |     0                         |
    +----------------------+---------------------------------+------------------+-------------------------------+
    |  **price_dispatch**  |         10                      |       0          |     0                         |
    +----------------------+---------------------------------+------------------+-------------------------------+
* energyConsumption.csv
    1. **dsm**: False (dsm stands for Demand Side Management. This feature has not been implement in MVS as of now.)
    2. **file_name**: electricity_load.csv
    3. **label**: Households
    4. **type_asset**: demand
    5. **type_oemof**: sink
    6. **energyVector**: Electricity
    7. **inflow_direction**: Electricity
    8. **unit**: kW
* energyConversion.csv
    1. **age_installed**: 0 (for all components such as charge controllers and inverters)
    2. **development_costs**: 0 (for all components)
    3. **capex_var**:
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 46 (According to this `source <https://alteredenergy.com/wholesale-cost-of-solar-charge-controllers/>`_, a 12 Volts, 80 Amperes Solar Charge Controller costs about 50 USD, which is about 46 €/kW.)
        b. **solar_inverter_01**: 230 (Per `this <https://www.solaranlage-ratgeber.de/photovoltaik/photovoltaik-wirtschaftlichkeit/photovoltaik-anschaffungskosten>`_, the cost of inverters are around 230 Euro/kW.)
    4. **efficiency**:
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 1
        b. **solar_inverter_01**: 0.95 (European efficiency is around 0.95, per several sources. `Fronius <https://www.fronius.com/en/photovoltaics/products>`_, for example.)
    5. **inflow_direction**:
        a. **storage_charge_controller_in**: Electricity
        b. **storage_charge_controller_out**: ESS Li-Ion
        c. **solar_inverter_01**: PV bus1 (if there are more inverters such as **solar_inverter_02**, then the buses from which the electricity flows into the inverter happens, will be named accordingly. E.g.: PV bus2.)
    6. **installedCap**: 0 (for all components)
    7. **label**:
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: Charge Contoller ESS Li-Ion (charge)
        b. **solar_inverter_01**: Solar inverter 1 (if there are more inverters, then will be named accordingly. E.g.: Solar inverter 2)
    8. **lifetime**:
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 15 (According to this `website <https://www.google.com/url?q=https://solarpanelsvenue.com/what-is-a-charge-controller/&sa=D&ust=1591697986335000&usg=AFQjCNE54Zbsv-Gd2UZb-_SY_QNG5Ig2fQ>`_, the lifetime of charge controllers is around 15 years.)
        b. **solar_inverter_01**: 10 (`Lifetime <https://thosesolarguys.com/how-long-do-solar-inverters-last/>`_ of solar (string) inverters is around 10 years.)
    9. **specific_costs_om**:
        a. **storage_charge_controller_in** and **storage_charge_controller_out**: 0 (According to `AM Solar <https://amsolar.com/diy-rv-solar-instructions/edmaintenance>`_, maintainence work on charge controllers is minimal. So we can consider the costs to be covered by specific_cost_om in fixcost.csv, which is just the system O&M cost.)
        b. **solar_inverter_01**: 6 (From page 11 in this 2015 Sandia `document <https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/2016/160649r.pdf>`_, assuming one maintainence activity per year, we can take 7 USD/kW or 6 €/kW.)
    10. **dispatch_price**: 0 (for all components)
    11. **optimizeCap**: True (for all components)
    12. **outflow_direction**:
        a. **storage_charge_controller_in**: ESS Li-Ion
        b. **storage_charge_controller_out**: Electricity
        c. **solar_inverter_01**: Electricity (if there are more solar inverters, this value applies for them as well)
    13. **energyVector**: Electricity (same for all the components)
    14. **type_oemof**: transformer (same for all the components)
    15. **unit**: kW (applies to all the components)
* energyProduction.csv:
    1. **age_installed**: 0 (for all the components)
    2. **development_costs**: 0 (**TO BE DECIDED**)
    3. **specific_costs**: (**TO BE DECIDED**)
    4. **file_name**:
        a. **pv_plant_01**: si_180_31.csv
        b. **pv_plant_02**: cpv_180_31.csv
        c. **pv_plant_03**: cpv_90_90.csv
    5. **installedCap**: 0.0 (for all components)
    6. **maximumCap**:
        a. **pv_plant_01**: 25454.87
        b. **pv_plant_02**: 55835.702
        c. **pv_plant_03**: 23929.586
    7. **label**:
        a. **pv_plant_01**: PV si_180_31
        b. **pv_plant_02**: PV cpv_180_31
        c. **pv_plant_03**: PV cpv_90_90
    8. **lifetime**: 25 (for all the components)
    9. **specific_costs_om**: 50 (same for all the components; 50 €/kWp is the value that is arrived at after accounting for the yearly inspection and cleaning. Here is the detailed `explaination <https://github.com/greco-project/pvcompare/issues/13>`_.)
    10. **dispatch_price**: 0 (this is because there are no fuel costs associated with Photovoltaics)
    11. **optimizeCap**: True (for all components)
    12. **outflow_direction**: PV bus1 (for all of the components)
    13. **type_oemof**: source (for all of the components)
    14. **unit**: kWp (for all of the components)
    15. **energyVector**: Electricity (for all of the components)
* energyProviders.csv:
    1. **energy_price**: 0.24 (0.24 €/kWh is the average household electricity price of Spain for 2019S1. Obtained from `Eurostat <https://ec.europa.eu/eurostat/statistics-explained/images/d/d9/Electricity_prices%2C_first_semester_of_2017-2019_%28EUR_per_kWh%29.png>`_.)
    2. **feedin_tariff**: (0.10 €/kWh is for Germany. We do not have data for Spain yet.)
    3. **inflow_direction**: Electricity
    4. **label**: Electricity grid feedin
    5. **optimizeCap**: True
    6. **outflow_direction**: Electricity
    7. **peak_demand_pricing**: 0
    8. **peak_demand_pricing_period**: 1
    9. **type_oemof**: source
    10. **energyVector**: Electricity
* energyStorage.csv:
    1. **inflow_direction**: ESS Li-Ion
    2. **label**: ESS Li-Ion
    3. **optimizeCap**: True
    4. **outflow_direction**: ESS Li-Ion
    5. **type_oemof**: storage
    6. **storage_filename**: storage_01.csv
    7. **energyVector**: Electricity
* storage_01.csv:
    1. **age_installed**: 0 (for all components)
    2. **development_costs**: 0 (for all components)
    3. **specific_costs**:
        a. **storage capacity**: 0.2 (Consult this `reference <https://www.energieheld.de/solaranlage/photovoltaik/kosten#vergleich>`_ for details.)
        b. **input power** and **output power**: 0
    4. **c_rate**:
        a. **storage capacity**: NA (does not apply)
        b. **input power** and **output power**: 1 (this just means that the whole capacity of the battary would be used during charging and discharging cycles)
    5. **efficiency**:
        a. **storage capacity**: 0
        b. **input power** and **output power**: 0.9 (Charging and discharging efficiency. The value has been sourced from this `page <https://en.wikipedia.org/wiki/Lithium-ion_battery>`_.)
    6. **installedCap**: 0 (applies for all the parameters of the battery storage)
    7. **label**: Same as the column headers (storage capacity, input power, output power)
    8. **lifetime**: 10 (applies for all the parameters of the battery storage)
    9. **specific_costs_om**: 0 (applies for all the parameters of the battery storage)
    10. **dispatch_price**:
        a. **storage capacity**: NA (does not apply)
        b. **input power** and **output power**: 0
    11. **soc_initial**:
        a. **storage capacity**: None
        b. **input power** and **output power**: NA
    12. **soc_max**:
        a. **storage capacity**: 0.8 (Took the Fronius 4.5 battery which has a rated capacity 4.5 kW, but 3.6 kW is the usable capacity.So SoC max would be 80% or 0.8.)
        b. **input power** and **output power**: NA
    13. **soc_min**:
        a. **storage capacity**: 0.1 (Figure from this research `article <https://www.sciencedirect.com/science/article/pii/S0378775319310043>`_.)
        b. **input power** and **output power**: NA
    14. **unit**:
        a. **storage capacity**: kWh
        b. **input power** and **output power**: kW