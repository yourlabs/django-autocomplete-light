from django.db import models


class TModel(models.Model):
    test = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return self.test or str(self.pk)
