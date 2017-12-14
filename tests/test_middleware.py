from django.core.handlers.base import BaseHandler
from django.test import RequestFactory, TestCase

from countries_plus.middleware import AddRequestCountryMiddleware
from countries_plus.models import Country


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


class TestCountryByRequest(TestCase):
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
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER',
                           COUNTRIES_PLUS_DEFAULT_ISO=''):
            self.assertIsNone(Country.get_by_request(self.request_without_geoip))

        # Test with a default
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER',
                           COUNTRIES_PLUS_DEFAULT_ISO='US'):
            self.assertEqual(Country.get_by_request(self.request_without_geoip),
                             self.default_country)
            self.assertEqual(Country.get_by_request(self.request_with_geoip), self.test_country)

    def test_middleware(self):
        with self.settings(COUNTRIES_PLUS_COUNTRY_HEADER='GEOIP_HEADER',
                           COUNTRIES_PLUS_DEFAULT_ISO='US'):
            # This should always return none, and it adds country to the request
            self.assertEqual(self.middleware.process_request(self.request_with_geoip), None)
            self.assertIsInstance(self.request_with_geoip.country, Country)
