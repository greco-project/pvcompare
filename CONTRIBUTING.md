## Development of pvcompare

### Prerequisites

- [Git](https://git-scm.com/)
- Clone https://github.com/greco-project/pvcompare.git or `git@github.com:greco-project/pvcompare.git` (SSH) and install the cloned repository using pip:

```bash
pip install -e /path/to/the/repository
```

### Philosophy

Development of a feature for this repository should be aligned with the workflow described 
by [Vincent Driessen](https://nvie.com/posts/a-successful-git-branching-model/).

Here is the minimal procedure you should follow : 

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
pip install -r tests/test_requirements.txt
```

Run tests locally by:
```bash
pytest
```

If a test fails, it is only due to what you changed (the test must passed before the code is
 merged, so you know that the tests were passing before you start working on your branch). The
  test names and error messages are there to help you find the error, please read them to try to
   debug yourself before seeking assistance.

#### Step 4: Submit a pull request (PR)

Follow the [steps](https://help.github.com/en/articles/creating-a-pull-request) of the github help to create the PR.
Please note that you PR should be directed from your branch (for example `feature/myfeature`) towards the branch `dev`.

You can start with a draft pull request (see [step 6](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request#creating-the-pull-request) of github help) to let the other developers know that you are working on the issue and  unblock if for review once your feature is finished.
 
Please follow the indications in the pull request template and update the appropriate checkboxes.

Once you are satisfied with your PR you should ask someone to review it. Before that please lint
 your code with [Black](https://github.com/psf/black) (run `black . --exclude docs/`).
