from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Artist(models.Model):
    name = models.CharField(max_length=100)

    genre = models.ForeignKey(Genre)

    def __unicode__(self):
        return '%s %s' % (self.name, self.genre)

    class Meta:
        ordering = ('name',)
