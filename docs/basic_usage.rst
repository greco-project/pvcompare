
.. _basic_usage:

Basic usage of pvcompare
~~~~~~~~~~~~~~~~~~~~~~~~

.. _run_simulation:

Run a simulation
================

You can easily run a simulation by executing one of the examples in ``examples/``.
There are three examples, one that accounts only for the electricity sector, one for sector coupling using heat pumps and one example covering heat demand with a gas plant as a reference scenario for the one with heat pumps.

If you want to set up your own scenario, you need to insert input files into the directory first. How to do this is described in the next paragraph :ref:`define_params`.
Afterwards you can run a simulation by running the file ``run_pvcompare.py`` in the parent folder of *pvcompare*.
In order to run a simulation you need to at least define the following parameters:

- latitude: float
- longitude: float
- year: int
- storeys: int
- country: str
- scenario_name: str

.. _define_params:

Define your own components and parameters
=========================================

*pvcompare* provides you with templates and default parameters for your simulations. You can find three basic scenarios (for the electricity sector, sector coupled system and a reference for the sector coupled system) in ``examples/example_user_inputs/``.
A full description of the parameters and default values can be found in the section :ref:`parameters`.
However, you can also define your own energy system, choose different parameters and/or change the settings.

You can configure your own scenario by defining the parameters in ``data/user_inputs``. It contains two subfolders ``mvs_inputs`` for all MVS parameters and ``pvcompare_inputs`` for *pvcompare* inputs parameters. You can define a different input directory by providing the parameters ``user_inputs_mvs_directory`` and ``user_inputs_pvcompare_directory`` to the :py:func:`~.main` and :py:func:`~.apply_mvs` functions.
Please note that *pvcompare* only works with csv files but not with `json files <https://multi-vector-simulator.readthedocs.io/en/latest/simulating_with_the_mvs.html#json-file-mvs-config-json>`_.

Because the ``data/user_inputs`` folder is an individual working directory, it is left empty in the initial state of *pvcompare*. The user is required to fill in the specific input files that fit to the according energy system setup.
The directory ``data/user_inputs_collection`` contains a broad collection of all kinds of possible asset definitions that have been used within the GRECO Project. Users are welcome to copy specific parts
from this collection folder into the ``data/user_inputs`` files. It is also possible to define new MVS assets (e.g. different power plants, storages or energy providers, transformers etc.). Please see the `MVS documentation on simulating with the MVS <https://multi-vector-simulator.readthedocs.io/en/latest/simulating_with_the_mvs.html>`_ for more information.
When setting up your own input files, please make sure that your individual input folder contains *all* available files. Even though you can change the values of the parameters, the files themselves, their naming and structure cannot be changed. As mentioned above, there are also three input folders  (one for each example) in the ``examples/example_user_inputs/`` directory that resemble specific scenario setups for
sector coupled and electricity sector scenarios. For a start we recommend to study the example input files and set up your own inputs according to the example folders and by adding (or deleting) components from the ``data/user_inputs_collection`` directory.

Here's a very short description of the different input files:

**pvcompare_inputs**
- ``pv_setup.csv``: Definition of PV assets (technology, tilt angle, azimuth angle, roof-top or facade installation)
- ``building_parameters.csv``: Definition of characteristics of the building type that should be considered in the simulation.
- ``heat_pumps_and_chillers.csv``: Definition of characteristics of the heat pumps and chillers in the simulated energy system.

**mvs_inputs/csv_elements**

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
If you run a simulation, *pvcompare* automatically downloads the ERA5 weather data from `Climate Data Store (CDS) <https://cds.climate.copernicus.eu/>`_ and store it locally in ``data/static_inputs``, unless the
file already exists. In order to enable this download you first need to make an account at the `CDS <https://cds.climate.copernicus.eu/user/login?destination=%2F%23!%2Fhome>`_ and
install the cdsapi package. `This page <https://cds.climate.copernicus.eu/api-how-to>`_ provides information about the installation. When using the API for a large about of data (e.g. a year for one location) the request gets queued and the download might take a while.

**Provide your own weather data**

As an alternative `oemof feedinlib <https://feedinlib.readthedocs.io/en/releases-0.1.0/load_era5_weather_data.html>`_ provides a jupyter notebook with instructuions on how to download data for a single coordinate or a region.

toto: add more information here (IS)



Add a sensitivy to your simulations
===================================

If you want to add a sensitivity to your simulation by varying one parameter, you can use the :py:func:`~.analysis.loop_mvs` or :py:func:`~.analysis.loop_pvcompare` functionality, depending
on whether the parameter you want to vary is a *pvcompare* or a *MVS* parameter.

The following *pvcompare* parameters can be varied:

- location (country, lat, lon)
- year (e.g. 2018)
- storeys (number of storeys of the buildings)
- technology (PV technologies: si, cpv or psi
- hp_temp (upper bound temperature for the heat pump (external outlet temperature at the condenser))

Further, all *MVS* parameters can be varied by specifying the csv file, the column name and the parameter name to be changed.
Please note that in each sensitivity analysis only *one* parameter can be varied.

For more information see :py:func:`~.analysis.loop_mvs` and :py:func:`~.analysis.loop_pvcompare`.
