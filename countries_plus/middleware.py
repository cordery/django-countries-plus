import logging
from countries_plus.models import Country

logger = logging.getLogger(__name__)


class AddRequestCountryMiddleware(object):
    def process_request(self, request):
        country = Country.get_by_request(request)
        if country:
            request.country = country
        else:
            logger.warning('countries_plus:  Could not retrieve country, not adding to request.')
