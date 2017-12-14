import logging

from django.utils.deprecation import MiddlewareMixin

from .models import Country

logger = logging.getLogger(__name__)


class AddRequestCountryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        country = Country.get_by_request(request)
        if country:
            request.country = country
        else:
            logger.warning('countries_plus:  Could not retrieve country, not adding to request.')
