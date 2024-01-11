import pytest


@pytest.mark.django_db
class TestAddRequestCountryMiddleware:
    def test_middleware_lookup(self, countries_plus_settings, client, other_country):
        header = countries_plus_settings.COUNTRIES_PLUS_COUNTRY_HEADER
        response = client.get("/", **{header: other_country.iso})
        assert response.wsgi_request.country == other_country

    @pytest.mark.parametrize("geoip_header_value", (None, "", "JUNK"))
    def test_middleware_default_blank(
        self, countries_plus_settings, client, default_country, geoip_header_value
    ):
        header = countries_plus_settings.COUNTRIES_PLUS_COUNTRY_HEADER
        response = client.get("/", **{header: geoip_header_value})
        assert response.wsgi_request.country == default_country
