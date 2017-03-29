from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class ModelOne(models.Model):
    """Model One."""

    name = models.CharField('Name', max_length=100)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = 'ModelOne'


class ModelTwo(models.Model):
    """Model Two"""

    name = models.CharField('Name', max_length=100, )

    class Meta:
        verbose_name = 'ModelTwo'

    def __str__(self):
        return self.name


class MasterModel(models.Model):
    """Model connecting to ModelOne and ModelTwo."""

    name = models.CharField('Name', max_length=100, )

    modelone = models.ManyToManyField(
        ModelOne,
        verbose_name='ModelOne',
        blank=True,
    )
    modeltwo = models.ManyToManyField(
        ModelTwo,
        blank=True,
        verbose_name='ModelTwo',
    )

    class Meta:
        verbose_name = 'MasterModel'

    def __str__(self):
        return self.name