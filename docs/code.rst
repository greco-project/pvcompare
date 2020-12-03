.. currentmodule:: pvcompare

.. _code:

Code documentation
~~~~~~~~~~~~~~~~~~

.. _main:

Main
====

Main functions of *pvcompare* that can be used to start a full simulation.

.. autosummary::
    :toctree: temp/

    main.main
    main.apply_mvs


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
    pv_feedin.nominal_values_pv
    pv_feedin.set_up_system
    pv_feedin.get_optimal_pv_angle

.. _cpv:

CPV time series
===============

Function for calculating the feed-in time series for the CPV technology.

.. autosummary::
    :toctree: temp/

    cpv.apply_cpvlib_StaticHybridSystem.create_cpv_time_series

.. _psi:

PSI time series
===============

Function for calculating the feed-in time series for the perovskite silicone technology.

.. autosummary::
    :toctree: temp/

    perosi.perosi.create_pero_si_timeseries
    perosi.perosi.create_timeseries
    perosi.perosi.calculate_smarts_parameters
    perosi.pvlib_smarts.SMARTSSpectra
    perosi.pvlib_smarts._smartsAll


.. _check_inputs:

Reading and Writing input csv's
===============================

Functions that match manual inputs and calculated results with mvs_inputs/csv_elements/

.. autosummary::
    :toctree: temp/

    check_inputs.check_for_valid_country_year
    check_inputs.add_project_data
    check_inputs.add_electricity_price
    check_inputs.check_mvs_energy_production_file
    check_inputs.add_parameters_to_energy_production_file
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


.. _loops:

Automated loops
===============

Functions that help to loop over simulations while alterating a specific parameter (sensitivity).

.. autosummary::
    :toctree: temp/

    automated_loop.loop


.. _plots:

Plotting
========

Functions for plotting mvs results.

.. autosummary::
    :toctree: temp/

    plots.plot_all_flows
    plots.plot_kpi_loop




