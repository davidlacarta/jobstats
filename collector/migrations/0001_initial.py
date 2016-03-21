# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=256)),
                ('value', models.CharField(max_length=256, null=True, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=256)),
                ('value', models.CharField(max_length=256, null=True, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256, null=True, blank=True)),
                ('description', models.CharField(max_length=5000, null=True, blank=True)),
                ('requirements', models.CharField(max_length=5000, null=True, blank=True)),
                ('link', models.URLField(max_length=5000, null=True, blank=True)),
                ('fetch_date', models.DateTimeField(null=True, blank=True)),
                ('publish_date', models.DateTimeField(null=True, blank=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('salary_max', models.IntegerField(null=True, blank=True)),
                ('salary_min', models.IntegerField(null=True, blank=True)),
                ('experience_min', models.IntegerField(null=True, blank=True)),
                ('applications', models.IntegerField(null=True, blank=True)),
                ('vacancies', models.IntegerField(null=True, blank=True)),
                ('city', models.ForeignKey(blank=True, to='collector.City', null=True)),
                ('country', models.ForeignKey(blank=True, to='collector.Country', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=256)),
                ('value', models.CharField(max_length=256, null=True, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=256)),
                ('value', models.CharField(max_length=256, null=True, blank=True)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('country', models.ForeignKey(to='collector.Country')),
            ],
        ),
        migrations.AddField(
            model_name='offer',
            name='provider',
            field=models.ForeignKey(to='collector.Provider'),
        ),
        migrations.AddField(
            model_name='offer',
            name='province',
            field=models.ForeignKey(blank=True, to='collector.Province', null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(to='collector.Province'),
        ),
        migrations.AlterUniqueTogether(
            name='province',
            unique_together=set([('country', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='offer',
            unique_together=set([('provider', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('province', 'key')]),
        ),
    ]
