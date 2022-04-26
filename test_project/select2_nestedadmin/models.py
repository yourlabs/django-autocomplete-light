from django.db import models


class TModelOne(models.Model):
    name = models.CharField(max_length=200)
    level_one = models.CharField(max_length=20, blank=True, default='one')

    def __str__(self):
        return self.name


class TModelTwo(models.Model):
    name = models.CharField(max_length=200)
    level_two = models.CharField(max_length=20, blank=True, default='two')

    parent = models.ForeignKey(
        'select2_nestedadmin.TModelOne',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return self.name


class TModelThree(models.Model):
    name = models.CharField(max_length=200)

    parent = models.ForeignKey(
        'select2_nestedadmin.TModelTwo',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    test = models.ForeignKey(
        'self',
        models.CASCADE,
        null=True,
        blank=True,
        related_name='related_test_models'
    )

    def __str__(self):
        return self.name
