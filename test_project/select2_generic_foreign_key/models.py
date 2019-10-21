from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from six import python_2_unicode_compatible


@python_2_unicode_compatible
class TModel(models.Model):
    name = models.CharField(max_length=200)

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        models.CASCADE,
        null=True,
        blank=True,
        editable=False,
        related_name='content_type_test_models'
    )

    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    test = GenericForeignKey('content_type', 'object_id')

    content_type2 = models.ForeignKey(
        'contenttypes.ContentType',
        models.CASCADE,
        null=True,
        blank=True,
        editable=False,
        related_name='content_type_test_models2'
    )

    object_id2 = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    test2 = GenericForeignKey('content_type2', 'object_id2')

    for_inline = models.ForeignKey(
        'self',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='inline_test_models'
    )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TProxyModel(TModel):
    class Meta:
        proxy = True

    def __str__(self):
        return self.name
