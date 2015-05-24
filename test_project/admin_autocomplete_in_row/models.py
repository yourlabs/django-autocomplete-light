from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class YourModel(models.Model):
    name = models.CharField(max_length=100)
    relation = models.ForeignKey('self', null=True, blank=True)

    name2 = models.CharField(max_length=100, null=True, blank=True)
    date_and_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
