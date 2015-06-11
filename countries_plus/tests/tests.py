import gzip
import os

from django.core import serializers

from django.test import SimpleTestCase, TestCase

from django.test import Client

from django.core.handlers.base import BaseHandler

from django.test.client import RequestFactory

from countries_plus.models import Country
from countries_plus.middleware import AddRequestCountryMiddleware
from countries_plus.utils import update_geonames_data


class RequestMock(RequestFactory):
    def request(self, **request):
        """Construct a generic request object."""
        request = RequestFactory.request(self, **request)
        handler = BaseHandler()
        handler.load_middleware()
        for middleware_method in handler._request_middleware:
            if middleware_method(request):
                raise Exception("Couldn't create request mock object - "
                                "request middleware returned a response")
        return request


class TestCountryByRequest(SimpleTestCase):
    def setUp(self):
        self.request_without_geoip = RequestMock()
        self.request_without_geoip.META = {}

        self.request_with_geoip = RequestMock()
        self.request_with_geoip.META = {
            'GEOIP_HEADER': 'TC',
        }

        self.middleware = AddRequestCountryMiddleware()

        self.default_country = Country.objects.create(
            name='DefaultCountry',
            iso='US',
            iso3='USA',
            iso_numeric='1',
        )
        self.test_country = Country.objects.create(
            name='TestCountry',
            iso='TC',
            iso3='TCO',
            iso_numeric='2',
        )

    def tearDown(self):
        Country.objects.all().delete()

    def test_country_by_request(self):
        # Test with missing/badly formed settings
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='', COUNTRIES_PLUS_DEFAULT_ISO=''):
            with self.assertRaises(AttributeError):
                Country.get_by_request(self.request_without_geoip)

        # Test without a default
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER', COUNTRIES_PLUS_DEFAULT_ISO=''):
            self.assertIsNone(Country.get_by_request(self.request_without_geoip))

        # Test with a default
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER', COUNTRIES_PLUS_DEFAULT_ISO='US'):
            self.assertEqual(Country.get_by_request(self.request_without_geoip), self.default_country)
            self.assertEqual(Country.get_by_request(self.request_with_geoip), self.test_country)

    def test_middleware(self):
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER', COUNTRIES_PLUS_DEFAULT_ISO='US'):
            # This should always return none, and it adds country to the request
            self.assertEqual(self.middleware.process_request(self.request_with_geoip), None)
            self.assertIsInstance(self.request_with_geoip.country, Country)


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
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER', COUNTRIES_PLUS_DEFAULT_ISO='US'):
            response = self.client.get('/')
            self.assertIsInstance(response.context.get('country'), Country)


class TestFixtures(TestCase):
    def setUp(self):
        fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures'))
        fixture_filename = 'initial_data.json.gz'
        fixture_file = os.path.join(fixture_dir, fixture_filename)
        with gzip.open(fixture_file, 'rb') as fixture:
            objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
            for obj in objects:
                obj.save()

    def test_count(self):
        country_count = Country.objects.all().count()
        self.assertEqual(country_count, 252)

    def test_get_by_iso(self):
        panama = Country.objects.get(iso='PA')
        self.assertEqual('Panama', panama.name)
        self.assertEqual('PAN', panama.iso3)


class TestUpdateGeonamesData(TestCase):
    def setUp(self):
        Country.objects.all().delete()

    def tearDown(self):
        Country.objects.all().delete()

    def test_first_update_geonames_data(self):
        # If the geonames.org dataset adds/removes a country or changes its format this test will fail, which is intended.
        num_updated, num_created = update_geonames_data()
        self.assertEqual(num_updated, 0)
        self.assertEqual(num_created, 252)

        num_updated, num_created = update_geonames_data()
        self.assertEqual(num_updated, 252)
        self.assertEqual(num_created, 0)
