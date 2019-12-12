'''
This script has a second model where the idea for a big storage acting as a grid to simulate NZEB will be implemented.
'''
# import necessary libraries

import logging
import oemof
import pandas as pd

from oemof.solph import (Sink, Source, Bus, Flow, EnergySystem, Investment, Model)
from oemof.solph.components import GenericStorage
from oemof.outputlib import processing, views
import pprint as pp

from oemof.tools import economics

oemof.tools.logger.define_logging(logfile='oemof example.log', screen_level=logging.INFO, file_level=logging.DEBUG)

# Creating the energy system

date_time_index = pd.date_range('1/1/2018', periods=24*365, freq='H')

es = EnergySystem(timeindex=date_time_index)

filename = 'data_timeseries.csv'
data = pd.read_csv(filename, sep=",")

logging.info('ENERGY SYSTEM created and initialized')

# Creating the necessary buses

elbus = Bus(label='elbus')

logging.info('Necessary buses for the system created')

# Now creating the necessary components for the system

epc_pv = economics.annuity(capex=1000, n=20, wacc=0.05)
epc_storage = economics.annuity(capex=1000, n=5, wacc=0.05)

pv = Source(label='pv', outputs={elbus: Flow(actual_value=data['pv'], nominal_value=None,
                                              fixed=True, investment=Investment(ep_costs=epc_pv))})

demand_el = Sink(label='demand_el', inputs={elbus: Flow(nominal_value=1, actual_value=data['demand_el'], fixed=True)})

# excess_el = Sink(label='excess_el', inputs={elbus: Flow(variable_costs=0)})
# shortage_el = Source(label='shortage_el', outputs={elbus: Flow(variable_costs=1e30)})

el_storage = GenericStorage(label='el_storage',
                            inputs={elbus: Flow(variable_costs=0.0001)},
                            outputs={elbus: Flow()},
                            loss_rate=0.00,
                            initial_storage_level=0.6, balanced=True,
                            invest_relation_input_capacity=1 / 6,
                            invest_relation_output_capacity=1 / 6,
                            inflow_conversion_factor=0.9,
                            outflow_conversion_factor=0.9,
                            investment=Investment(ep_costs=epc_storage))

grid = GenericStorage(label='grid',
                            inputs={elbus: Flow(variable_costs=-0.005)},
                            outputs={elbus: Flow(variable_costs=1.5)},
                            loss_rate=0.00, nominal_storage_capacity=10000000,
                            initial_storage_level=0.5, balanced=True,
                            invest_relation_input_capacity=1,
                            invest_relation_output_capacity=1,
                            inflow_conversion_factor=1,
                            outflow_conversion_factor=1)

# Adding all the components to the energy system

es.add(demand_el, el_storage, pv, elbus, grid)

# Create the model for optimization and run the optimization

opt_model = Model(es)
opt_model.solve(solver='cbc')

logging.info('Optimization successful')

# Collect and plot the results

results = processing.results(opt_model)

custom_storage = views.node(results, 'el_storage')
electricity_bus = views.node(results, 'elbus')

meta_results = processing.meta_results(opt_model)
pp.pprint(meta_results)

my_results = electricity_bus['scalars']

# installed capacity of storage in MWh
my_results['storage_invest_MWh'] = (results[(el_storage, None)]
                                    ['scalars']['invest'])

# installed capacity of PV power plant in MW
my_results['PV_invest_MW'] = (results[(pv, elbus)]
                              ['scalars']['invest'])

pp.pprint(my_results)
