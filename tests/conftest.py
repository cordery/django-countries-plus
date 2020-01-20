import pytest

from countries_plus.models import Country


@pytest.fixture
def default_country(db):
    return Country.objects.create(
        name='DefaultCountry',
        iso='US',
        iso3='USA',
        iso_numeric='1',
    )


@pytest.fixture
def other_country(db):
    return Country.objects.create(
        name='TestCountry',
        iso='TC',
        iso3='TCO',
        iso_numeric='2',
    )

