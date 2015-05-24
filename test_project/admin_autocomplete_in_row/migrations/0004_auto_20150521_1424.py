# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_autocomplete_in_row', '0003_auto_20150521_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yourmodel',
            name='nouveau_champs',
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='date_and_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='name2',
            field=models.CharField(null=True, max_length=100, blank=True),
        ),
    ]
