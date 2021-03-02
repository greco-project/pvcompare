
.. _pv-feedin:

Validation of PV modeling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In `pv-feedin`_ the models used to generate feed-in time series for SI, CPV and
PSI technologies are presented. This section will show some results of the
calculated time series and discuss model assumptions.

Normalized time series
======================
The generated hourly time series over one year are normalized by the peak power
of each module. Figure ... shows the time series for all three technologies in year 2014.

.. figure:: ./images/pv_timeseries_madrid_2015.png
    :width: 50%
    :alt: Normalized time series for Madrid, Spain in 2014.
    :align: center

    Normalized time series for Madrid, Spain in 2014.

Energy yield
============
The size and efficiency of the three modules used, age given in table `table1`_

.. _table1:

+------------+-----------------+---------------+
| Technology | Module Size (m) | Efficiency (%)|
+============+=================+===============+
| SI         | 1.6434          | 17            |
+------------+-----------------+---------------+
| CPV        | 0.1             | 32            |
+------------+-----------------+---------------+
| PSI        | 1.219           | 24.5          |
+------------+-----------------+---------------+

The following figure shows the yearly energy yield per kWp on the lefthand side and the
yearly energy yield per m² on the right hand side. The plot shows that the production
per kWp is the highest for SI. This is due to a high performance ratio of SI (~ 0.8). The
performance ratio of cpv with ~0.6-0.7 is lower, thus the overall production per kWp
is lower. Although when looking at the production per m², the CPV technology as well
as the PSI technology performs better than SI, as expected. Overall, the yield
in Berlin is lower than in Madrid but also the margin between the technologies
decreases in Berlin. This outcome is caused by lower direct normal irradiance in
Berlin which causes a decrease in the yield of the CPV Hybrid technology.

.. figure:: ./images/PV_energy_yield_medium_years.png
    :width: 50%
    :alt: Energy yield per kWp (left) and per m² (right) for Berlin and Madrid in 2014.
    :align: center

    Normalized time series for Madrid, Spain in 2014.

CPV
===

Figure ... will illustrate the energy yield for the different components of the
Hybrid CPV technology. The Flatplate component collects diffuse horizontal irradiance
while the CPV components only collects direct normal irradiance. The Hybrid module
adds up both power outputs of the Flatplate and the CPV part.

.. figure:: ./images/PV_energy_yield_medium_years.png
    :width: 50%
    :alt: Energy yield per kWp (left) and per m² (right) for Berlin and Madrid in 2014.
    :align: center

    Normalized time series for Madrid, Spain in 2014.
