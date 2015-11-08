# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poblation', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=5000, null=True, blank=True)),
                ('aplications', models.IntegerField(null=True, blank=True)),
                ('salary_max', models.IntegerField(null=True, blank=True)),
                ('salary_min', models.IntegerField(null=True, blank=True)),
                ('fetching_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
