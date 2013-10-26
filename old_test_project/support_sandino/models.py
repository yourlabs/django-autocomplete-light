from django.db import models

class Location(models.Model):
    street = models.CharField(max_length=50, blank=True)
    city = models.ForeignKey('cities_light.City')
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

class Event(models.Model):
    slug = models.CharField(max_length=128, blank=True)
    begin_date = models.DateField(null=True)
    location = models.ForeignKey(Location, blank=True, null=True)
