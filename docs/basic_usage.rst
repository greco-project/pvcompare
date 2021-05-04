
.. _basic_usage:

Basic usage of pvcompare
~~~~~~~~~~~~~~~~~~~~~~~~

.. _run_simulation:

Run a simulation
================

You can easily run a simulation with *pvcompare* by running the file ``run_pvcompare.py`` (ADD LINK!) or by executing one of the examples.
There is three examples, one that accounts only for the electricity sector, one with sector coupling and heat pumps and one sector coupling scenario with a gas
plant instead of heat pumps.

.. _define_params:

Define your own components and parameters
=========================================

*pvcompare* provides you with templates and default parameters for your simulations. A full description of the parameters can be found in the section :ref:`parameters`.
However, you can also define your own energy system, choose different parameters and/or change the settings.

Please refer to `Simulating with the MVS <https://multi-vector-simulator.readthedocs.io/en/latest/simulating_with_the_mvs.html>`_ to learn
how to work with the input csv files and how to provide your own time series.
In *pvcompare* all user input files are stored in the directory
``data/user_inputs``. It contains two subfolders ``mvs_inputs`` for all MVS parameters and ``pvcompare_inputs`` for *pvcompare* inputs parameters. You can define a different input directory by providing the parameters ``user_inputs_mvs_directory`` and ``user_inputs_pvcompare_directory`` to the :py:func:`~.main` and :py:func:`~.apply_mvs` functions.
Please note that *pvcompare* only works with csv files but not with `json files <https://multi-vector-simulator.readthedocs.io/en/latest/simulating_with_the_mvs.html#json-file-mvs-config-json>`_.

Here's a very short description of the different input files:

**``pvcompare_inputs``**
- ``pv_setup.csv``: Definition of PV assets (technology, tilt angle, azimuth angle, roof-top or facade installation)
- ``building_parameters.csv``: Definition of characteristics of the building type that should be considered in the simulation.
- ``heat_pumps_and_chillers.csv``: Definition of characteristics of the heat pumps and chillers in the simulated energy system.

**``mvs_inputs/csv_elements``**

- ``constraints.csv``: List of contraints that should be activated for the energy system optimization (such as Net Zero Energy (NZE) constraint)
- ``economic_data.csv``: General information about the simulation (currency, project duration, discount factor)
- ``energyBusses.csv``: Definition of connecting busses (e.g. one electricty and one heat bus in a sector coupled scenario)
- ``energyConsumption.csv``: Definition of the energy demand (e.g. electricity demand and/or heat demand with the filename of the demand time series)
- ``energyConversion.csv``: Definition of transformers (e.g. solar inverter, charge controller, heat pumps etc.)
- ``energyProduction.csv``: Definition of local generation (e.g. one or more PV plants with the maximal installable capacity and costs)
- ``energyProviders.csv``: Definition of the energy Provider (e.g. a DSO or a Gas plant in a sectorcoupled scenario)
- ``energyStorage.csv``: Definition of storages (battery or TES storage with the filename of the csv file that contains more precise information for each storage (e.g. ``storage_01.csv`` or ``storage_02.csv``))
- ``fixcost.csv``: Definition of general fixcosts for the project (disregarded by default)
- ``project_data.csv``: Definition of the location and name of the simulation
- ``simulation_settings.csv``: Definition of the year and the duration of the simulation (e.g. one year or less)
- ``storage_01.csv``: Definition of more precise storage parameters (as an addition to ``energyStorage.csv``)



Download ERA5 weather data
==========================
If you run a simulation, *pvcompare* automatically tries to download the ERA5 weather data from `Climate Data Store (CDS) <https://cds.climate.copernicus.eu/>`_ and store it locally in ``data/static_inputs``, unless the
file already exists. In order to enable this download you first need to make an account at the `CDS <https://cds.climate.copernicus.eu/user/login?destination=%2F%23!%2Fhome>`_ and
install the cdsapi package. `This page <https://cds.climate.copernicus.eu/api-how-to>`_ provides information about the installation. When using the API for a large about of data (e.g. a year for one location) the request gets queued and the download might take a while.

Provide your own weather data
-----------------------------
As an alternative `oemof feedinlib <https://feedinlib.readthedocs.io/en/releases-0.1.0/load_era5_weather_data.html>`_ provides a jupyter notebook with instructuions on how to download data for a single coordinate or a region.

toto: add more information here (IS)



Add a sensitivy to your simulations
===================================

Here follows a description of how to use the :py:func:`~.automated_loop` functionality.