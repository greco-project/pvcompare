.. _heat-sector:

Heat pump and thermal storage modelling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Heat pumps and chillers
==========================

Different types of heat pumps and chillers can be modelled by adjusting their parameters in ``heat_pumps_and_chillers.csv`` accordingly.

Parameters which can be adjusted and passed are:

  * **mode**: Plant type which can be either heat_pump or chiller
  * **quality_grade**: Plant-specific scale-down factor to carnot efficiency
  * **temp_high**: Outlet temperature / High temperature of heat reservoir
  * **temp_low** Inlet temperature / Low temperature of heat reservoir
  * **factor_icing**: COP reduction caused by icing
  * **temp_threshold_icing**: Temperature below which icing occurs

Please see the `documentation on compression heat pumps and chillers <https://oemof-thermal.readthedocs.io/en/stable/compression_heat_pumps_and_chillers.html>`_
of `oemof.thermal <https://github.com/oemof/oemof-thermal>`_ for further information.


1.1 Heat pumps
**************

In case of a heat pump **mode**, **quality_grade** and **temp_high** are required values, while passing **temp_low**, **factor_icing** and
**temp_threshold_icing** are optional.

To model an air source heat pump the parameter **temp_low** is passed empty or with *NaN*.
In this case the *COP* will be calculated from the weather data, to be more exact from the ambient temperature.
You can also provide your own time series of temperatures in a separate file as shown in this example:

.. code-block:: python

    mode,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
    heat_pump,0.35,35,"{'file_name': 'temperature_heat_pump.csv', 'header': 'degC', 'unit': ''}",None,None


(In this example temperatures are provided in ``temperature_heat_pump.csv``. The file's header is *degC*.)

To model a water or brine source heat pump, you can either

* pass a time series of temperatures with a separate file as shown in the example below or

    .. code-block:: python

        mode,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
        heat_pump,0.35,35,"{'file_name': 'temperatures_heat_pump.csv', 'header': 'degC', 'unit': ''}",None,None


    (In this example temperatures are provided in ``temperature_heat_pump.csv``. The file's header is *degC*.)

* pass a numeric with **temp_low** to model a constant inlet temperature:

    .. code-block:: python

        mode,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
        heat_pump,0.35,35,10,None,None

    (In this example with constant inlet temperature **temp_low**)



1.2 Chillers
************

Modelling a chiller is carried out analogously. Here **mode**, **quality_grade** and **temp_low** are required values,
while passing **temp_high**, **factor_icing** and **temp_threshold_icing** are optional.

To model an air source chiller the parameter **temp_high** is passed empty or with *NaN*.
In this case the *EER* will be calculated from the weather data, to be more exact from the ambient temperature.
You can also provide your own time series of temperatures in a separate file:

.. code-block:: python

    mode,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
    chiller,0.35,"{'file_name': 'temperatures_chiller.csv', 'header': 'degC', 'unit': ''}",15,None,None


(In this example temperatures are provided in ``temperature_chiller.csv``. The file's header is *degC*.)

To model a water or brine source chiller, you can either

* provide a time series of temperatures in a separate file as shown in the example below or

    .. code-block:: python

        mode,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
        heat_pump,0.35,"{'file_name': 'temperatures_chiller.csv', 'header': 'degC', 'unit': ''}",15,None,None


    (In this example temperatures are provided in ``temperature_chiller.csv``. The file's header is *degC*.)

* pass a numeric with **temp_high** to model a constant outlet temperature:

    .. code-block:: python

        mode,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
        heat_pump,0.35,25,15,None,None

    (In this example with constant outlet temperature **temp_high**)