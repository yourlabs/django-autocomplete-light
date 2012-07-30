from django.db import models


class Address(models.Model):
    city = models.ForeignKey('cities_light.city', related_name='address_inline_set')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
