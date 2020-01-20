import pytest


@pytest.mark.django_db
class TestContextProcessor:

    def test_context_processor(self, settings, client, default_country):
        settings.MIDDLEWARE += ('countries_plus.middleware.AddRequestCountryMiddleware',)
        settings.COUNTRIES_PLUS_COUNTRY_HEADER = 'GEOIP_HEADER'
        settings.COUNTRIES_PLUS_DEFAULT_ISO = 'US'
        settings.TEMPLATES[0]['OPTIONS'] = {'context_processors': [
            'countries_plus.context_processors.add_request_country'
        ]}

        response = client.get('/')
        assert response.context.get('country') == default_country
