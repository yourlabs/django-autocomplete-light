from django.db import models
from taggit.managers import TaggableManager


class TModel(models.Model):
    name = models.CharField(max_length=200)
    test = TaggableManager(related_name='alight_taggit_tmodels')
    for_inline = models.ForeignKey(
        'self', models.CASCADE, null=True, blank=True,
        related_name='inline_test_models',
    )

    class Meta:
        db_table = 'select2_taggit_tmodel'
        managed = False
        ordering = ['name']

    def __str__(self):
        return self.name
