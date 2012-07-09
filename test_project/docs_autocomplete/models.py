from django.db import models


class Profile(models.Model):
    user = models.ForeignKey('auth.User')
    cities = models.ManyToManyField('cities_light.city')

    def __unicode__(self):
        return self.user.username
