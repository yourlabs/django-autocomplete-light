from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alight_many_to_many', '0003_alter_tmodel_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TModelTest',
        ),
    ]
