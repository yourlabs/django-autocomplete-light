from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alight_list', '0004_alter_tmodel_table'),
    ]

    operations = [
        # Remove managed=False from Meta options
        migrations.AlterModelOptions(
            name='tmodel',
            options={'ordering': ['name']},
        ),
        # Update migration state to point back to the default table
        # (alight_list_tmodel already exists in the DB — no SQL needed)
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterModelTable(
                    name='tmodel',
                    table=None,
                ),
            ],
            database_operations=[],
        ),
        # Add name column back to alight_list_tmodel
        migrations.AddField(
            model_name='tmodel',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
