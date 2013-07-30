from django.db import models


class VisitedCities(models.Model):
    cities = models.ManyToManyField('cities_light.City')
    parent = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'visited cities'
