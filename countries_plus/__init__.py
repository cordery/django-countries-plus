from django.conf import settings
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
    header_name = settings.COUNTRIES_PLUS_COUNTRY_HEADER
    default_iso = settings.COUNTRIES_PLUS_DEFAULT_ISO

    if header_name:
        geoip_request_iso = request.META.get(header_name)
        try:
            return Country.objects.get(iso=geoip_request_iso.upper())
        except:
            logger.warning("Could not find a country matching '%s' from provided meta header '%s'." % (geoip_request_iso, header_name))
            if default_iso:
                logger.warning("Setting country to provided default '%s'." % default_iso)
                try:
                    return Country.objects.get(iso=default_iso.upper())
                except:
                    logger.warning("Could not find a country matching COUNTRIES_PLUS_DEFAULT_ISO of '%s'. Not adding country to request." % default_iso)
    return None
