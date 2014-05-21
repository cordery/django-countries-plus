import logging

from . import get_country_by_request


logger = logging.getLogger('django')


class AddRequestCountryMiddleware(object):
    def process_request(self, request):
        country = get_country_by_request(request)
        if country:
            request.country = country
        else:
            logger.warning('countries_plus:  Could not retrieve country, not adding to request.')
