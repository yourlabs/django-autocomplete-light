from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TestModel(models.Model):
    name = models.CharField(max_length=200)

    test = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='related_test_models_rf'
    )

    owner = models.ForeignKey(
        'auth.user',
        null=True,
        blank=True,
        related_name='owned_linked_models_rf',
    )

    for_inline = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='inline_test_models_rf'
    )

    def __str__(self):
        return self.name
