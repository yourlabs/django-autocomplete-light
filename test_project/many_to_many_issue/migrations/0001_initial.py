# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=63)),
            ],
            options={
                'verbose_name': 'Entry',
            },
        ),
        migrations.CreateModel(
            name='TestMany',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('category_key', models.ManyToManyField(help_text='Can Belong to Many Categories', verbose_name='Category', to='many.Cat')),
            ],
            options={
                'verbose_name': 'Many To Many Model',
            },
        ),
    ]
