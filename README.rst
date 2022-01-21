=============================
Django Countries Plus
=============================

.. image:: https://badge.fury.io/py/django-countries-plus.svg
    :target: https://badge.fury.io/py/django-countries-plus

.. image:: https://travis-ci.org/cordery/django-countries-plus.svg
    :target: https://travis-ci.org/cordery/django-countries-plus

.. image:: https://codecov.io/github/cordery/django-countries-plus/coverage.svg
    :target: https://codecov.io/github/cordery/django-countries-plus

.. image:: https://requires.io/github/cordery/django-countries-plus/requirements.svg?branch=master
    :target: https://requires.io/github/cordery/django-countries-plus/requirements/?branch=master

.. image:: https://www.codacy.com/project/badge/c74f1b1041f44940b58e0e1587b10453?style=flat-square
    :target: https://www.codacy.com/app/cordery/django-countries-plus

django-countries-plus provides a model and fixture containing all top level country data from Geonames.org (http://download.geonames.org/export/dump/countryInfo.txt)

This package also provides a convenience middleware that will look up a country in the database using a defined meta header, ex:  the Cloudflare provided geoip META header HTTP_CF_IPCOUNTRY.  This country object will be
attached to the request object at request.country.



Country Model
-------------

The model provides the following fields (original geonames.org column name in parentheses).

* iso (ISO)
* iso3 (ISO3)
* iso_numeric (ISO-Numeric)
* fips (fips)
* name (Country)
* capital
* area (Area(in sq km))
* population (population)
* continent (continent)
* tld (tld)
* currency_code (CurrencyCode)
* currency_name (CurrencyName)
* currency_symbol (Not part of the original table)
* phone (Phone)
* postal_code_format (Postal Code Format)
* postal_code_regex (Postal Code Regex)
* languages (Languages)
* geonameid (geonameid)
* neighbors (neighbours)
* equivalent_fips_code (EquivalentFipsCode)



Installation
------------

Step 1: Install From PyPi

``pip install django-countries-plus``

Step 2: Add ``countries_plus`` to your settings INSTALLED_APPS

Step 3: Run ``python manage.py migrate``

Step 4: Load the Countries Data
    a. Load the countries data into your database with the update_countries_plus management command.
        ``python manage.py update_countries_plus``
    b. (alternative) Load the provided fixture from the fixtures directory.
        ``python manage.py loaddata PATH_TO_COUNTRIES_PLUS/countries_plus/countries_data.json.gz``



Usage
-----

**Retrieve a Country**::

    from countries_plus.models import Country
    usa = Country.objects.get(iso3='USA')

**Update the countries data with the latest geonames.org data**::

    python manage.py update_countries_plus

This management command will download the latest geonames.org countries data and convert it into Country objects.  Existing Country objects will be updated if necessary.  No Country objects will be deleted, even if that country has ceased to exist.


Add the Request Country to each Request
---------------------------------------

1.  Add ``countries_plus.middleware.AddRequestCountryMiddleware`` to your MIDDLEWARE setting.

2.  add the following two settings to your settings.py:

    ``COUNTRIES_PLUS_COUNTRY_HEADER``   -   A string defining the name of the meta header that provides the country code.  Ex: 'HTTP_CF_COUNTRY' (from https://support.cloudflare.com/hc/en-us/articles/200168236-What-does-CloudFlare-IP-Geolocation-do-)

    ``COUNTRIES_PLUS_DEFAULT_ISO``  -   A string containing an iso code for the country you want to use as a fallback in the case of a missing or malformed geoip header.  Ex:  'US' or 'DE' or 'BR'

    Example::

        COUNTRIES_PLUS_COUNTRY_HEADER = 'HTTP_CF_COUNTRY'
        COUNTRIES_PLUS_DEFAULT_ISO = 'US'


Add the Request Country to the Request Context
----------------------------------------------
1. Enable the optional middleware as described above

2. Add ``countries_plus.context_processors.add_request_country`` to your 'context_processors' option in the OPTIONS of a DjangoTemplates backend instead (Django 1.8)


---------------------------------------
Requirements
---------------------------------------
Python: 3.7+
Django:  Tested against the LTS or latest versions of 2.2, 3, and 4.


Integrating with django-languages-plus
--------------------------------------
If you also have django-languages-plus(https://pypi.python.org/pypi/django-languages-plus) installed then you can run the following command once to associate the two datasets and generate a list of culture codes (pt_BR for example)::

        from languages_plus.utils import associate_countries_and_languages
        associate_countries_and_languages()


Notes on 1.0.1
--------------
* Two countries (Dominican Republic and Puerto Rico) have two phone number prefixes instead of 1.  These prefixes are now comma separated.
* The Country model has had all fields with undefined lengths (ex: name) expanded to max_length=255.  Defined length fields (ex: Iso, Iso3) are unchanged.
* The Country model will no validate on save and reject values of the wrong length.  The test suite has been expanded to test this.

Notes on 1.0.0
--------------
* The data migration has been removed in favour of the new management command and manually loading the fixture.
* The fixture is no longer named initial_data and so must be loaded manually, if desired.
* In order to provide better compatibility with the way Django loads apps the Country model is no longer importable directly from countries_plus.
* The get_country_by_request utility function has been moved into the Country model, and is available as Country.get_by_request(request)
* Test coverage has been substantially improved.
* If you have been running an earlier version you should run python manage.py update_countries_plus to update your data tables as they may contain incorrect data.



Running Tests
-------------

Does the code actually work?

::

    $ poetry install
    $ poetry run pytest

Or for the full tox suite:

::

    $ poetry install
    $ pip install tox
    $ tox

