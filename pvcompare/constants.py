import os

# path to the root of this repository (assumes this file is in src folder)
REPO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
TEST_DATA_DIRECTORY = os.path.join(REPO_PATH, "tests/test_data/",)
DUMMY_TEST_DATA = os.path.join(REPO_PATH, "tests/test_data/dummy_data/",)
