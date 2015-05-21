from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class YourModel(models.Model):
    name = models.CharField(max_length=100)
    relation = models.ForeignKey('self', null=True, blank=True)
    
    def __str__(self):
        return self.name
