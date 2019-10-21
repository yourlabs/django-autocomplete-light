from django.db import models

from six import python_2_unicode_compatible


@python_2_unicode_compatible
class TModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
