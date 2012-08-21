from django.db import models

class Address(models.Model):
    city = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'addresses'

    def __unicode__(self):
        return "Address for city: " + self.city


class CityOrSomethingElse(models.Model):
    city_or_something_else = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'city or something else'

    def __unicode__(self):
        return self.city_or_something_else