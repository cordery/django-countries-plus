from copy import deepcopy
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from countries_plus.models import Country


class TestCountryModel(TestCase):
    valid_values = {
        'postal_code_regex': 'test', 'geonameid': 1149361,
        'languages': 'fa-AF,ps,uz-AF,tk', 'equivalent_fips_code': '2134',
        'population': 29121286, 'name': 'Afghanistan', 'area': Decimal('647500.0'),
        'postal_code_format': None, 'capital': 'Kabul', 'fips': 'AF', 'iso3': 'AFG',
        'currency_symbol': '?', 'currency_name': 'Afghani',
        'neighbours': 'TM,CN,IR,TJ,PK,UZ', 'iso_numeric': 4, 'continent': 'AS',
        'tld': '.af', 'iso': 'AF', 'phone': '9342342 and 4293432434', 'currency_code': 'AFN'
    }

    def setUp(self):
        Country.objects.all().delete()

    def tearDown(self):
        Country.objects.all().delete()

    def test_country_validation_valid(self):
        self.assertIsInstance(Country.objects.create(**self.valid_values), Country)

    def test_country_validation_invalid(self):
        invalid_values = deepcopy(self.valid_values)
        invalid_values['iso'] = "This is too long for the iso field"
        with self.assertRaises(ValidationError):
            Country.objects.create(**invalid_values)
