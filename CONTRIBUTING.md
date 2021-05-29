## Development of pvcompare

### Prerequisites

- [Git](https://git-scm.com/)
- Clone https://github.com/greco-project/pvcompare.git or `git@github.com:greco-project/pvcompare.git` (SSH) and install the cloned repository using pip with the developer and documentation extras:

```bash
cd pvcompare
pip install -e .[dev, docs]
```

### Philosophy

Development of a feature for this repository should be aligned with the workflow described 
by [Vincent Driessen](https://nvie.com/posts/a-successful-git-branching-model/).

Here is the minimal procedure you should follow: 

#### Step 1: Create an issue.
 
 Create [an issue](https://help.github.com/en/articles/creating-an-issue) on the github repository, describing the problem you will then address with your feature/fix.
This is an important step as it forces one to think about the issue (to describe an issue to others, one has to think it through first).

#### Step 2: Create a branch to work on the issue.

1. Create a separate branch from `dev` (make sure you have the latest version of `dev`), to work on
    ```bash
    git checkout -b feature/description_of_feature dev
    ```
    The convention is to start the branch name with its functionality, e.g. `feature/` or `fix/`.  The second part describes shortly what the feature/fix is about.

2. Try to follow [these conventions](https://chris.beams.io/posts/git-commit) for commit messages:
    - Keep the subject line [short](https://chris.beams.io/posts/git-commit/#limit-50) (i.e. do not commit more than a few changes at the time)
    - Use [imperative](https://chris.beams.io/posts/git-commit/#imperative) for commit messages 
    - Do not end the commit message with a [period](https://chris.beams.io/posts/git-commit/#end) 

3. Push your local branch on the remote server immediately so
 that everyone knows you are working on it, you are also encouraged to create a draft pull request (see Step 4).


#### Step 3: Run tests locally

After creating a pull request (step 4) tests will run automatically but you can also run them locally - this is especially helpful in case a tests fails and you need debugging for finding the error.
To install all packages required for the integration tests locally run:
```bash
pip install -e .[dev]
```

Run tests locally by:
```bash
pytest
```

If a test fails, it is only due to what you changed (the test must passed before the code is
 merged, so you know that the tests were passing before you start working on your branch). The
  test names and error messages are there to help you find the error, please read them to try to
   debug yourself before seeking assistance.

As some tests run full simulations they take a long time and are therefore not run at every push, but are disabled by default.
Before you ask for a review please run all tests locally by:
 ```bash
EXECUTE_TESTS_ON=master pytest
```

#### Step 4: Submit a pull request (PR)

Follow the [steps](https://help.github.com/en/articles/creating-a-pull-request) of the github help to create the PR.
Please note that you PR should be directed from your branch (for example `feature/myfeature`) towards the branch `dev`.

You can start with a draft pull request (see [step 6](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request#creating-the-pull-request) of github help) to let the other developers know that you are working on the issue and  unblock if for review once your feature is finished.
 
Please follow the indications in the pull request template and update the appropriate checkboxes.

Once you are satisfied with your PR you should ask someone to review it. Before that please lint
 your code with [Black](https://github.com/psf/black) (run `black . --exclude docs/`).

## Documentation on Readthedocs

The documentation of pvcompare is compiled with the content of the folder "docs". 
Make sure you have installed the documentation extras:

```bash
pip install -e .[docs]
```

After editing, build the documentation locally by running

```bash
 sphinx-build -b html ~/path/to/pvcompare/docs/ ~/path/to/pvcompare/pvcompare_docs/
```

to check the results by opening the html files in the directory `pvcompare_docs`.

An introduction to creating the readthedocs with Sphinx is given here: https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html.

## How to release

Currently *pvcompare* is not released on pypi, but only on github. Please follow the instructions to create a new release on github. Check [GitHub Docs](https://docs.github.com/en/github/administering-a-repository/managing-releases-in-a-repository) for more information on releases.

### Preparations
1. Create a release branch by branching off from `dev` branch by
    ```bash
    git checkout -b release/vX.Y.Z dev
    ```
    Please use [semantic versioning guidelines](https://semver.org/spec/v2.0.0.html) for `X`, `Y` and `Z`.
2. In the release branch update the version number in [`__init__.py`](https://github.com/greco-project/pvcompare/blob/dev/pvcompare/__init__.py) and [`setup.py`](https://github.com/greco-project/pvcompare/blob/dev/setup.py).
3. Adapt the header `[Unreleased]` of [Changelog.md](https://github.com/greco-project/pvcompare/blob/dev/CHANGELOG.md) with the version number and the date of the release in [ISO format](https://xkcd.com/1179/): `[Version] - YYYY-MM-DD`.
4. Push your changes in 2. and 3. to your release branch (commit message e.g. "Bump version number and adapt Changelog.md for release")
5. Install pvcompare in a clean virtual environment on `release/vX.Y.Z` branch (navigate to directory where `setup.py` is located):
   ```bash
      pip install -e .[dev,docs]
   ```
6. Run all tests locally in this new environment (step 5) by `EXECUTE_TESTS_ON=master pytest`.
7. If there are errors, fix them in the release branch. If you fix something in the `setup.py` please test the installation in clean virtual environment again (see step 4).
8. When `EXECUTE_TESTS_ON=master pytest` passes, push your release branch, create a pull request towards `master` and merge.
9. Wait until the [build](https://github.com/greco-project/pvcompare/actions) on `master` branch passes.

### The actual release
1. Draft a new release on [github](https://github.com/greco-project/pvcompare/releases/) and choose `master` as target.
2. As tag version use `vX.Y.Z`.
3. Type a descriptive title and copy the [Changelog entries](https://github.com/greco-project/pvcompare/blob/dev/CHANGELOG.md) as description of the release.
4. Use checkbox "this is a pre-release" to indicate that the model may be unstable.

### After the release
1. Locally, merge `release/vX.Y.Z` into `dev` and push to the remote version of dev.
2. In your `dev` branch, set the version for next release in [`__init__.py`](https://github.com/greco-project/pvcompare/blob/dev/pvcompare/__init__.py) and [`setup.py`](https://github.com/greco-project/pvcompare/blob/dev/setup.py): for example `0.0.3dev`
3. Add the structure for a new `unreleased` version to the [`CHANGELOG.md`](https://github.com/greco-project/pvcompare/blob/dev/CHANGELOG.md):
    ```
    ## [unreleased]

    ### Added
    -
    ### Changed
    -
    ### Removed
    -
    ### Fixed
    -
    ```
4. Commit and push your changes to `dev`.
5. Party :)
