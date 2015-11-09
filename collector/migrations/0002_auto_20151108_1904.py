# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='aplications',
            new_name='applications',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='id',
        ),
        migrations.AddField(
            model_name='offer',
            name='id_supplier',
            field=models.CharField(default=datetime.datetime(2015, 11, 8, 19, 4, 45, 765005, tzinfo=utc), max_length=256, serialize=False, primary_key=True),
            preserve_default=False,
        ),
    ]
