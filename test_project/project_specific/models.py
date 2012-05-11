from django.db import models

import cities_light


def filter_city_import(sender, items, **kwargs):
    if items[8] not in ('FR', 'US', 'BE'):
        raise cities_light.InvalidItems()
cities_light.signals.city_items_pre_import.connect(filter_city_import)

class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.ForeignKey('cities_light.City')
