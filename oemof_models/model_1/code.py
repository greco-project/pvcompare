# import necessary libraries

import logging
import oemof
import pandas as pd
import matplotlib.pyplot as plt

from oemof.solph import (Sink, Source, Bus, Flow, EnergySystem, Investment, Model)
from oemof.solph.components import GenericStorage
from oemof.outputlib import processing, views
import pprint as pp

from oemof.tools import economics

oemof.tools.logger.define_logging(logfile='oemof example.log', screen_level=logging.INFO, file_level=logging.DEBUG)

# Creating the energy system

date_time_index = pd.date_range('1/1/2018', periods=24 * 365, freq='H')

es = EnergySystem(timeindex=date_time_index)

filename = 'data_timeseries.csv'
data = pd.read_csv(filename, sep=",")
logging.info('Energy system created and initialized')

# Creating the necessary buses

elbus = Bus(label='electricity')

logging.info('Necessary buses for the system created')

# Now creating the necessary components for the system

epc_pv = economics.annuity(capex=1000, n=20, wacc=0.05)
epc_storage = economics.annuity(capex=100, n=5, wacc=0.05)

pv = Source(label='pv', outputs={elbus: Flow(actual_value=data['pv'], nominal_value=None,
                                             fixed=True, investment=Investment(ep_costs=epc_pv, maximum=30))})


demand_el = Sink(label='demand_el', inputs={elbus: Flow(nominal_value=1, actual_value=data['demand_el'], fixed=True)})
excess_el = Sink(label='excess_el', inputs={elbus: Flow(variable_costs=-0.005)})
shortage_el = Source(label='shortage_el', outputs={elbus: Flow(variable_costs=1e20)})

el_storage = GenericStorage(label='el_storage',
                            inputs={elbus: Flow(variable_costs=0.0001)},
                            outputs={elbus: Flow()},
                            loss_rate=0.00,
                            initial_storage_level=0.5,
                            invest_relation_input_capacity=1 / 6,
                            invest_relation_output_capacity=1 / 6,
                            inflow_conversion_factor=0.9,
                            outflow_conversion_factor=0.9,
                            investment=Investment(ep_costs=epc_storage))

# Adding all the components to the energy system

es.add(excess_el, demand_el, el_storage, shortage_el, pv, elbus)

# Create the model for optimization and run the optimization

opt_model = Model(es)
opt_model.solve(solver='cbc')

logging.info('Optimization successful')

# Collect and plot the results

results = processing.results(opt_model)

results_el = views.node(results, 'electricity')
meta_results = processing.meta_results(opt_model)
pp.pprint(meta_results)

el_sequences = results_el['sequences']

to_el = {key[0][0]: key for key in el_sequences.keys() if key[0][1] == 'electricity' and key[1] == 'flow'}
to_el = [to_el.pop('pv')] + list(to_el.values())
el_prod = el_sequences[to_el]

fig, ax = plt.subplots(figsize=(14, 6))
el_prod.plot.area(ax=ax)
el_sequences[(('electricity', 'demand_el'), 'flow')].plot(ax=ax, linewidth=3, c='k')
el_sequences[(('electricity', 'excess_el'), 'flow')].plot(ax=ax, linewidth=3)
el_sequences[(('electricity', 'el_storage'), 'flow')].plot(ax=ax, linewidth=3, c='b')
legend = ax.legend(loc='upper right', bbox_to_anchor=(1.0, 0.5))

plt.show()
print(el_sequences.sum(axis=0))

my_results = results_el['scalars']

# installed capacity of storage in MWh
my_results['storage_invest_MWh'] = (results[(el_storage, None)]
['scalars']['invest'])

# installed capacity of PV power plant in MW
my_results['PV_invest_MW'] = (results[(pv, elbus)]
['scalars']['invest'])

pp.pprint(my_results)
