from django.test import Client
from django.test import TestCase

from countries_plus.models import Country


class TestContextProcessor(TestCase):
    def setUp(self):
        self.default_country = Country.objects.create(
            name='DefaultCountry',
            iso='US',
            iso3='USA',
            iso_numeric='1',
        )
        self.client = Client()

    def test_context_processor(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context.get('country'), Country)


class TestFixtures(TestCase):
    fixtures = ['countries_data']

    def test_count(self):
        country_count = Country.objects.all().count()
        self.assertEqual(country_count, 252)

    def test_get_by_iso(self):
        panama = Country.objects.get(iso='PA')
        self.assertEqual('Panama', panama.name)
        self.assertEqual('PAN', panama.iso3)
