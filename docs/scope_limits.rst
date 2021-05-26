.. _scope-limit:

Scope and limitations
~~~~~~~~~~~~~~~~~~~~~

The *pvcompare* model evolved during the H2020 project `GRECO <https://www.greco-project.eu/>`_ with the purpose of
analysing the integration of three innovative PV techologies, that are developed within the project, into energy systems
in comparison to the state of the art technologies. These three technologies are

- concentrator-PV (CPV),
- a multi-junction of perovskite and silicon (PSI) and
- PV powered heat pumps.

Therefore, the model focuses on photovoltaics, while including sector-coupling through heat pumps (and chillers).
However, a shift of focus is possible and can easily be integrated.
Concerning the components of the energy system, you can use any of the components listed in the `MVS documentation <https://multi-vector-simulator.readthedocs.io/en/v0.5.5/Model_Assumptions.html#component-models>`_.
There you also find information on packages for calculating feed-in time series of other fluctuating renewable energies than PV.
Checkout :ref:`define_params` for information on how to include more components into the simulated energy system.

*pvcompare* further focuses on residential areas in cities (also see :ref:`local_energy_system`).
Therefore, assumptions for demand and buildings (available area for PV on façades) are based on this use case.
However, users can provide their own demand time series, adjust the building assumptions (see :ref:`building_parameters`) or only allow roof-top PV (see :ref:`pv_setup`) in their simulations.
This way other use cases like detached houses (single-family houses) or industrial areas can be analyzed, as well.

The default energy system modelled with *pvcompare* has only one node, meaning that within the energy system, energy can be shared without restrictions through power connections between the buildings ("Coper Plate").
An analysis of the interconnection of several buildings with restrictions in power lines or due to billing are not content of this model.
However, a system with multiple nodes can be implemented with *pvcompare* by connecting single energy systems (e.g. of one building or a group of buildings) via multiple transfomer components.
The transmission capacity between the nodes can be restricted by either setting a maximum capacity constraint or an `installed capacity <https://multi-vector-simulator.readthedocs.io/en/v0.5.5/MVS_parameters.html#installedcap>`_, while setting `optimizeCap <https://multi-vector-simulator.readthedocs.io/en/v0.5.5/MVS_parameters.html#optimizecap>`_ to ``False``. This has not been tested, yet.

As *pvcompare* builds on other packages, there are inherited limitations. Checkout the `limitations of the MVS <https://multi-vector-simulator.readthedocs.io/en/v0.5.5/Model_Assumptions.html#limitations>`_.
