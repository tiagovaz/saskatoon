# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-24 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_beneficiary',
            field=models.BooleanField(default=False, verbose_name='is beneficiary'),
        ),
    ]