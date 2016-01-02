from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from taggit.managers import TaggableManager


@python_2_unicode_compatible
class TestModel(models.Model):
    name = models.CharField(max_length=200)

    test = TaggableManager()

    for_inline = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='inline_test_models'
    )

    def __str__(self):
        return self.name
