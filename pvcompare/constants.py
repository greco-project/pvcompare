import os

# path to the root of this repository (assumes this file is in src folder)
REPO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# default input directory for pvcompare
DEFAULT_STATIC_INPUT_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/static_inputs/"
)
DEFAULT_USER_INPUT_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/user_inputs/pvcompare/"
)
# default input directory for mvs
DEFAULT_MVS_INPUT_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/user_inputs/mvs_inputs/"
)
DEFAULT_COLLECTION_MVS_INPUTS_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/user_inputs_collection/mvs_inputs/"
)
DEFAULT_OUTPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), "data/outputs")

# test directories
TEST_OUTPUT_DIRECTORY = os.path.join(REPO_PATH, "tests/data/outputs"
        )
TEST_USER_INPUTS_PVCOMPARE = os.path.join(REPO_PATH, "tests/data/user_inputs/pvcompare_inputs"
        )
TEST_USER_INPUTS_MVS = os.path.join(REPO_PATH, "tests/data/user_inputs/mvs_inputs"
        )
TEST_STATIC_INPUTS = os.path.join(REPO_PATH, "tests/data/static_inputs"
        )
TEST_COLLECTION_MVS_INPUTS_DIRECTORY = os.path.join(REPO_PATH, "tests/data/user_inputs_collection/mvs_inputs")

TEST_DATA_HEAT = os.path.join(REPO_PATH, "tests/test_data/test_inputs_heat")
