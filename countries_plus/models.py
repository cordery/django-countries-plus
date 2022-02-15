import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class Country(models.Model):
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['name']

    iso = models.CharField(max_length=2, primary_key=True)
    iso3 = models.CharField(max_length=3, unique=True)
    iso_numeric = models.IntegerField(unique=True)
    fips = models.CharField(max_length=3, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    capital = models.CharField(max_length=255, blank=True, null=True)
    area = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    continent = models.CharField(max_length=2, blank=True, null=True)
    tld = models.CharField(max_length=255, blank=True, null=True)
    currency_code = models.CharField(max_length=3, blank=True, null=True)
    currency_symbol = models.CharField(max_length=255, blank=True, null=True)
    currency_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    postal_code_format = models.CharField(max_length=255, blank=True, null=True)
    postal_code_regex = models.CharField(max_length=255, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    geonameid = models.IntegerField(blank=True, null=True)
    neighbours = models.CharField(max_length=255, blank=True, null=True)
    equivalent_fips_code = models.CharField(max_length=4, blank=True, null=True)

    @staticmethod
    def get_by_request(request):
        from django.conf import settings

        country = None
        default_iso = None

        try:
            header_name = settings.COUNTRIES_PLUS_COUNTRY_HEADER
        except AttributeError:
            raise AttributeError(
                "COUNTRIES_PLUS_COUNTRY_HEADER setting missing.  This setting must be present "
                "when using the countries_plus middleware.")

        if not settings.COUNTRIES_PLUS_COUNTRY_HEADER:
            raise AttributeError(
                "COUNTRIES_PLUS_COUNTRY_HEADER can not be empty.   This setting must be present "
                "when using the countries_plus middleware.")

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
            logger.warning(
                "countries_plus:  Could not find a country matching '%s' from provided meta "
                "header '%s'." % (
                    geoip_request_iso, header_name))
            if default_iso:
                logger.warning(
                    "countries_plus:  Setting country to provided default '%s'." % default_iso)
                try:
                    country = Country.objects.get(iso=default_iso)
                except ObjectDoesNotExist:
                    logger.warning(
                        "countries_plus:  Could not find a country matching "
                        "COUNTRIES_PLUS_DEFAULT_ISO of '%s'." % default_iso)
        return country

    def __str__(self):
        return u'%s' % (self.name,)

    def save(self, **kwargs):
        self.full_clean()
        super(Country, self).save(**kwargs)
