# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-27 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20180127_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u65f6\u957f(\u5206\u949f\u6570)'),
        ),
    ]
