from django.db import models


class TModel(models.Model):
    name = models.CharField(max_length=200)

    test = models.ForeignKey(
        'self',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='related_test_models_asd',
    )

    owner = models.ForeignKey(
        'auth.user',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='owned_models_asd',
    )

    for_inline = models.ForeignKey(
        'self',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='inline_test_models_asd',
    )

    class Meta:
        db_table = 'select2_secure_data_tmodel'
        managed = False
        ordering = ['name']

    def __str__(self):
        return self.name
