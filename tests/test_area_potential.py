import pytest
import pandas as pd
import numpy as np
import os

from pvcompare.area_potential import calculate_area_potential


class TestCalculateAreaPotential:
    def test_storeys_of_calculate_area_potential(self):

        input_dir = os.path.join(os.path.dirname(__file__), "../pvcompare/data/inputs/")
        a = calculate_area_potential(
            population=6000, input_directory=input_dir, surface_type="flat_roof",
        )
        assert a == 24640.0
