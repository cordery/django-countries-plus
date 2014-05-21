from django.db import models
from django.utils.translation import ugettext as _


class Country(models.Model):

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['name']

    iso = models.CharField(max_length=2, primary_key=True)
    iso3 = models.CharField(max_length=3, unique=True)
    iso_numeric = models.IntegerField(max_length=3, unique=True)
    fips = models.CharField(max_length=3, blank=True, null=True)
    name = models.CharField(max_length=50, unique=True)
    capital = models.CharField(max_length=30, blank=True, null=True)
    area = models.IntegerField(max_length=8, blank=True, null=True)
    population = models.IntegerField(max_length=10, blank=True, null=True)
    continent = models.CharField(max_length=2, blank=True, null=True)
    tld = models.CharField(max_length=5, blank=True, null=True)
    currency_code = models.CharField(max_length=3, blank=True, null=True)
    currency_symbol = models.CharField(max_length=7, blank=True, null=True)
    currency_name = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=5, blank=True, null=True)
    postal_code_format = models.CharField(max_length=60, blank=True, null=True)
    postal_code_regex = models.CharField(max_length=175, blank=True, null=True)
    languages = models.CharField(max_length=100, blank=True, null=True)
    geonameid = models.IntegerField(max_length=7, blank=True, null=True)
    neighbours = models.CharField(max_length=50, blank=True, null=True)
    equivalent_fips_code = models.CharField(max_length=4, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.name,)

"""


Fixture analysis showing max length encountered per field

{
 'pk': 2, #iso
 u'area': 8,
 u'capital': 20,
 u'continent': 2,
 u'currency_code': 3,
 u'currency_name': 13,
 u'currency_symbol': 6,
 u'equivalent_fips_code': 4,
 u'fips': 2,
 u'geonameid': 7,
 u'iso3': 3,
 u'iso_numeric': 3,
 u'languages': 89,
 u'name': 44,
 u'neighbours': 41,
 u'phone': 5,
 u'population': 10
 u'postal_code_format': 55,
 u'postal_code_regex': 155,
 u'tld': 3,
 }
"""
