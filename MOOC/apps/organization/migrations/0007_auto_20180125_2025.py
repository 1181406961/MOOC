# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-25 20:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20180125_2021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='ponits',
            new_name='points',
        ),
    ]
