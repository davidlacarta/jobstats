# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0002_auto_20151108_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='poblation',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
