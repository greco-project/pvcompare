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

### Changed
- The inlet temperatures of the heat pump and the stratified thermal storage have been revised in the pvcompare input parameters, adapting them in order to fit typical temperatures of the heating system. Also the pvcompare input parameters of the stratified thermal storage have been revised (#272)
- Improved "how to release" section in `contributing.md` with insights from last release (#275)
- Tests have been added which check if the examples of pvcompare run with exit code 0 (#284)
- Move docs requirements from `docs/docs_requirements.txt ` to `setup.py` - now installed e.g. by `pip install -e .[dev, docs]` (#276)
- Update code documentation in RTD: add missing functions and modules and delete outdated ones (#287)

### Removed
-

### Fixed
- fix PV costs parameters and PSI lifetime (#273)
- fix number of houses to 20 (8 flats per storey makes 40 flats per house with 5 storeys, makes 800 in total (and 480 for 3 storeys)) (#273)

# Hot fixes
- Hot fix: install MVS with option `[report]` to install missing packages (#270)
- Hot fix: remove build for python 3.6 from `main.yml` github actions workflow (#270)

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
