from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
