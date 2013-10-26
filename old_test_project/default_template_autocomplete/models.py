from django.db import models
from django.core.urlresolvers import reverse


class TemplatedChoice(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_absolute_update_url(self):
        url = 'admin:default_template_autocomplete_templatedchoice_change'
        return reverse(url, args=(self.pk,))

    def get_absolute_url(self):
        return reverse('templated_choice_detail', args=(self.pk,))


class TestModel(models.Model):
    choices = models.ManyToManyField(TemplatedChoice)

    def __unicode__(self):
        return u', '.join(self.choices.values_list('name', flat=True))
