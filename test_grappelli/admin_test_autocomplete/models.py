from django.db import models


class Foo(models.Model):
    name = models.CharField(max_length=100)
    bar = models.ForeignKey('Bar', related_name='bar_fk')

    def __unicode__(self):
        return self.name


class Bar(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
