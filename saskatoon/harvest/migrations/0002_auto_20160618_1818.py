# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-18 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harvest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harvest',
            name='status',
            field=models.CharField(choices=[(b'To-be-confirmed', b'To be confirmed'), (b'Orphan', b'Orphan'), (b'Adopted', b'Adopted'), (b'Date-scheduled', b'Date scheduled'), (b'Ready', b'Ready'), (b'Succeeded', b'Succeeded'), (b'Cancelled', b'Cancelled')], max_length=100, null=True, verbose_name='Harvest status'),
        ),
        migrations.AlterField(
            model_name='historicalharvest',
            name='status',
            field=models.CharField(choices=[(b'To-be-confirmed', b'To be confirmed'), (b'Orphan', b'Orphan'), (b'Adopted', b'Adopted'), (b'Date-scheduled', b'Date scheduled'), (b'Ready', b'Ready'), (b'Succeeded', b'Succeeded'), (b'Cancelled', b'Cancelled')], max_length=100, null=True, verbose_name='Harvest status'),
        ),
        migrations.DeleteModel(
            name='HarvestStatus',
        ),
    ]
