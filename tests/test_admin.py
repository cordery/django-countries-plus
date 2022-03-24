import pytest
from django.contrib import admin

from countries_plus.admin import CountryAdmin  # noqa
from countries_plus.models import Country
from tests.models import Company
from tests.admin import CompanyAdmin  # noqa


@pytest.mark.django_db
class TestAdmin:
    def test_countries_admin(self, countries_plus_settings, rf):
        assert admin.site.is_registered(Company)
        assert admin.site.is_registered(Country)
        assert not admin.site.check(
            None
        ), "If CountryAdmin is missing search_fields then an E040 error will be present"
