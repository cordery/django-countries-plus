# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('iso3', models.CharField(max_length=3, unique=True)),
                ('iso_numeric', models.IntegerField(max_length=3, unique=True)),
                ('fips', models.CharField(blank=True, null=True, max_length=3)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('capital', models.CharField(blank=True, null=True, max_length=30)),
                ('area', models.IntegerField(blank=True, null=True, max_length=8)),
                ('population', models.IntegerField(blank=True, null=True, max_length=10)),
                ('continent', models.CharField(blank=True, null=True, max_length=2)),
                ('tld', models.CharField(blank=True, null=True, max_length=5)),
                ('currency_code', models.CharField(blank=True, null=True, max_length=3)),
                ('currency_symbol', models.CharField(blank=True, null=True, max_length=7)),
                ('currency_name', models.CharField(blank=True, null=True, max_length=15)),
                ('phone', models.CharField(blank=True, null=True, max_length=5)),
                ('postal_code_format', models.CharField(blank=True, null=True, max_length=60)),
                ('postal_code_regex', models.CharField(blank=True, null=True, max_length=175)),
                ('languages', models.CharField(blank=True, null=True, max_length=100)),
                ('geonameid', models.IntegerField(blank=True, null=True, max_length=7)),
                ('neighbours', models.CharField(blank=True, null=True, max_length=50)),
                ('equivalent_fips_code', models.CharField(blank=True, null=True, max_length=4)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
    ]
