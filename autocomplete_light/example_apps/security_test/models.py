from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from ..autocomplete_test_case_app.models import User


@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField('self', blank=True)
    private = models.BooleanField(default=True)
    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name
