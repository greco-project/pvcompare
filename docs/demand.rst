
.. _demand:

Electricity and heat demand modeling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The load profiles of the demand (electricity and heat) are calculated for a
given population (calculated from number of storeys), a certain country and year. The profile is generated with the
help of `oemof.demandlib <https://demandlib.readthedocs.io/en/latest/description.html>`_.

Electricity demand
==================

For the electricity demand, the BDEW load profile for households (H0) is scaled with the annual
demand of a certain population.
Therefore the annual electricity demand is calculated by the following procedure:

1)  the national residential electricity consumption for a country is calculated
    with the following procedure. The data for the total electricity consumprion
    as well as the fractions for space heating (SH), water heating (WH) and cooking
    are requested from `EU Building Database <https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use>`_.

.. math::
    \text{nec} &= \text{tec}(country, year) \\
        &- \text{esh}(country, year) \\
        &- \text{ewh}(country, year) \\
        &+ \text{tc}(country, year) \\
        &- \text{ec}(country, year) \\

    \text{with } nec &= \text{national energy consumption} \\
    \text{tec} &= \text{total electricity consumption} \\
    \text{esh} &= \text{electricity space heating} \\
    \text{ewh} &= \text{electricity water heating} \\
    \text{tc} &= \text{total cookin}g \\
    \text{ec} &= \text{electicity cooking} \\

2)  the population of the country is requested from `EUROSTAT <https://ec.europa.eu/eurostat/tgm/table.do?tab=table&init=1&plugin=1&language=en&pcode=tps00001>`_.
3)  the total residential demand is divided by the countries population and
    multiplied by the house population. The house population is calculated
    by the number of storeys and the number of people per storey.
4)  The load profile is shifted due to country specific behaviour following the
    approach of HOTMAPS. For further information see p.127 in
    `HOTMAPS <https://www.hotmaps-project.eu/wp-content/uploads/2018/03/D2.3-Hotmaps_for-upload_revised-final_.pdf>`_.

Figure `Electricity demand`_ shows an exemplary electricty demand for Spain, 2013.

.. _Electricity demand:

.. figure:: ./images/input_timeseries_Electricity_demand.png
    :width: 100%
    :alt: Energy yield per kWp (left) and per m² (right) for Berlin and Madrid in 2014.
    :align: center

    Exemplary electricty demand for Spain, 2013.


Heat demand
===========

The heat demand is calculated for a given number of houses with a given
number of storeys, a certain country and year. The BDEW standard load profile
is used. This standard load profile is derived for german households. Because
there is no other standard load profiles available for other countries, the german
standard load profiles is used for all countries as an approximation.

The standard load profile is scaled with the annual heat demand for the given
population. The annual heat demand is calculated by the following procedure:

1)  the residential heat demand for a country is requested from `EU Building Database <https://ec.europa.eu/energy/en/eu-buildings-database#how-to-use>`_. Only the
    Space Heating is used in the simulations (TODO: How to include WH).
2)  on the lines of the electricity demand, the population of the country is requested from `EUROSTAT <https://ec.europa.eu/eurostat/tgm/table.do?tab=table&init=1&plugin=1&language=en&pcode=tps00001>`_.
3)  the total residential demand is divided by the countries population and
    multiplied by the house population that is calculated by the storeys
    of the house and the number of people in one storey
4)  The load profile is shifted due to countries specific behaviour following the
    approach of HOTMAPS. For further information see p.127 in
    `HOTMAPS <https://www.hotmaps-project.eu/wp-content/uploads/2018/03/D2.3-Hotmaps_for-upload_revised-final_.pdf>`_.

Figure `Heat demand`_ shows an exemplary electricty demand for Spain, 2013.

.. _Heat demand:

.. figure:: ./images/input_timeseries_Heat_demand.png
    :width: 100%
    :alt: Energy yield per kWp (left) and per m² (right) for Berlin and Madrid in 2014.
    :align: center

    Exemplary heat demand for Spain, 2013.