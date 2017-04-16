from django.db import models


class Cat(models.Model):
    name = models.CharField(
        max_length=63,
    )

    def __str__(self):
        return '{0}'.format(
            self.name
        )

    class Meta(object):
        verbose_name = 'Entry'



class TestMany(models.Model):
    category_key = models.ManyToManyField(
        Cat,
        verbose_name='Category',
        help_text='Can Belong to Many Categories',
    )

    def __str__(self):
        return 'id: {0}'.format(
            self.id,
        )

    class Meta(object):
        verbose_name = 'Many To Many Model'
