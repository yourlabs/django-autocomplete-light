from django.db import models
from django.utils.translation import ugettext_lazy as _


class Media(models.Model):
    code = models.CharField(_(u'Code'), max_length=128, null=False, \
        blank=False, primary_key=True)
    name = models.CharField(_('Name'), max_length=128, null=True, \
        blank=True)

    def __unicode__(self):
        return self.name


class MediaFilter(models.Model):
    media = models.ForeignKey(Media, verbose_name=_("Media"))
