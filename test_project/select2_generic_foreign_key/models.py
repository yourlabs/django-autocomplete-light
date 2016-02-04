from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TestModel(models.Model):
    name = models.CharField(max_length=200)

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        null=True,
        blank=True,
        editable=False,
    )

    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    test = GenericForeignKey('content_type', 'object_id')

    for_inline = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='inline_test_models'
    )

    def __str__(self):
        return self.name
