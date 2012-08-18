from django.db import models

class ClickableItem(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class ClickableItemContainer(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(ClickableItem)

    def __unicode__(self):
        return self.name

