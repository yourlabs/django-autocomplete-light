from django.db import models


class TModel(models.Model):
    tags = models.CharField(max_length=500, blank=True, default='')

    def __str__(self):
        return self.tags or str(self.pk)
