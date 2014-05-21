from django.conf import settings
from django.test import SimpleTestCase, TestCase
from django.test import Client
from django.core.handlers.base import BaseHandler
from django.test.client import RequestFactory

from model_mommy import mommy
from rentalsite.countries_plus import get_country_by_request, Country
from rentalsite.countries_plus.middleware import AddRequestCountryMiddleware


class RequestMock(RequestFactory):
    def request(self, **request):
        "Construct a generic request object."
        request = RequestFactory.request(self, **request)
        handler = BaseHandler()
        handler.load_middleware()
        for middleware_method in handler._request_middleware:
            if middleware_method(request):
                raise Exception("Couldn't create request mock object - "
                                "request middleware returned a response")
        return request


class CountryByRequestTest(SimpleTestCase):
    def setUp(self):
        self.request_without_geoip = RequestMock()
        self.request_without_geoip.META ={}

        self.request_with_geoip = RequestMock()
        self.request_with_geoip.META = {
            'GEOIP_HEADER': 'TC',
        }

        self.middleware = AddRequestCountryMiddleware()

        self.default_country = mommy.make(
            'Country',
            name='DefaultCountry',
            iso='US'
        )
        self.test_country = mommy.make(
            'Country',
            name='TestCountry',
            iso='TC'
        )

    def test_country_by_request(self):
        # Test with missing/badly formed settings
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='', COUNTRIES_PLUS_DEFAULT_ISO=''):
            with self.assertRaises(AttributeError):
                get_country_by_request(self.request_without_geoip)

        # Test without a default
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER', COUNTRIES_PLUS_DEFAULT_ISO=''):
            self.assertIsNone(get_country_by_request(self.request_without_geoip))

        # Test with a default
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER', COUNTRIES_PLUS_DEFAULT_ISO='US'):
            self.assertEqual(get_country_by_request(self.request_without_geoip), self.default_country)
            self.assertEqual(get_country_by_request(self.request_with_geoip), self.test_country)

    def test_middleware(self):
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER', COUNTRIES_PLUS_DEFAULT_ISO='US'):
            #This should always return none, and it adds country to the request
            self.assertEqual(self.middleware.process_request(self.request_with_geoip), None)
            self.assertIsInstance(self.request_with_geoip.country, Country)


class ContextProcessorTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.default_country = mommy.make(
            'Country',
            name='DefaultCountry',
            iso=settings.COUNTRIES_PLUS_DEFAULT_ISO
        )
        self.client = Client()

    def test_context_processor(self):
        # Test
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER', COUNTRIES_PLUS_DEFAULT_ISO='US'):
            response = self.client.get('/')

            self.assertIsInstance(response.context['country'], Country)