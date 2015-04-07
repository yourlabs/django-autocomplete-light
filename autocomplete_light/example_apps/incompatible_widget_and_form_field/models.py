from django.db import models


class Film(models.Model):
    relation = models.ForeignKey('self', blank=True, null=True)
