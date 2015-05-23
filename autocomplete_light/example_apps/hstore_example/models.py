from django.db import models

from django_hstore import hstore


class HstoreModel(models.Model):
    name = models.CharField(max_length=32)
    data = hstore.DictionaryField()

    objects = hstore.HStoreManager()
