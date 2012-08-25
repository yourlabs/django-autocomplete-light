from django.db import models


class City(models.Model):
    city = models.CharField(max_length=100)

    def __unicode__(self):
        return self.city


class Trip_City(models.Model):
    trip = models.ForeignKey('Trip')
    city = models.ForeignKey('City')
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('order',)


class Trip(models.Model):
    name = models.CharField(max_length=200)
    cities = models.ManyToManyField(City, through=Trip_City)