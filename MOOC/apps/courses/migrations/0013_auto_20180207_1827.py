# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-02-07 18:27
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20180206_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default=b'', verbose_name='\u8bfe\u7a0b\u8be6\u60c5'),
        ),
    ]
