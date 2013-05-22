===========
django-countries-plus
===========

django-countries-plus provides a model and fixture containing all top level country data from Geonames.org (http://download.geonames.org/export/dump/countryInfo.txt)

The model provides the following fields (original geonames.org column name in parentheses) are:

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

Installation & Use
========= 

Install:
	pip install django-countries-plus

Usage:

	1. Add countriesplus to your INSTALLED_APPS
	2. Run python manage.py syncdb to install the countriesplus fixtures
	3. In your code use:
		from countriesplus.models import Country
		usa = Country.objects.get(iso3='USA')
