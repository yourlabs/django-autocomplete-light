from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tagging.fields import TagField


@python_2_unicode_compatible
class TestModel(models.Model):
    name = models.CharField(max_length=200)

    test = TagField()

    for_inline = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='inline_test_models'
    )

    def __str__(self):
        return self.name
