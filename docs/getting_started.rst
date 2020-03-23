==================
Getting started
==================

Introduction
=============

PVcompare is an oemof application that compares the benefit of different PV technologies for net zero energy buildings.

Please note that this repository is at an early stage of development.

Documentation
==============

Full documentation can be found at `readthedocs <http://pvcompare.readthedocs.org>`_.

Installation
============

The feedin module requires an installation of the `greco_technologies <https://github.com/greco-project/greco_technologies>`_
repository. Please clone the repository:

::

    git clone git@github.com:greco-project/greco_technologies.git

Go into the repository and checkout into the branch `CPV_dev`:

::

    cd ./greco_technologies
    git chechout CPV_dev

then you can install the developer version:

::

    pip install -e ./


PVcompare additionally requires an installation of the `mvs_tool`. Please follow the steps explained in the `Setup and installation` section of the `MVS tool <https://github.com/rl-institut/mvs_eland>`_.


Examples and basic usage
=========================


Contributing
==============

We are warmly welcoming all who want to contribute to the PVcompare.
Please read `CONTRIBUTING.md <https://github.com/greco-project/pvcompare/blob/dev/CONTRIBUTING.md>`_.
