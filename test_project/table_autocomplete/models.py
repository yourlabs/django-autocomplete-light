from django.db import models


class TableWidget(models.Model):
    name = models.CharField(max_length=255)

    widgets = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        return self.name
