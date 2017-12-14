from django.core.management import call_command
from django.test import TestCase

from countries_plus.models import Country


class TestUpdateCountriesPlusCommand(TestCase):
    def setUp(self):
        Country.objects.all().delete()

    def tearDown(self):
        Country.objects.all().delete()

    def test_update_countries_plus_command(self):
        # If the geonames.org dataset adds/removes a country or changes its format this
        # test will fail, which is intended.

        call_command('update_countries_plus')
        self.assertEqual(Country.objects.count(), 252)
