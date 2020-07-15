.. currentmodule:: pvcompare

==================
Code documentation
==================

Area potential
==============

Function for calculating the area potential of the rooftop and facades for a given population.

.. autosummary::
   :toctree: temp/

    area_potential.calculate_area_potential


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



Reading and Writing input csv's
===============================

Functions that match manual inputs and calculated results with mvs_inputs/csv_elements/

.. autosummary::
   :toctree: temp/

   check_inputs.check_for_valid_country_year
   check_inputs.add_project_data
   check_inputs.add_electricity_price
   check_inputs.check_mvs_energy_production_file
   check_inputs.create_mvs_energy_production_file
   check_inputs.add_parameters_to_energy_production_file
   check_inputs.add_evaluated_period_to_simulation_settings


	