import pytest

from countries_plus.models import Country


@pytest.fixture
def default_country(db):
    return Country.objects.create(
        name='DefaultCountry',
        iso='DC',
        iso3='DCO',
        iso_numeric='1',
    )


@pytest.fixture
def other_country(db):
    return Country.objects.create(
        name='Other Country',
        iso='OC',
        iso3='OCO',
        iso_numeric='2',
    )


@pytest.fixture
def countries_plus_settings(settings, default_country, other_country):
    settings.MIDDLEWARE += ('countries_plus.middleware.AddRequestCountryMiddleware',)
    settings.COUNTRIES_PLUS_COUNTRY_HEADER = 'GEOIP_HEADER'
    settings.COUNTRIES_PLUS_DEFAULT_ISO = default_country.iso
    settings.TEMPLATES[0]['OPTIONS']['context_processors'] += [
        'countries_plus.context_processors.add_request_country'
    ]
    return settings
