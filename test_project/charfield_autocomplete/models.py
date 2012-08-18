from django.db import models

class Address(models.Model):
    city = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'addresses'

    def __unicode__(self):
        return "Address for city: " + self.city