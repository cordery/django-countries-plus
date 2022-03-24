from django.db import models


class Company(models.Model):
    class Meta:
        verbose_name_plural = 'Companies'

    name = models.CharField(max_length=512)
    country = models.ForeignKey(
        'countries_plus.Country', related_name='companies', on_delete=models.PROTECT
    )
