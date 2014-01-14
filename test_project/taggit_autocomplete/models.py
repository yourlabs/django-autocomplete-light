from django.db import models
from taggit.managers import TaggableManager

class TaggitDemo(models.Model):
    name = models.CharField(max_length=255)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.name

