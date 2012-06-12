from django.db import models

class Address(models.Model):
    city = models.CharField(max_length=100)
