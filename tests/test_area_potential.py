
import pytest
import pandas as pd
import numpy as np

from pvcompare.area_potential import (
    calculate_area_potential,
)


class TestCalculateAreaPotential:

    def test_storeys_of_calculate_area_potential(self):
        storeys_exp = 20
        a = calculate_area_potential(population=2400)
        assert storeys_exp == a[0]
