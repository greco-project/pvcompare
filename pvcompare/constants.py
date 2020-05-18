import os


# default input directory for pvcompare
DEFAULT_INPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "data/inputs/")
# default input directory for mvs
DEFAULT_MVS_INPUT_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/mvs_inputs/"
)
# default output directory for mvs
DEFAULT_MVS_OUTPUT_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/mvs_outputs"
)
TEST_DATA_DIRECTORY = os.path.join(
    os.path.dirname(os.path.join("", os.pardir)), "tests/test_data/",
)
DUMMY_TEST_DATA = os.path.join(
    os.path.dirname(os.path.join("", os.pardir)), "tests/test_data/dummy_data",
)
