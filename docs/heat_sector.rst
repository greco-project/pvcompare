.. _heat-sector:

Heat pump and thermal storage modelling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Heat pumps and chillers
==========================

Different types of heat pumps and chillers can be modelled by adjusting their parameters in ``heat_pumps_and_chillers.csv`` accordingly.

Parameters which can be adjusted and passed are:

  * **mode**: Plant type which can be either ``heat_pump`` or ``chiller``
  * **technology**: Specific technology of the plant type which can  be 'air-air', 'air-water' or 'brine-water'
  * **quality_grade**: Plant-specific scale-down factor to carnot efficiency
  * **temp_high**: Outlet temperature / High temperature of heat reservoir
  * **temp_low** Inlet temperature / Low temperature of heat reservoir
  * **factor_icing**: COP reduction caused by icing (only for heat pumps)
  * **temp_threshold_icing**: Temperature below which icing occurs (only for heat pumps)

Please see the `documentation on compression heat pumps and chillers <https://oemof-thermal.readthedocs.io/en/stable/compression_heat_pumps_and_chillers.html>`_
of `oemof.thermal <https://github.com/oemof/oemof-thermal>`_ for further information.


1.1 Heat pumps
**************

In case of a heat pump **mode** and **temp_high** are required values, while passing **temp_low**, **factor_icing** and
**temp_threshold_icing** are optional. Besides either **quality_grade** or **technology** has to be passed.
The quality grade depends on the technology hence you need to provide a specification of the technology if you want to model the asset from default quality grades.
Default values are implemented for the following technologies: air-to-air, air-to-water and brine-to-water.
If you provide your own quality grade, passing **technology** is optional and will be set to an air source technology if passed empty or *NaN*.

To model an air source heat pump, **technology** is set to either **air-air** or **air-water** and the parameter **temp_low** is passed empty or with *NaN*.
In case you provide your own quality grade you do not need to specify the technology, since it will be set to the default: air source technology (**air-air** or **air-water**).
In this case the *COP* will be calculated from the weather data, to be more exact from the ambient temperature.
You can also provide your own time series of temperatures in a separate file as shown in this example of a ``heat_pumps_and_chillers.csv`` file:

.. code-block:: python

    mode,technology,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
    heat_pump,air-water,0.403,"{'file_name': 'temperature_heat_pump.csv', 'header': 'degC', 'unit': ''}",None,None


(In this example temperatures are provided in ``temperature_heat_pump.csv``, with *degC* as header of the column containing the temperatures.)

To model a water or brine source heat pump, you can either

* pass a time series of temperatures with a separate file as shown in the example below or

    .. code-block:: python

        mode,technology,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
        heat_pump,water-water,0.45,"{'file_name': 'temperatures_heat_pump.csv', 'header': 'degC', 'unit': ''}",None,None


    (In this example temperatures are provided in ``temperature_heat_pump.csv``, with *degC* as header of the column containing the temperatures.)

* pass a numeric with **temp_low** to model a constant inlet temperature:

    .. code-block:: python

        mode,technology,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
        heat_pump,brine-water,0.53,65,16,None,None

    (In this example with constant inlet temperature **temp_low**)

To model a brine source heat pump from ground temperature calculated in ``heat_pump_and_chiller.py``, **technology** is set to **brine-water** and the parameter **temp_low** is passed empty or with *NaN*:

    .. code-block:: python

        mode,technology,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
        heat_pump,brine-water,0.53,65,,None,None

    (In this example without passed inlet temperature **temp_low**)

In this case the *COP* will be calculated from the mean yearly ambient temperature, as an as simplifying assumption of the ground temperature according to `brandl_energy_2006 <https://www.icevirtuallibrary.com/doi/full/10.1680/geot.2006.56.2.81>`_

1.2 Chillers
************

.. warning:: At this point it is not possible to run simulations with a chiller. Adjustments need to be made in ``add_sector_coupling`` function of ``heat_pump_and_chiller.py``.

Modelling a chiller is carried out analogously. Here **mode** and **temp_low** are required values, while passing **temp_high** is optional.
The parameters **factor_icing** and **temp_threshold_icing** have to be passed empty or as *NaN* or *None*.

The quality grade depends on the technology hence you need to provide a specification of the technology if you want to model the asset from default quality grade.
So far there is only one default value implemented for an air-to-air chiller's quality grade. It has been obtained from `monitored data <https://oemof-thermal.readthedocs.io/en/latest/validation_compression_heat_pumps_and_chillers.html>`_ of the GRECO project.
If you provide your own quality grade, passing **technology** is optional and will be set to an air source technology if passed empty or *NaN*.

To model an air source chiller, **technology** is set to **air-air** and the parameter **temp_high** is passed empty or with *NaN*.
In case you provide your own quality grade you do not need to specify the technology, since it will be set to the default: air source technology (**air-air**).
In this case the *EER* will be calculated from the weather data, to be more exact from the ambient temperature.
You can also provide your own time series of temperatures in a separate file as in this example of a ``heat_pumps_and_chillers.csv`` file:

.. code-block:: python

    mode,technology,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
    chiller,air-air,0.3,"{'file_name': 'temperatures_chiller.csv', 'header': 'degC', 'unit': ''}",15,None,None


(In this example temperatures are provided in ``temperature_chiller.csv``, with *degC* as header of the column containing the temperatures.)

To model a water or brine source chiller, you can either

* provide a time series of temperatures in a separate file as shown in the example below or

    .. code-block:: python

        mode,technology,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
        chiller,water-water,0.45,"{'file_name': 'temperatures_chiller.csv', 'header': 'degC', 'unit': ''}",15,None,None


    (In this example temperatures are provided in ``temperature_chiller.csv``, with *degC* as header of the column containing the temperatures.)

* pass a numeric with **temp_high** to model a constant outlet temperature:

    .. code-block:: python

        mode,technology,quality_grade,temp_high,temp_low,factor_icing,temp_threshold_icing
        chiller,water-water,0.3,25,15,None,None

    (In this example with constant outlet temperature **temp_high**)
