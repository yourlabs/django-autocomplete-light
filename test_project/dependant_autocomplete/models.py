from django.db import models


class Dummy(models.Model):
    country = models.ForeignKey('cities_light.country')
    region = models.ForeignKey('cities_light.region')

    def __unicode__(self):
        return u'%s %s' % (self.country, self.region)
