# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_autocomplete_in_row', '0002_auto_20150519_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yourmodel',
            name='name2',
        ),
        migrations.RemoveField(
            model_name='yourmodel',
            name='name3',
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='nouveau_champs',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
