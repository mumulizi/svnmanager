# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-17 05:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20170328_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='online',
            name='sexcludedir',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
