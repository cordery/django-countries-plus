import pytest
from django.core.management import call_command

from countries_plus.models import Country


@pytest.mark.django_db
class TestUpdateCountriesPlusCommand:
    def test_update_countries_plus_command(self):
        # If the geonames.org dataset adds/removes a country or changes its format this
        # test will fail, which is intended.

        call_command("update_countries_plus")
        assert Country.objects.count() == 252
