from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField('self', blank=True)
    private = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name
