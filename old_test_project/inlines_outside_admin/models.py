from django.db import models

from tagging.fields import TagField
import tagging


class OutsideAdmin(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True)
    tags = TagField(null=True, blank=True)

    def __unicode__(self):
        return self.name

tagging.register(OutsideAdmin, tag_descriptor_attr='etags')
