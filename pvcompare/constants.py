import os

# path to the root of this repository (assumes this file is in src folder)
REPO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# default input directory for pvcompare
DEFAULT_STATIC_INPUTS_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/static_inputs/"
)
DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/user_inputs/pvcompare_inputs/"
)
# default input directory for mvs
DEFAULT_USER_INPUTS_MVS_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/user_inputs/mvs_inputs/"
)
DEFAULT_COLLECTION_MVS_INPUTS_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "data/user_inputs_collection/mvs_inputs/"
)
DEFAULT_OUTPUTS_DIRECTORY = os.path.join(os.path.dirname(__file__), "data/outputs")

# example directories
EXAMPLE_DIRECTORY = os.path.join(REPO_PATH, "examples")
EXAMPLE_OUTPUTS_DIRECTORY = os.path.join(REPO_PATH, "examples/example_outputs")
EXAMPLE_USER_INPUTS_PVCOMPARE = os.path.join(
    REPO_PATH, "examples/example_user_inputs/pvcompare_inputs"
)
EXAMPLE_USER_INPUTS_MVS_ELECTRICITY = os.path.join(
    REPO_PATH, "examples/example_user_inputs/mvs_inputs_electricity_sector"
)
EXAMPLE_USER_INPUTS_MVS_SECTOR_COUPLING = os.path.join(
    REPO_PATH, "examples/example_user_inputs/mvs_inputs_sector_coupling"
)

# test directories
TEST_OUTPUTS_DIRECTORY = os.path.join(REPO_PATH, "tests/data/outputs")
TEST_USER_INPUTS_PVCOMPARE = os.path.join(
    REPO_PATH, "tests/data/user_inputs/pvcompare_inputs"
)
TEST_USER_INPUTS_MVS = os.path.join(REPO_PATH, "tests/data/user_inputs/mvs_inputs")
TEST_STATIC_INPUTS = os.path.join(REPO_PATH, "tests/data/static_inputs")
TEST_COLLECTION_MVS_INPUTS_DIRECTORY = os.path.join(
    REPO_PATH, "tests/data/user_inputs_collection/mvs_inputs"
)
