# -*- coding: utf-8 -*-
"""

calculating the available area potential for PV-modules on the rooftop and facades

"""

import matplotlib.pyplot as plt
import pandas as pd
import os
import logging

def calculate_area_potential(population, input_directory, surface_type):

    """Calculates the area potential of the rooftop, south and east+west facades
    for a given population

    Parameters
    ----------
    population: int
        the population of the district

    Returns
    -------
    int
        surface_area
    """

    # read building parameters
    logging.info("loading building parameters from building_parameters.csv ")
    datapath = os.path.join(input_directory,
                                'building_parameters.csv')

    bp = pd.read_csv(datapath, index_col=0)
    bp=bp.T
    population_per_storey=bp.iloc[0]['population per storey']
    number_houses = bp.iloc[0]['number of houses']
    floor_area = bp.iloc[0]['total storey area']
    length_south_facade = bp.iloc[0]['length south facade']
    length_eastwest_facade = bp.iloc[0]['length eastwest facade']
    hight_per_storey=bp.iloc[0]['hight storey']

    if surface_type=="flat_roof":
        area = floor_area * number_houses
    elif surface_type=="gable_roof":
        # the south facing side of the gable roof with 45° elevation equals
        # 70% of the floor area
        area = (floor_area * number_houses / 100) * 70

    #number of storeys for each building

    else:
        storeys= population/population_per_storey/number_houses

        # solar panels are only starting from the fourth storey (see Hachem2014)
        if storeys > 3:
            used_storeys = storeys - 3
            south_facade = length_south_facade * hight_per_storey * \
                           used_storeys * number_houses
            eastwest_facade = length_eastwest_facade * hight_per_storey * 2 * \
                              used_storeys *number_houses

            # 50 % of the south facade and 80% of the west and east facade can be used
            # due to windows (see Hachem2014)
            if surface_type=="south_facade":
                area = south_facade/100 * 50
            else:
                area = eastwest_facade/100 * 80
        else:
                area = 0
    logging.info("The area potential has been calculated to be %s " %area +
                 " for the surface type %s" %surface_type)
    return(area)


# def plot_facade_potential(): #todo: delete this function?
#
#     population = range(0, 1300, 120)
#     storeys = {}
#     south = {}
#     eastwest = {}
#     total_floor = {}
#
#     for i in population:
#         storeys[i], south[i], eastwest[i], total_floor[i] = \
#             calculate_area_potential(population=i)
#
#     st = pd.DataFrame(list(storeys.items()))
#     st.columns = ['population', 'storeys']
#     st.set_index('population', inplace=True)
#     s = pd.DataFrame(list(south.items()))
#     s.columns = ['population', 'south_facade']
#     s.set_index('population', inplace=True)
#     e = pd.DataFrame(list(eastwest.items()))
#     e.columns = ['population', 'eastwest_facade']
#     e.set_index('population', inplace=True)
#     t = pd.DataFrame(list(total_floor.items()))
#     t.columns = ['population', 'total_floor_area']
#     t.set_index('population', inplace=True)
#
#     area = pd.concat([st, s, e, t], axis=1)
#
#     plt.plot(area['storeys'],
#              area['south_facade'] / area['total_floor_area'] * 100,
#              label='south_facade')
#     plt.plot(area['storeys'],
#              area['eastwest_facade'] / area['total_floor_area'] * 100,
#              label='eastwest_facades')
#     plt.ylabel('fraction of used facade to the total floor area')
#     plt.xlabel('number of floors')
#     plt.legend()
#     plt.show()


#if __name__ == '__main__':

    #    calculate_area_potential(population=48000)
    #    plot_facade_potential()