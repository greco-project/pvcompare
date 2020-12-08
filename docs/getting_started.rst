==================
Getting started
==================

Documentation
=============

The full documentation can be found at `readthedocs <http://pvcompare.readthedocs.org>`_.

Installation
============

To install *pvcompare* follow these steps:

- Clone *pvcompare* and navigate to the directory ``\pvcompare`` containing the ``setup.py`` and ``requirements.txt``:

::

   git clone git@github.com:greco-project/pvcompare.git
   cd pvcompare

- Install the ``requirements.txt`` and the package:

::

   pip install -r requirements.txt
   pip install -e .

- For the optimization you need to install a solver. Your can download the open source `cbc-solver <https://projects.coin-or.org/Cbc>`_ from https://ampl.com/dl/open/cbc/ . Please follow the installation `steps <https://oemof-solph.readthedocs.io/en/latest/readme.html#installing-a-solver>`_ in the oemof installation instructions. You also find information about other solvers there.

Examples and basic usage
========================
The basic usage of *pvcompare* is explained in section :ref:`basic_usage`.
You can look into the section :ref:`scenarios-results` for examples of simulations with *pvcompare*.

Contributing
============

We are warmly welcoming all who want to contribute to *pvcompare*.
Please read our `Contributing Guidelines <https://github.com/greco-project/pvcompare/blob/dev/CONTRIBUTING.md>`_.