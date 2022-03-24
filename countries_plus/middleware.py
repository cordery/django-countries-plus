import logging

from countries_plus.models import Country

logger = logging.getLogger(__name__)


class AddRequestCountryMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        country = Country.get_by_request(request)
        if country:
            request.country = country
        else:
            logger.warning(
                'countries_plus:  Could not retrieve country, not adding to request.'
            )
        return self.get_response(request)
