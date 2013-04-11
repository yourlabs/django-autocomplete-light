from django.db import models


class Creatable(models.Model):
    name = models.CharField(max_length=100)
    related = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        return self.name
