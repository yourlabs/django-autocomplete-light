from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TModel(models.Model):
    name = models.CharField(max_length=200)

    group = models.ForeignKey(
        Group,
        models.CASCADE,
        null=True,
        blank=True,
        related_name='members',
    )

    test = models.ForeignKey(
        'self',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='related_test_models',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
