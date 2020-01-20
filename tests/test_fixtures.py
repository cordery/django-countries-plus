from django.test import TestCase

from countries_plus.models import Country


class TestFixtures(TestCase):
    fixtures = ['countries_data']

    def test_count(self):
        country_count = Country.objects.all().count()
        assert country_count == 252

    def test_get_by_iso(self):
        panama = Country.objects.get(iso='PA')
        assert 'Panama' == panama.name
        assert 'PAN' == panama.iso3
