# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 17:53
from __future__ import unicode_literals

from django.db import migrations
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('select2_tagging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmodel',
            name='test',
            field=tagging.fields.TagField(blank=True, max_length=255),
        ),
    ]
