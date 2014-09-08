=====================
django-countries-plus
=====================

django-countries-plus provides a model and fixture containing all top level country data from Geonames.org (http://download.geonames.org/export/dump/countryInfo.txt)

This package also provides a convenience middleware that will look up a country in the database using a defined meta header, ex:  the Cloudflare provided geoip META header HTTP_CF_IPCOUNTRY.  This country object will be
attached to the request object at request.country

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
* phone (Phone)
* postal_code_format (Postal Code Format)
* postal_code_regex (Postal Code Regex)
* languages (Languages)
* geonameid (geonameid)
* neighbors (neighbours)
* equivalent_fips_code (EquivalentFipsCode)


------------
Installation
------------

::

    pip install django-countries-plus


------------
Usage
------------

1. Add ``countries_plus`` to your INSTALLED_APPS

2. Sync your fixtures::

        python manage.py syncdb

3. In your code use::

        from countries_plus.models import Country
        usa = Country.objects.get(iso3='USA')


Enabling the optional middleware:
---------------------------------
1.  Follow steps 1 & 2 above.

2.  Add ``countries_plus.middleware.AddRequestCountryMiddleware`` to your middleware.

3.  add the following two settings to your settings.py:

    ``COUNTRIES_PLUS_COUNTRY_HEADER``   -   A string defining the name of the meta header that provides the country code.  Ex: 'HTTP_CF_COUNTRY' (from https://support.cloudflare.com/hc/en-us/articles/200168236-What-does-CloudFlare-IP-Geolocation-do-)

    ``COUNTRIES_PLUS_DEFAULT_ISO``  -   A string containing an iso code for the country you want to use as a fallback in the case of a missing or malformed geoip header.  Ex:  'US' or 'DE' or 'BR'

Compatibility
-------------
Compatible with Django 1.2+
