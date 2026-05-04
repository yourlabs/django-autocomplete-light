from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='tmodel',
            name='test',
            field=models.ManyToManyField(blank=True, related_name='related_test_models', symmetrical=False, to='alight_many_to_many.tmodel'),
        ),
    ]
