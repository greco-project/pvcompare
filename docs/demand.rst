
.. _demand:

Electricity and heat demand modeling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The load profiles of the demand (electricity and heat) are calculated for a
given population, a certain country and year. The profile is generated with the
help of oemof.demandlib (https://demandlib.readthedocs.io/en/latest/description.html).

Electricity demand
==================

For the electricity demand, the BDEW load profile for households (H0) is scaled with the annual
demand. The annual electricity demand is calculated by the
following procedure:

1)  the national residential electricity consumption for a country is calculated
    with the following procedure. The data for the total electricity consumprion
    as well as the fractions for space heating (SH), water heating (WH) and cooking
    are requested from [2].

.. math::
    national energy consumption = (total electricity consumption(country, year) -
    electricity SH(country, year)
        - electricity WH(country, year)
        + (total cooking(country, year)
        - electicity cooking(country, year))
    )

2)  the population of the country is requested from EUROSTAT_population (LINK)
3)  the total residential demand is divided by the countries population and
    multiplied by the districts population. The district population is calulated
    by the number of storeys and the number of people per storey
4) The load profile is shifted due to country specific behaviour (see LINK)

[2] https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use


Heat demand
===========

The heat demand is calculated for a given number of houses with a given
number of storeys, a certain country and year. The BDEW standard load profile
is used. This standard load profile is derived for german households. Because
there is no other standard load profiles available for other countries, the german
standard load profiles is used for all countries as an approximation.

The standard load profile is scaled with the annual heat demand for the given
population. The annual heat demand is calculated by the following procedure:

1)  the residential heat demand for a country is requested from [2]. Only the
    Space Heating is used in the simulations (TODO: How to include WH)
2)  the population of the country is requested from EUROSTAT_population
3)  the total residential demand is devided by the countries population and
    multiplied by the districts population that is calculated by the storeys
    of the house and the number of people in one storey
4)  The load profile is shifted due to countrys specific behaviour

[2] https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use