from __future__ import unicode_literals

from django.core import urlresolvers
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class NonAdminAddAnotherModel(models.Model):
    name = models.CharField(max_length=100)
    widgets = models.ManyToManyField('self', blank=True)

    def get_absolute_url(self):
        return urlresolvers.reverse(
            'non_admin_add_another_model_update', args=(self.pk,))

    def __str__(self):
        return self.name
