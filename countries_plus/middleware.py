import logging
from . import get_country_by_request

logger = logging.getLogger('django')


class AddRequestCountryMiddleware(object):
    def process_request(self, request):
        country = get_country_by_request(request)
        if country:
            request.country = country
