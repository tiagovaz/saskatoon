# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-29 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvest', '0005_auto_20160624_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='harvest',
            name='owner_no_fruit',
        ),
        migrations.RemoveField(
            model_name='historicalharvest',
            name='owner_no_fruit',
        ),
        migrations.AddField(
            model_name='harvest',
            name='owner_fruit',
            field=models.BooleanField(default=False, verbose_name='Owner want his share of fruits'),
        ),
        migrations.AddField(
            model_name='historicalharvest',
            name='owner_fruit',
            field=models.BooleanField(default=False, verbose_name='Owner want his share of fruits'),
        ),
    ]