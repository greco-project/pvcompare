.. currentmodule:: pvcompare

.. _code:

Code documentation
~~~~~~~~~~~~~~~~~~

.. _main:

Main
====

Main functions of *pvcompare* that can be used to run a full simulation.

.. autosummary::
    :toctree: temp/

    main.apply_mvs
    main.apply_pvcompare


.. _area_potential:

Area potential
==============

Function for calculating the area potential of the rooftop and facades for a given population.

.. autosummary::
    :toctree: temp/

    area_potential.calculate_area_potential

.. _demand:

Demand
======

Functions for calculating the electrical demand profiles and heat demand profiles.

.. autosummary::
    :toctree: temp/

    demand.calculate_load_profiles
    demand.calculate_power_demand
    demand.calculate_heat_demand
    demand.adjust_heat_demand
    demand.shift_working_hours
    demand.get_workalendar_class

.. _pv_feedin:

Feed-in time series of photovoltaic installations
=================================================

Functions for calculating the feed-in time series of different PV technologies.

.. autosummary::
    :toctree: temp/

    pv_feedin.create_pv_components
    pv_feedin.create_si_time_series
    pv_feedin.create_cpv_time_series
    pv_feedin.create_psi_time_series
    pv_feedin.nominal_values_pv
    pv_feedin.get_peak
    pv_feedin.set_up_system
    pv_feedin.get_optimal_pv_angle

.. _cpv:

CPV time series
===============

Specific functions for calculating the feed-in time series of the CPV technology.

.. autosummary::
    :toctree: temp/

    cpv.apply_cpvlib_StaticHybridSystem.create_cpv_time_series
    cpv.apply_cpvlib_StaticHybridSystem.calculate_efficiency_ref

.. _psi:

PSI time series
===============

Specific functions for calculating the feed-in time series of the perovskite-silicon technology.

.. autosummary::
    :toctree: temp/

    perosi.perosi.create_pero_si_timeseries
    perosi.perosi.create_timeseries
    perosi.perosi.calculate_smarts_parameters
    perosi.pvlib_smarts.SMARTSSpectra
    perosi.pvlib_smarts._smartsAll

.. _heat_pumps_chillers:

Heat pumps and chillers
=======================

Functions for implementing a sector-coupled system (electricity, heat) and for calculating the COPs/EERs of heat pumps and chillers.

.. autosummary::
    :toctree: temp/

    heat_pump_and_chiller.add_sector_coupling
    heat_pump_and_chiller.calculate_cops_and_eers

.. _thermal_storage:

Stratified thermal storage
==========================

Functions for calculating thermal losses of a stratified thermal storage and for adding it to the energy system.

.. autosummary::
    :toctree: temp/

    stratified_thermal_storage.calc_strat_tes_param
    stratified_thermal_storage.save_time_dependent_values
    stratified_thermal_storage.add_strat_tes
    stratified_thermal_storage.run_stratified_thermal_storage

.. _check_inputs:

Reading and Writing input csv's
===============================

Functions that match manual inputs and calculated results with data/user_inputs/mvs_inputs/csv_elements/

.. autosummary::
    :toctree: temp/

    check_inputs.add_parameter_to_mvs_file
    check_inputs.load_parameter_from_mvs_file
    check_inputs.add_parameters_to_storage_xx_file
    check_inputs.add_scenario_name_to_project_data
    check_inputs.add_location_and_year_to_project_data
    check_inputs.add_local_grid_parameters
    check_inputs.check_for_valid_country_year
    check_inputs.overwrite_mvs_energy_production_file
    check_inputs.add_parameters_to_energy_production_file
    check_inputs.add_file_name_to_energy_consumption_file
    check_inputs.add_evaluated_period_to_simulation_settings


.. _era5:

Loading ERA5 weather data
=========================

Functions that request the weather data of one year and one location from the ERA5 weather data set

.. autosummary::
    :toctree: temp/

    era5.load_era5_weatherdata
    era5.get_era5_data_from_datespan_and_position
    era5.format_pvcompare
    era5.weather_df_from_era5

.. _sensitivity_analysis:

Sensitivity analysis
====================

Functions sensivity analysis, i.e. running simulations in a loop while adjusting one parameter at each loop.

.. autosummary::
    :toctree: temp/

    analysis.create_loop_output_structure
    analysis.loop_pvcompare
    analysis.single_loop_pvcompare
    analysis.loop_mvs

.. _evaluation:

Evaluation
==========

Function for the post-processing of KPIs. It is recommended to post-process certain KPIs when sector-coupling electricity and heat sector with a heat pump and/or chiller.

.. autosummary::
    :toctree: temp/

    analysis.postprocessing_kpi

.. _visualization:

Visualization
=============

Plotting function for visualization of simulation results.

.. autosummary::
    :toctree: temp/

    plots.plot_all_flows
    plots.plot_psi_matrix
    plots.plot_kpi_loop
    plots.plot_facades
    plots.plot_compare_scenarios
    plots.plot_compare_technologies
