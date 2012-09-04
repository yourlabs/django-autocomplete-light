from django.db import models
from django.core import urlresolvers


class Widget(models.Model):
    city = models.ForeignKey('cities_light.city', null=True, blank=True)
    users = models.ManyToManyField('auth.user', blank=True)

    def get_absolute_url(self):
        return urlresolvers.reverse('non_admin:widget_update', args=(self.pk,))
