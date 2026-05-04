import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('object_id', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('object_id2', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('content_type', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_type_alight_test_models', to='contenttypes.contenttype')),
                ('content_type2', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_type_alight_test_models2', to='contenttypes.contenttype')),
                ('for_inline', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inline_test_models', to='alight_generic_foreign_key.tmodel')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TProxyModel',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('alight_generic_foreign_key.tmodel',),
        ),
    ]
