from django.test import TestCase
from countries_plus import Country

__author__ = 'luiscberrocal'


class TestCountry(TestCase):

    def test_create(self):
        country_count = Country.objects.all().count()
        self.assertEqual(country_count,252)

    def test_get_by_iso(self):
        panama = Country.objects.get(iso='PA')
        self.assertEqual('Panama', panama.name)
        self.assertEqual('PAN', panama.iso3)
