# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0003_auto_20151109_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='fetching_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
