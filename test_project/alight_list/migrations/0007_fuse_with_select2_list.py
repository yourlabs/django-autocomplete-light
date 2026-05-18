from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alight_list', '0006_tmodel_for_inline_alter_tmodel_test'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tmodel',
            options={'managed': False, 'ordering': ['name']},
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterModelTable(
                    name='tmodel',
                    table='select2_list_tmodel',
                ),
            ],
            database_operations=[],
        ),
    ]
