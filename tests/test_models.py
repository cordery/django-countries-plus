from copy import deepcopy
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from countries_plus.models import Country


@pytest.mark.django_db
class TestCountryModel:
    valid_values = {
        'postal_code_regex': 'test',
        'geonameid': 1149361,
        'languages': 'fa-AF,ps,uz-AF,tk',
        'equivalent_fips_code': '2134',
        'population': 29121286,
        'name': 'Afghanistan',
        'area': Decimal('647500.0'),
        'postal_code_format': None,
        'capital': 'Kabul',
        'fips': 'AF',
        'iso3': 'AFG',
        'currency_symbol': '?',
        'currency_name': 'Afghani',
        'neighbours': 'TM,CN,IR,TJ,PK,UZ',
        'iso_numeric': 4,
        'continent': 'AS',
        'tld': '.af',
        'iso': 'AF',
        'phone': '9342342 and 4293432434',
        'currency_code': 'AFN',
    }

    def test_country_validation_valid(self):
        assert isinstance(Country.objects.create(**self.valid_values), Country)

    def test_country_validation_invalid(self):
        invalid_values = deepcopy(self.valid_values)
        invalid_values['iso'] = "This is too long for the iso field"
        with pytest.raises(ValidationError):
            Country.objects.create(**invalid_values)


@pytest.mark.django_db
class TestCountryGetByRequest:
    @pytest.fixture
    def request_without_geoip(self, rf):
        request = rf.get('/')
        request.META = {}
        return request

    @pytest.fixture
    def request_with_geoip(self, rf, other_country):
        request = rf.get('/')
        request.META = {
            'GEOIP_HEADER': other_country.iso,
        }
        return request

    def test_blank_settings(self, settings, request_without_geoip):
        # Test with missing/badly formed settings
        settings.COUNTRIES_PLUS_COUNTRY_HEADER = ''
        settings.COUNTRIES_PLUS_DEFAULT_ISO = ''
        with pytest.raises(AttributeError):
            Country.get_by_request(request_without_geoip)

    def test_blank_default(self, settings, request_without_geoip):
        # Test without a default
        settings.COUNTRIES_PLUS_COUNTRY_HEADER = 'GEOIP_HEADER'
        settings.COUNTRIES_PLUS_DEFAULT_ISO = ''
        assert Country.get_by_request(request_without_geoip) is None

    def test_default(
        self,
        countries_plus_settings,
        default_country,
        other_country,
        request_without_geoip,
        request_with_geoip,
    ):
        # Test with a default
        assert Country.get_by_request(request_without_geoip) == default_country
        assert Country.get_by_request(request_with_geoip) == other_country
