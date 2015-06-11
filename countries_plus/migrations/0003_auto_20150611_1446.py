# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countries_plus', '0002_auto_20150120_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='area',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='geonameid',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='iso_numeric',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='population',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
