import tagging
from django.db import models
from tagging.fields import TagField


class Taggable(models.Model):
    name = models.CharField(max_length=50)
    tags = TagField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.name

tagging.register(Taggable, tag_descriptor_attr='etags')
