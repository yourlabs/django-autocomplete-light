from django.db import models

from django.contrib.contenttypes import generic


class TaggedItem(models.Model):
    content_type = models.ForeignKey('contenttypes.contenttype', related_name='my_tagged_item')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    tag = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s %s' % (self.tag, self.content_object)
