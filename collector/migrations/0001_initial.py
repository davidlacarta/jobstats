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
                ('offer', models.CharField(max_length=256, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256, null=True, blank=True)),
                ('description', models.CharField(max_length=5000, null=True, blank=True)),
                ('requirements', models.CharField(max_length=5000, null=True, blank=True)),
                ('link', models.URLField(max_length=5000, null=True, blank=True)),
                ('country', models.CharField(max_length=256, null=True, blank=True)),
                ('province', models.CharField(max_length=256, null=True, blank=True)),
                ('city', models.CharField(max_length=256, null=True, blank=True)),
                ('fetch_date', models.DateTimeField(null=True)),
                ('publish_date', models.DateTimeField(null=True)),
                ('salary_max', models.IntegerField(null=True, blank=True)),
                ('salary_min', models.IntegerField(null=True, blank=True)),
                ('applications', models.IntegerField(null=True, blank=True)),
                ('vacancies', models.IntegerField(null=True, blank=True)),
                ('experience', models.IntegerField(null=True, blank=True)),
            ],
        ),
    ]
