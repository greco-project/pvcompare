|badge_docs| |badge_CI| |badge_coverage| |badge_zenodo|

Deprecated: |badge_travis| 

.. |badge_docs| image:: https://readthedocs.org/projects/pvcompare/badge/?version=latest
    :target: https://pvcompare.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |badge_CI| image:: https://github.com/greco-project/pvcompare/actions/workflows/main.yml/badge.svg
    :target: https://github.com/greco-project/pvcompare/actions/workflows/main.yml
    :alt: Build status

.. |badge_coverage| image:: https://coveralls.io/repos/github/greco-project/pvcompare/badge.svg?branch=dev
    :target: https://coveralls.io/github/greco-project/pvcompare?branch=dev
    :alt: Test coverage

.. |badge_travis| image:: https://travis-ci.com/greco-project/pvcompare.svg?branch=dev
    :target: https://travis-ci.com/greco-project/pvcompare

.. |badge_zenodo| image:: https://zenodo.org/badge/224614782.svg
   :target: https://zenodo.org/badge/latestdoi/224614782


pvcompare
~~~~~~~~~

Introduction
============

*pvcompare* is a model that compares the benefits of different PV technologies in a specified energy system by running
an energy system optimization. This model concentrates on the integration of PV technologies into local energy systems but could
easily be enhanced to analyse other conversion technologies.

The functionalities include

* calculation of an area potential for PV on rooftops and façades based on building parameters,
* calculation of heat and electricity demand time series for a specific amount of people living in these buildings,
* calculation of PV feed-in time series for a set of PV installations on rooftops and façades incl. different technologies,

    * all technologies in the database of `pvlib <https://pvlib-python.readthedocs.io/en/stable/index.html>`_,
    * a specific concentrator-PV module (`CPV <https://pvcompare.readthedocs.io/en/latest/model_assumptions.html#cpv>`_) and
    * a module of perovskite-silicon cells (`PeroSI <https://pvcompare.readthedocs.io/en/latest/model_assumptions.html#perosi>`_),

* calculation of temperature dependent COPs or respectively EERs for heat pumps and chillers,
* download and formatting of `ERA5 weather data <https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5>`_ (global reanalysis data set),
* preparation of data and input files for the energy system optimization,
* a sensitivity analysis for input parameters and
* visualisations for the comparison of different technologies.

The model is being developed within the scope of the H2020 project `GRECO <https://www.greco-project.eu/>`_.
The energy system optimization is based on the `oemof-solph <https://oemof-solph.readthedocs.io/en/latest/>`_ python package,
which *pvcompare* calls via the `Multi-Vector Simulator (MVS)  <https://github.com/rl-institut/multi-vector-simulator>`_, a
tool for assessing and optimizing Local Energy Systems (LES).

Documentation
=============

The full documentation can be found at `readthedocs <http://pvcompare.readthedocs.org>`_.

Installation
============

To install *pvcompare* follow these steps:

- Clone *pvcompare* and navigate to the directory ``\pvcompare`` containing the ``setup.py``:

::

   git clone git@github.com:greco-project/pvcompare.git
   cd pvcompare

- Install the package:

::

   pip install -e .

- For the optimization you need to install a solver. You can download the open source `cbc-solver <https://projects.coin-or.org/Cbc>`_ from https://ampl.com/dl/open/cbc/ . Please follow the installation `steps <https://oemof-solph.readthedocs.io/en/latest/readme.html#installing-a-solver>`_ in the oemof installation instructions. You also find information about other solvers there.

Examples and basic usage
========================
The basic usage of *pvcompare* is explained in the documentation in section `Basic usage of pvcompare <https://pvcompare.readthedocs.io/en/latest/basic_usage.html>`_.
Examples are provided on github in the directory `examples/ <https://github.com/greco-project/pvcompare/tree/master/examples>`_.

Contributing
============

We are warmly welcoming all who want to contribute to *pvcompare*.
Please read our `Contributing Guidelines <https://github.com/greco-project/pvcompare/blob/dev/CONTRIBUTING.md>`_.
You can also get in contact by writing an `issue on github <https://github.com/greco-project/pvcompare/issues/new/choose>`_.
