
.. _basic_usage:

Basic usage of pvcompare
~~~~~~~~~~~~~~~~~~~~~~~~

.. _run_simulation:

Run a simulation
================

You can easily run a simulation with *pvcompare* by running the file TODO (adjust after decision in #164).
More information to follow.

.. _define_params:

Define your own components and parameters
=========================================

*pvcompare* provides you with templates and default parameters for your simulations. However, you can also define your own energy system, choose different parameters and/or change the settings.

Please refer to `Simulating with the MVS <https://multi-vector-simulator.readthedocs.io/en/latest/simulating_with_the_mvs.html>`_ to learn
how to work with the input csv files and how to provide your own time series. In *pvcompare* these files are by default stored in the directory
``data/mvs_inputs``. You can define another input directory by providing the parameter ``mvs_input_directory`` to the :py:func:`~.main` and :py:func:`~.apply_mvs` functions.
Please note that *pvcompare* only works with csv files but not with `json files <https://multi-vector-simulator.readthedocs.io/en/latest/simulating_with_the_mvs.html#json-file-mvs-config-json>`_.

Further parameters are stored in the ``data/inputs`` directory. You can adapt this directory by providing the parameter ``input_directory`` to the :py:func:`~.main` and :py:func:`~.apply_mvs` functions.
Especially interesting for adapting your simulations will be:

- ``pv_setup.csv``: Definition of PV assets (technology, tilt angle, azimuth angle, roof-top or facade installation)
- ``building_parameters.csv``: Definition of characteristics of the building type that should be considered in the simulation.
- ``heat_pumps_and_chillers.csv``: Definition of characteristics of the heat pumps and chillers in the simulated energy system.

A full description of the parameters can be found in the section :ref:`parameters`.


Download ERA5 weather data
==========================
Info follows, see #68.



Add a sensitivy to your simulations
===================================

Here follows a description of how to use the :py:func:`~.automated_loop` functionality.