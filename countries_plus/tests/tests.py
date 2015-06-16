from copy import deepcopy
from decimal import Decimal

from django.core.exceptions import ValidationError

from django.core.management import call_command
from django.test import TestCase
from django.test import Client
from django.core.handlers.base import BaseHandler

from django.test.client import RequestFactory

from countries_plus.models import Country
from countries_plus.middleware import AddRequestCountryMiddleware
from countries_plus.utils import update_geonames_data, parse_geonames_data, GeonamesParseError


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


class TestUpdateGeonamesData(TestCase):
    def setUp(self):
        Country.objects.all().delete()

    def tearDown(self):
        Country.objects.all().delete()

    def test_update_geonames_data(self):
        # If the geonames.org dataset adds/removes a country or changes its format
        # this test will fail, which is intended.
        num_updated, num_created = update_geonames_data()
        self.assertEqual(num_updated, 0)
        self.assertEqual(num_created, 252)

        num_updated, num_created = update_geonames_data()
        self.assertEqual(num_updated, 252)
        self.assertEqual(num_created, 0)

        self.assertEqual(Country.objects.count(), 252)


class TestParseGeonamesData(TestCase):
    valid_data = [
        u"#ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode	CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode".encode(),
        u"AD	AND	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
    ]
    invalid_data_no_header = [
        u"AD	AND	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
    ]
    invalid_data_bad_header = [
        u"#ISO  Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode	CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode".encode(),
        u"AD	AND	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
    ]
    invalid_data_invalid_field_length = [
        u"#ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode	CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode".encode(),
        u"AD	INVALID_ISO3	020	AN	Andorra	Andorra la Vella	468	84000	EU	.ad	EUR	Euro	376	AD###	^(?:AD)*(\d{3})$	ca	3041565	ES,FR	".encode()
    ]

    def setUp(self):
        Country.objects.all().delete()

    def tearDown(self):
        Country.objects.all().delete()

    def test_valid_data(self):
        parse_geonames_data(iter(self.valid_data))
        self.assertEqual(Country.objects.count(), 1)

    def test_invalid_data_no_header(self):
        with self.assertRaises(GeonamesParseError):
            parse_geonames_data(iter(self.invalid_data_no_header))

    def test_invalid_data_bad_header(self):
        with self.assertRaises(GeonamesParseError):
            parse_geonames_data(iter(self.invalid_data_bad_header))

    def test_invalid_data_field_length(self):
        with self.assertRaises(GeonamesParseError):
            parse_geonames_data(iter(self.invalid_data_invalid_field_length))

    def test_invalid_data_field_length_update(self):
        parse_geonames_data(iter(self.valid_data))
        with self.assertRaises(GeonamesParseError):
            parse_geonames_data(iter(self.invalid_data_invalid_field_length))


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
