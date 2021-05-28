# -*- coding: utf-8 -*-
"""
calculating the available area potential for PV-modules on the rooftop and facades

"""
import pandas as pd
import os
import logging
import pvcompare.constants as constants

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def calculate_area_potential(storeys, user_inputs_pvcompare_directory, surface_type):

    r"""
    Calculates the area potential for PV installations.

    Calculates the area potential of the roof top, south, east or west
    facade  depending on `surface_type`.

    Due to shading, the area potential for a flat roof is estimated to be 40%
    of the whole usable roof area.
    For more information see [1]_.

    Parameters
    ----------
    storeys: int
        The number of storeys of a building.
    user_inputs_pvcompare_directory: str or None
        Path to user input directory. If None,
        `constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY` is used.
        Default: None._USER_INPUTS_MVS_DIRECTORY` is used.
        Default: None.
    surface_type: str
        possible values: "flat_roof", "gable_roof", "east_facade",
        "west_facade" or "south_facade"

    Returns
    --------
    area: int
        Area potential of the roof top, south, east or west facade depending on `surface_type`.

    References
    ----------
    .. [1] Business Location Center: "Solarpotentialanalyse Berlin – Datendokumentation". Report, 2011, https://energieatlas.berlin.de/Energieatlas_Be/Docs/Datendokumentation-Solarkataster_BLN.pdf
    """

    # read building parameters
    logging.info("loading building parameters from building_parameters.csv ")
    data_path = os.path.join(user_inputs_pvcompare_directory, "building_parameters.csv")

    # load input parameters from building_parameters.csv
    bp = pd.read_csv(data_path, index_col=0)
    bp = bp.T
    population_per_storey = int(bp.iloc[0]["population per storey"])
    number_of_houses = int(bp.iloc[0]["number of houses"])
    floor_area = int(bp.iloc[0]["total storey area"])
    length_south_facade = int(bp.iloc[0]["length south facade"])
    length_east_west_facade = int(bp.iloc[0]["length eastwest facade"])
    hight_per_storey = int(bp.iloc[0]["hight storey"])
    population = storeys * population_per_storey * number_of_houses

    number_houses = population / (population_per_storey * storeys)
    if surface_type == "flat_roof":
        area = floor_area * number_houses * 0.4
    elif surface_type == "gable_roof":
        # the south facing side of the gable roof with 45° elevation equals
        # 70% of the floor area
        area = (floor_area * number_houses / 100) * 70 * 0.4

    else:
        # solar panels are only starting from the fourth storey (see Hachem2014)
        if storeys > 3:
            used_storeys = storeys - 3
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
        storeys=5,
        user_inputs_pvcompare_directory=constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY,
        surface_type="flat_roof",
    )
    print(area)
