import pytest


@pytest.mark.django_db
class TestContextProcessor:
    def test_context_processor(self, countries_plus_settings, client, default_country):
        response = client.get("/")
        assert response.status_code == 200
        assert response.context.get("country") == default_country
