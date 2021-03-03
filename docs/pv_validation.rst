
.. _pv-feedin:

Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validation of radiation data
============================
The weather data used for simulation is the Copernicus ERA5 reanalysis weather data.
It provides hourly data for atmospheric, land-surface and sea-state parameters with a
latitude-longitude grid of 0.25 x 0.25 degrees resolution. For more information
of the data set see `ERA5 <https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview>`_.

The calculation of diffuse horizontal irradiance (DHI), direct normal irradiance
(DNI) and global horizontal irradiance (GHI) is based on the ERA5 parameter
'Surface solar radiation downwards' (ssrd). The ssrd describes all radiation (direct
and diffuse in a downward direction and thus is used as the GHI.
Coming from the GHI, the DHI and DNI are calculated the following way:

.. math::
    DHI = GHI - DNI * cos(zenith)

.. math::
    DNI = pvlib.irradiance.dirint(GHI, ...)

With the pvlib function: `pvlib.irradiance.dirint <https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.irradiance.dirint.html#pvlib.irradiance.dirint>`_.

The DHI has been validated for three different locations (Berlin, Madrid and Oslo)
by comparing the ERA5 output to two other weather data sets such as the GlobalSolarAtlas
and PVGIS. Figure `Validation DHI`_ shows the yearly energy yield of DHI for 2014 for the
three locations.

.. _Validation DHI:

.. figure:: ./images/compare_dhi_reference.png
    :width: 80%
    :alt: Validation of DHI .
    :align: center

    Yearly energy yield of DHI for three locations and three weather data sets.



Validation of PV modeling
=========================
In `pv-feedin`_ the models used to generate feed-in time series for SI, CPV and
PSI technologies are presented. This section will show some results of the
calculated time series and discuss model assumptions.

The generated hourly time series over one year are normalized by the peak power
of each module. Figure `PV time series`_ shows the time series for all three technologies in year 2014.

.. _PV time series:

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

Figure `energy yield`_ shows the yearly energy yield per kWp on the lefthand side and the
yearly energy yield per m² on the right hand side. The plot demonstrates that the production
per kWp is the highest for SI. This is due to a high performance ratio of SI. The
performance ratio of Hybrid CPV is lower, thus the overall production per kWp
decreases. Nevertheless, when looking at the production per m², the Hybrid CPV technology as well
as the PSI technology performs better than SI, as expected, due to it's higher
efficiency.
Overall, the yield in Berlin is lower than in Madrid but also the
margin between the technologies
decreases in Berlin. This outcome is due to a  lower direct normal irradiance (DNI) in
Berlin which causes a decrease in the yield of the Hybrid CPV technology.

.. _energy yield:

.. figure:: ./images/PV_energy_yield_medium_years.png
    :width: 50%
    :alt: Energy yield per kWp (left) and per m² (right) for Berlin and Madrid in 2014.
    :align: center

    Energy yield per kWp (left) and per m² (right) for Berlin and Madrid in 2014.

Hybrid CPV
==========

Figure `Hybrid CPV`_ illustrates the energy yield for the different components of the
Hybrid CPV technology. The Flatplate component collects diffuse horizontal irradiance (DHI)
while the CPV components only collects direct normal irradiance (DNI). The Hybrid module
adds up both power outputs of the Flatplate and the CPV part. For more information
about the modeling of Hybrid CPV see `pv-feedin`_.

.. _Hybrid CPV:

.. figure:: ./images/CPV_energy_production.png
    :width: 60%
    :alt: Yearly energy yield of the Hybrid CPV and its components per m² for Berlin and Madrid in 2014.
    :align: center

    Yearly energy yield of the Hybrid CPV and its components per m² for Berlin and Madrid in 2014.
