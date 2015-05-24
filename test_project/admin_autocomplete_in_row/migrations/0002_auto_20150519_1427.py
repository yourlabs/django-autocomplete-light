# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_autocomplete_in_row', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='yourmodel',
            name='name2',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='name3',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]
