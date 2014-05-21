from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Country
import logging


logger = logging.getLogger('django')


#  Look up the country of the request
#  Uses a META header defined in settings COUNTRIES_PLUS_COUNTRY_HEADER, this must be an iso code like 'us' for USA.
#  Also accepts a setting COUNTRIES_PLUS_DEFAULT_ISO for cases where the geoip fails.  If this setting is
#  not set, the country will not be added to the request.
#
#  Cloudflare is an example of a service that will add the country iso to the request header,
#  using the meta tag HTTP_CF_IPCOUNTRY
def get_country_by_request(request):
    country = None
    default_iso = None

    try:
        header_name = settings.COUNTRIES_PLUS_COUNTRY_HEADER
    except AttributeError:
        raise AttributeError("COUNTRIES_PLUS_COUNTRY_HEADER setting missing")

    if not settings.COUNTRIES_PLUS_COUNTRY_HEADER:
        raise AttributeError("COUNTRIES_PLUS_COUNTRY_HEADER can not be empty")

    try:
        default_iso = settings.COUNTRIES_PLUS_DEFAULT_ISO.upper()
    except AttributeError:
        pass

    geoip_request_iso = request.META.get(header_name, '')
    if geoip_request_iso:
        try:
            country = Country.objects.get(iso=geoip_request_iso.upper())
        except ObjectDoesNotExist:
            pass

    if not country:
        logger.warning("countries_plus:  Could not find a country matching '%s' from provided meta header '%s'." % (geoip_request_iso, header_name))
        if default_iso:
            logger.warning("countries_plus:  Setting country to provided default '%s'." % default_iso)
            try:
                country = Country.objects.get(iso=default_iso)
            except ObjectDoesNotExist:
                logger.warning("countries_plus:  Could not find a country matching COUNTRIES_PLUS_DEFAULT_ISO of '%s'." % default_iso)
    return country
