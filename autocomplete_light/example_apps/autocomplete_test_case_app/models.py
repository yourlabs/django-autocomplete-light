from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    groups = models.ManyToManyField('Group')


class Group(models.Model):
    name = models.CharField(max_length=100)
