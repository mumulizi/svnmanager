# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-24 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cronmanager', '0009_auto_20170524_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cron_info',
            name='cron_name',
            field=models.CharField(max_length=100),
        ),
    ]
