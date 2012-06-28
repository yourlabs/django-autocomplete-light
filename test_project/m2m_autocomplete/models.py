from django.db import models


class VisitedCities(models.Model):
    cities = models.ManyToManyField('cities_light.City')

    class Meta:
        verbose_name_plural = 'visited cities'
