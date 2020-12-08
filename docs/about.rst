
.. _about:

About pvcompare
~~~~~~~~~~~~~~~
*pvcompare* is a model that compares the benefits of different PV technologies in a specified energy system by running
an energy system optimization. This model concentrates on the integration of PV technologies into local energy systems but could
easily be enhanced to analyse other conversion technologies.

The functionalities include

* calculation of an area potential for PV on roof-tops and facades based on building parameters,
* calculation of heat and electricity demand profiles for a specific amount of people living in these buildings,
* calculation of PV feed-in time series for a set of PV installations on roof-tops and facades incl. different technologies, such as:

    * all technologies in the database of `pvlib <https://pvlib-python.readthedocs.io/en/stable/index.html>`_,
    * a specific concentrator-PV module, and
    * a module of silicon-perovskite cells,

* calculation of temperature dependent COPs or respectively EERs for heat pumps and chillers,
* preparation of data and input files for the energy system optimization,
* a sensitivity analysis for input parameters and
* visualisations for the comparison of different technologies.

The model is being developed within the scope of the H2020 project `GRECO <https://www.greco-project.eu/>`_.
The energy system optimization is based on the `oemof-solph <https://oemof-solph.readthedocs.io/en/latest/>`_ python package,
which *pvcompare* calls via the `Multi-Vector Simulator (MVS)  <https://github.com/rl-institut/multi-vector-simulator>`_, a
tool for assessing and optimizing Local Energy Systems (LES).
