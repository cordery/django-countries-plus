from django.db import models
from django.utils.translation import ugettext as _

class Country(models.Model):
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['continent', 'name']

    iso = models.CharField(max_length=2, primary_key=True)
    iso3 = models.CharField(max_length=3, unique=True)
    iso_numeric = models.IntegerField(max_length=3, unique=True)
    fips = models.CharField(max_length=3, blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    capital = models.CharField(max_length=100, blank=True, null=True)
    area = models.IntegerField(max_length=3, blank=True, null=True)
    population = models.IntegerField(max_length=3, blank=True, null=True)
    continent = models.CharField(max_length=2, blank=True, null=True)
    tld = models.CharField(max_length=10, blank=True, null=True)
    currency_code = models.CharField(max_length=3, blank=True, null=True)
    currency_symbol = models.CharField(max_length=5, blank=True, null=True)
    currency_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    postal_code_format = models.CharField(max_length=100, blank=True, null=True)
    postal_code_regex = models.CharField(max_length=100, blank=True, null=True)
    languages = models.CharField(max_length=100, blank=True, null=True)
    geonameid = models.IntegerField(max_length=20, blank=True, null=True)
    neighbours = models.CharField(max_length=100, blank=True, null=True)
    equivalent_fips_code = models.CharField(max_length=3, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.continent, self.name)
