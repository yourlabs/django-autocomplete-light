from django.db import models


class TModel(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'select2_forward_different_fields_tmodel'
        managed = False
        ordering = ['name']

    def __str__(self):
        return self.name
