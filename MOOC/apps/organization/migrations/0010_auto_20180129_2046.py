# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-29 20:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_teacher_age'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='click_num',
            new_name='click_nums',
        ),
    ]
