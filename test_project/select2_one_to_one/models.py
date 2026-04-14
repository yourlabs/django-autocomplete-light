from django.core.validators import validate_slug
from django.db import models


class TModel(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[validate_slug]
    )

    test = models.OneToOneField(
        'self',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='related_test_models'
    )

    for_inline = models.ForeignKey(
        'self',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='inline_test_models'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
