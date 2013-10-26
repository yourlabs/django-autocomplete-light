from django.db import models
from django.core import urlresolvers


class Widget(models.Model):
    name = models.CharField(max_length=100)
    widget = models.ForeignKey('self', null=True, blank=True,
        related_name='widget_fk')
    widgets = models.ManyToManyField('self', blank=True,
        related_name='widget_m2m')

    def get_absolute_url(self):
        return urlresolvers.reverse(
            'non_admin_add_another:widget_update', args=(self.pk,))

    def __unicode__(self):
        return self.name
