from django.db import models


class TModelTest(models.Model):
    from_tmodel = models.ForeignKey('TModel', models.CASCADE, related_name='+')
    to_tmodel = models.ForeignKey('TModel', models.CASCADE, related_name='+')

    class Meta:
        db_table = 'select2_many_to_many_tmodel_test'
        managed = False


class TModel(models.Model):
    name = models.CharField(max_length=200)

    test = models.ManyToManyField(
        'self',
        through='TModelTest',
        blank=True,
        related_name='related_test_models',
    )

    for_inline = models.ForeignKey(
        'self',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='inline_test_models',
    )

    class Meta:
        db_table = 'select2_many_to_many_tmodel'
        managed = False
        ordering = ['name']

    def __str__(self):
        return self.name
