from django.db import models


class Address(models.Model):
    city = models.ForeignKey('cities_light.city')
