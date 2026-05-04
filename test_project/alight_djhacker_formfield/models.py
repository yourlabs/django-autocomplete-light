from django.db import models


class TModel(models.Model):
    name = models.CharField(max_length=200)
    test = models.ForeignKey(
        'self', models.CASCADE, null=True, blank=True,
        related_name='related_test_models_adf',
    )
    for_inline = models.ForeignKey(
        'self', models.CASCADE, null=True, blank=True,
        related_name='inline_test_models_adf',
    )

    class Meta:
        db_table = 'select2_djhacker_formfield_tmodel'
        managed = False
        ordering = ['name']

    def __str__(self):
        return self.name
