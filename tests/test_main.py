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
import pytest
import logging
from pvcompare import main
from pvcompare import constants
import multi_vector_simulator as mvs


def test_main(self):

    latitude = 52.5243700  # Madrid: 40.416775 # berlin: 52.5243700 oslo: 59.9127300 athens: 37.983810, Paris: 48.864716

    longitude = 13.4105300  # M: -3.703790 # berlin 13.4105300 oslo:10.7460900 	athens: 23.727539, paris: 2.349014
    year = 2014
    storeys = 5
    country = "Germany"
    scenario_name = "Test_loop_mvs"
    output_directory = constants.TEST_DATA_OUTPUT
    mvs_input_directory = os.path.join(constants.TEST_DATA_DIRECTORY,
                                       "test_inputs_loop_mvs")



    main.apply_pvcompare(
        latitude=latitude,
        longitude=longitude,
        year=year,
        storeys=storeys,
        country=country,
    )

    main.apply_mvs(
        scenario_name=scenario_name, output_directory=output_directory,
        mvs_input_directory=mvs_input_directory
    )

def test_mvs():
    """ """

    output_directory = constants.TEST_DATA_OUTPUT
    mvs_input_directory = os.path.join(constants.TEST_DATA_DIRECTORY,
                                       "test_inputs_loop_mvs")
    mvs.main(
        path_input_folder=mvs_input_directory,
        path_output_folder=output_directory,
        input_type="csv",
        overwrite=True,
        pdf_report=False,
        save_png=True,
    )