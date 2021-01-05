"""
run these tests with `pytest tests/name_of_test_module.py` or `pytest tests`
or simply `pytest` pytest will look for all files starting with "test_" and run
all functions within this file starting with "test_". For basic example of
tests you can look at our workshop
https://github.com/rl-institut/workshop/tree/master/test-driven-development.
Otherwise https://docs.pytest.org/en/latest/ and
https://docs.python.org/3/library/unittest.html are also good support.
"""

import os
import pvcompare.constants as constants
from pvcompare.area_potential import calculate_area_potential


class TestCalculateAreaPotential:
    @classmethod
    def setup_class(self):
        self.user_inputs_pvcompare_directory = constants.TEST_USER_INPUTS_PVCOMPARE

    def test_storeys_of_calculate_area_potential(self):

        a = calculate_area_potential(
            storeys=5,
            user_inputs_pvcompare_directory=self.user_inputs_pvcompare_directory,
            surface_type="flat_roof",
        )
        assert a == 197120.0
