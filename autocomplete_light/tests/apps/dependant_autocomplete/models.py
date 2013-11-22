from django.db import models


class Dummy(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True)
    country = models.ForeignKey('cities_light.country')
    region = models.ForeignKey('cities_light.region')

    def __unicode__(self):
        return u'%s %s' % (self.country, self.region)