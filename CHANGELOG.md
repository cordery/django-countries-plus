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
- The Country model has had all fields with undefined lengths (ex: name) expanded to max_length=255.  Defined length fields (ex: Iso, Iso3) are unchanged.
- Two countries (Dominican Republic and Puerto Rico) have two phone number prefixes instead of 1.  These prefixes are now comma separated.
- The Country model will now validate on save and reject values of the wrong length.  The test suite has been expanded to test this.

### Fixed
- Fixed update_countries_plus command for python 3

## [1.0.0] - 2015-06-11
### Added
- Added feature to update data from geonames.org.  
- Test coverage has been substantially improved.

### Changed
- The data migration has been removed in favour of the new management command and manually loading the fixture.
- The fixture is no longer named initial_data and so must be loaded manually, if desired.
- In order to provide better compatibility with the way Django loads apps the Country model is no longer importable directly from countries_plus.
- The get_country_by_request utility function has been moved into the Country model, and is available as Country.get_by_request(request)

### Fixed 
- General code cleanup & improved test coverage.

### Note
- If you have been running an earlier version you should run python manage.py update_countries_plus to update your data tables as they may contain incorrect data.

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