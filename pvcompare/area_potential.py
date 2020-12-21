# -*- coding: utf-8 -*-
"""

calculating the available area potential for PV-modules on the rooftop and facades

"""
import pandas as pd
import os
import logging

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def calculate_area_potential(population, user_input_directory, surface_type):

    """
    Calculates the area potential.

    Calculates the area potential of the rooftop, south and east/west
    facades for a given population.

    Due to shading, the area potential for a flat roof is estimated to be 40%
    of the whole usable roof area.
    For more information see [1].

    [1] https://energieatlas.berlin.de/Energieatlas_Be/Docs/Datendokumentation-Solarkataster_BLN.pdf

    Parameters
    ----------
    population: int
        the population of the district
    user_input_directory: str or None
        Directory of the user inputs. If None,
        `constants.DEFAULT_USER_INPUT_DIRECTORY` is used as user_input_directory.
        Default: None.
    surface_type: str
        possible values: "flat_roof", "gable_roof", "east_facade",
        "west_facade" or "south_facade"

    Returns
    --------
    int
        area

    """

    # read building parameters
    logging.info("loading building parameters from building_parameters.csv ")
    data_path = os.path.join(user_input_directory, "building_parameters.csv")

    # load input parameters from building_parameters.csv
    bp = pd.read_csv(data_path, index_col=0)
    bp = bp.T
    population_per_storey = int(bp.iloc[0]["population per storey"])
    number_of_storeys = int(bp.iloc[0]["number of storeys"])
    floor_area = int(bp.iloc[0]["total storey area"])
    length_south_facade = int(bp.iloc[0]["length south facade"])
    length_east_west_facade = int(bp.iloc[0]["length eastwest facade"])
    hight_per_storey = int(bp.iloc[0]["hight storey"])

    number_houses = population / (population_per_storey * number_of_storeys)
    if surface_type == "flat_roof":
        area = floor_area * number_houses * 0.4
    elif surface_type == "gable_roof":
        # the south facing side of the gable roof with 45° elevation equals
        # 70% of the floor area
        area = (floor_area * number_houses / 100) * 70 * 0.4

    # number of storeys for each building

    else:
        # solar panels are only starting from the fourth storey (see Hachem2014)
        if number_of_storeys > 3:
            used_storeys = number_of_storeys - 3
            south_facade = (
                length_south_facade * hight_per_storey * used_storeys * number_houses
            )
            if surface_type == "east_facade" or surface_type == "west_facade":
                east_west_facade = (
                    length_east_west_facade
                    * hight_per_storey
                    * 2
                    * used_storeys
                    * number_houses
                )

            # 50 % of the south facade and 80% of the west and east facade can
            # be used
            # due to windows (see Hachem2014)
            if surface_type == "south_facade":
                area = south_facade / 100 * 50
            else:
                area = east_west_facade / 100 * 80
        else:
            area = 0

    logging.info(
        "The area potential has been calculated to be %s " % area
        + " qm for the surface type %s" % surface_type
    )
    return area


if __name__ == "__main__":

    area = calculate_area_potential(
        population=6000, user_input_directory="./data/user_inputs/", surface_type="flat_roof"
    )
    print(area)
