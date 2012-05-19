from django.db import models

import cities_light


def filter_city_import(sender, items, **kwargs):
    if items[8] not in ('FR', 'US', 'BE'):
        raise cities_light.InvalidItems()
cities_light.signals.city_items_pre_import.connect(filter_city_import)

class Contact(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ('name',)

class Address(models.Model):
    contact = models.ForeignKey('Contact')
    street = models.CharField(max_length=100)
    city = models.ForeignKey('cities_light.City')

    def __unicode__(self):
        return u'%s %s %s' % (self.contact, self.city, self.street)
        
    class Meta:
        ordering = ('contact', 'city')
