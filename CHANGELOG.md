# Changelog
All notable changes to this project will be documented in this file.

The format is inspired from [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and the versioning aim to respect [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Here is a template for new release sections

```
## [_._._] - 20XX-MM-DD

### Added
-
### Changed
-
### Removed
-
### Fixed
-
```

## [unreleased]

### Added
- Add config file for RTD `readthedocs.yml` (#276)
- Tests have been added which check if the examples of pvcompare run with exit code 0 (#284)
- Added basic model assumptions to RTD and introduced section "local energy system" in Model assumptions in RTD (#286)
- Added headings in `parameters.rst` to make references of these sections possible in RTD (#286)
- Improved "scope and limitations" section of RTD with additional information and corrections (#286)
- Add info on energy systems consisting of more than one node in RTD section "scope and limitations" (#293)
- Added description of the implementation of the stratified thermal storage in pvcompare with a description of the possibilities modeling it (#291)
- Dokumentation: Update on 'basic_usage', 'parameter description' and 'model assumptions' (#302)
- Add gas bus to `energyBusses.csv` in  `tests/data/user_inputs/mvs_inputs_sector_coupling/csv_elements` (#314)

### Changed
- The inlet temperatures of the heat pump and the stratified thermal storage have been revised in the pvcompare input parameters, adapting them in order to fit typical temperatures of the heating system. Also the pvcompare input parameters of the stratified thermal storage have been revised (#272)
- Improved "how to release" section in `contributing.md` with insights from last release (#275)
- Tests have been added which check if the examples of pvcompare run with exit code 0 (#284)
- Move docs requirements from `docs/docs_requirements.txt ` to `setup.py` - now installed e.g. by `pip install -e .[dev, docs]` (#276)
- Move coverage badge of `coveralls.io` from deprecated to valid section in `README.rst` (#289)
- Update code documentation in RTD: add missing functions and modules and delete outdated ones (#287)
- Update RTD's section `Electricity and heat demand modeling` and `Heat pump and thermal storage modelling` in `model_assumptions.rst` (#291)
- The parameters `inflow_direction` and `outflow_direction` of the gas plant have been changed from `Heat bus` to `Gas bus` in `energyProviders.csv` (#299)
- The parameter `energyVector` of the gas plant has been changed from `Heat` to `Gas` in `energyProviders.csv` (#299)
- All parameters in `fixcost.csv` have been set to zero except for the lifetime, which has been set to one for all in order to avoid ZeroDivisionError (#299)
- Corrected description of installation requirements in contributing.md (#306)
- Changed order of checks in github actions workflow - linting with black is last check now, to prevent failing due to black before pytest are run. (#298)
- Renamed "GRECO Results" section in RTD to "Selected results of the GRECO project" (#316)
- Minor changes and corrections in RTD (#316)

### Removed
- Remove lines that add gas bus in `test_raiseError_temperature_match_hp()` as this is not needed anymore (#314)

### Fixed
- fix PV costs parameters and PSI lifetime (#273)
- fix number of houses to 20 (8 flats per storey makes 40 flats per house with 5 storeys, makes 800 in total (and 480 for 3 storeys)) (#273)
- Test coverage is now automatically checked with github actions and [coveralls](https://coveralls.io/github/greco-project/pvcompare) (#283)
- In github actions workflow, add release branches to push events and correct name of `dev` branch (#305)
- In github actions workflow, set `EXECUTE_TEST_ON` to `"master"` for release branches (#305)

# Hot fixes
- Hot fix: install MVS with option `[report]` to install missing packages (#270)
- Hot fix: remove build for python 3.6 from `main.yml` github actions workflow (#270)
- Hot fix: Move `test_examples.py` to `examples` directory to make tests work in CI and add `__init__.py` to `examples` (#298)

## [0.0.2] - 2021-03-24

### Added
- Description of KPIs were added to the RTD that are used for evaluating the autonomy of the system (#261)
- "How to release" section in `contributing.md` (#259)

### Changed
- The evaluated period is no longer processed as integer but as float. Hence it is possible to simulate time periods that are for instance shorter than a day (#265)
- Divided check boxes in PR template into required checks and checks that do not apply to every PR, deleted the check box "Apply black" and added helpful notes (#266)

### Fixed
- Bug fix `fixcosts.csv` in test data (#263)
- Bug fix in setup.py (#263)
- Bug in calculation of the self-consumption was fixed (#261)

## [0.0.1] - 2021-03-22

Note that changes are tracked from next version.
