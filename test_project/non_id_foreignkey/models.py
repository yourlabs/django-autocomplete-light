from django.db import models


class CodeModel(models.Model):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class ItemModel(models.Model):
    code = models.ForeignKey('CodeModel', to_field='code')
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
