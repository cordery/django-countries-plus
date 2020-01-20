import pytest


@pytest.mark.django_db
class TestAddRequestCountryMiddleware:

    def test_middleware(self, settings, client, default_country):
        # This should always return none, and it adds country to the request
        settings.MIDDLEWARE += ('countries_plus.middleware.AddRequestCountryMiddleware',)
        settings.COUNTRIES_PLUS_COUNTRY_HEADER = 'GEOIP_HEADER'
        settings.COUNTRIES_PLUS_DEFAULT_ISO = 'US'
        response = client.get('/', META={'GEOIP_HEADER': 'TC'})
        assert response.wsgi_request.country == default_country
