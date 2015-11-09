# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0004_auto_20151109_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='fetching_date',
        ),
    ]
