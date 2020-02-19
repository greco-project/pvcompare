
import pytest
import pandas as pd
import numpy as np
import os

from pvcompare.area_potential import (
    calculate_area_potential,
)


class TestCalculateAreaPotential:

    def test_storeys_of_calculate_area_potential(self):
        # todo choose clearer example/numbers
        storeys_exp = 492800
        input_dir = os.path.join(os.path.dirname(__file__),
                                 '../pvcompare/data/inputs/')
        a = calculate_area_potential(population=2400,
                                     input_directory=input_dir,
                                     surface_type='flat_roof')
        assert storeys_exp == a
