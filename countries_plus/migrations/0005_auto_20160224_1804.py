# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countries_plus', '0004_auto_20150616_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='area',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
    ]
