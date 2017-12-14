# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Improved documentation

### Changed
- Added tests for Django 2.0
- Dropped tested support for Django versions < 1.11

## [1.1.0] - 2016-03-14
### Fixed
- Fixed Geonames.org file format error

## [1.0.1] - 2015-06-16
### Added
- Improved test coverage.

### Changed
- Loosened model restrictions

### Fixed
- Fixed update_countries_plus command for python 3

## [1.0.0] - 2015-06-11
### Added
- Added feature to update data from geonames.org.  

### Fixed 
- General code cleanup & improved test coverage.

## [0.3.3] - 2015-01-27
### Changed
- Now uses Django 1.7 data migration pattern

## [0.3.2] - 2015-01-10
### Fixed
- Corrected version number on setup.py

## [0.3.1] - 2015-01-09
### Added
- Now compatible with Python 3 thanks to luiscberrocal

## [0.3.0] - 2014-09-08
### Added
- Now compatible with Django 1.7 thanks to mrben

## [0.2.0] - 2014-02-13
### Added
- Added middleware that adds the request country to the request object.

## [0.1.5] - 2013-06-14
### Fixed
- Corrected model max_length attributes to properly match data.

## [0.1.0] - 2013-05-22
### Added
- Initial release.
