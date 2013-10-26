from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class SomeModel(models.Model):
    name = models.CharField(max_length=200)


class Relationship(models.Model):
    person_content_type = models.ForeignKey(ContentType, related_name="person_type_set")
    person_object_id = models.PositiveIntegerField()
    person = generic.GenericForeignKey("person_content_type", "person_object_id")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")
