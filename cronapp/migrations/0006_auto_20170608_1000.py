# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-08 02:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cronapp', '0005_cron_info_approval_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cron_info',
            name='approval_time',
            field=models.CharField(default='\u672a\u63d0\u4ea4', max_length=150, verbose_name='\u5ba1\u6838\u65f6\u95f4\u548c\u52a8\u4f5c'),
        ),
    ]
