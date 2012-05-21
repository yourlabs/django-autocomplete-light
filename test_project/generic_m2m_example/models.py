from django.db import models
from django.db.models import signals
from django.contrib.contenttypes import generic

from genericm2m.models import RelatedObjectsDescriptor

class ModelGroup(models.Model):
    name = models.CharField(max_length=100)

    related = RelatedObjectsDescriptor()

    def __unicode__(self):
        return self.name
