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
relevant parameters of MVS can be found `here <https://mvs-eland.readthedocs.io/en/latest/MVS_parameters.html>`_.

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
