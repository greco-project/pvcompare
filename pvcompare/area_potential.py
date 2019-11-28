# -*- coding: utf-8 -*-
"""

calculating the available area potential for PV-modules on the rooftop and facades

"""

import matplotlib.pyplot as plt
import pandas as pd
import os

def calculate_area_potential(population):

    """Calculates the area potential of the rooftop, south and east+west facades
    for a given population

    Parameters
    ----------
    population: int
        the population of the district

    Returns
    -------
    list
        the list contains: storeys, used_south_facade, used_eastwest_facade,
        total_floor_area, flatroof_area)
    """

    # read building parameters
    datapath = os.path.join(os.path.dirname(__file__),
                            'Data/building_parameters.csv')
    bp = pd.read_csv(datapath, index_col=0)
    bp=bp.T
    population_per_storey=bp.iloc[0]['population per storey']
    number_houses = bp.iloc[0]['number of houses']
    floor_area = bp.iloc[0]['total storey area']
    length_south_facade = bp.iloc[0]['length south facade']
    length_eastwest_facade = bp.iloc[0]['length eastwest facade']
    hight_per_storey=bp.iloc[0]['hight storey']

    #number of storeys for each building
    storeys= population/population_per_storey/number_houses

    flatroof_area = floor_area * number_houses
    # the south facing side of the gable roof with 45° elevation equals
    # 70% of the floor area
    gableroof_area = (floor_area * number_houses / 100) * 70
    total_floor_area = floor_area *number_houses * storeys

    # solar panels are only starting from the fourth storey (see Hachem2014)
    if storeys > 3:
        used_storeys = storeys - 3
        south_facade = length_south_facade * hight_per_storey * used_storeys * number_houses
        eastwest_facade = length_eastwest_facade * hight_per_storey * 2 * used_storeys *number_houses

        # 50 % of the south facade and 80% of the west and east facade can be used
        # due to windows (see Hachem2014)
        used_south_facade = south_facade/100 * 50
        used_eastwest_facade = eastwest_facade/100 * 80
    else:
        used_south_facade = 0
        used_eastwest_facade = 0

    print("number of storys:", storeys, "\n"
        "flat rooftop area:", flatroof_area, "\n"
            "gable rooftop area facing south:", gableroof_area, "\n"
          "south facade area:", used_south_facade, "\n"
          "eastwest facade area:", used_eastwest_facade, "\n")

    return(storeys, used_south_facade, used_eastwest_facade, total_floor_area,
           flatroof_area)

def plot_facade_potential(): #todo: delete this function?

    population = range(0, 1300, 120)
    storeys = {}
    south = {}
    eastwest = {}
    total_floor = {}

    for i in population:
        storeys[i], south[i], eastwest[i], total_floor[i] = \
            calculate_area_potential(population=i)

    st = pd.DataFrame(list(storeys.items()))
    st.columns = ['population', 'storeys']
    st.set_index('population', inplace=True)
    s = pd.DataFrame(list(south.items()))
    s.columns = ['population', 'south_facade']
    s.set_index('population', inplace=True)
    e = pd.DataFrame(list(eastwest.items()))
    e.columns = ['population', 'eastwest_facade']
    e.set_index('population', inplace=True)
    t = pd.DataFrame(list(total_floor.items()))
    t.columns = ['population', 'total_floor_area']
    t.set_index('population', inplace=True)

    area = pd.concat([st, s, e, t], axis=1)

    plt.plot(area['storeys'],
             area['south_facade'] / area['total_floor_area'] * 100,
             label='south_facade')
    plt.plot(area['storeys'],
             area['eastwest_facade'] / area['total_floor_area'] * 100,
             label='eastwest_facades')
    plt.ylabel('fraction of used facade to the total floor area')
    plt.xlabel('number of floors')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    calculate_area_potential(population=600)
#    plot_facade_potential()