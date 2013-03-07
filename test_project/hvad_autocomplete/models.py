from django.db import models
from django.core import urlresolvers
from hvad.models import TranslatableModel, TranslatedFields

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=255, db_index=True),
        slug = models.SlugField(max_length=255),
    )

    class Meta:
        verbose_name_plural = "categories"

    def lazy_language(self):
        """helper for usage in admin"""
        return self.language_code

    def lazy_name(self):
        """helper for usage in admin"""
        return self.lazy_translation_getter('name')

    def __unicode__(self):
        return u"%s" % (self.lazy_translation_getter('name'))


class Item(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True)

    def __unicode__(self):
        return u"Category: %s" % (self.category)

    def get_absolute_url(self):
        return urlresolvers.reverse('hvad_autocomplete:item_update',
                                    args=(self.pk,))
