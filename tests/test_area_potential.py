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
from pvcompare.area_potential import calculate_area_potential


class TestCalculateAreaPotential:
    @classmethod
    def setup_class(self):
        self.test_input_directory = os.path.join(
            os.path.dirname(__file__), "test_data/test_pvcompare_inputs"
        )

    def test_storeys_of_calculate_area_potential(self):

        a = calculate_area_potential(
            population=6000,
            user_input_directory=self.test_input_directory,
            surface_type="flat_roof",
        )
        assert a == 24640.0
