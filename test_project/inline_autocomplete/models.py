from django.db import models

class Trip_City(models.Model):
    trip = models.ForeignKey('Trip')
    city = models.ForeignKey('cities_light.city')
    order = models.IntegerField()

class Trip(models.Model):
    name = models.CharField(max_length=200)
    cities = models.ManyToManyField('cities_light.city', through=Trip_City)