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

    demand.calculate_power_demand
    demand.calculate_heat_demand

Feed-in time series of photovoltaic installations
=================================================


.. autosummary::
   :toctree: temp/

    pv_feedin.create_PV_timeseries
    pv_feedin.create_normalized_SI_timeseries
    pv_feedin.create_normalized_CPV_timeseries
    pv_feedin.nominal_values_pv
    pv_feedin.set_up_system
    pv_feedin.get_optimal_pv_angle
