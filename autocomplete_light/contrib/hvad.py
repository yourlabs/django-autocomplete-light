"""
This module provides out of the box django-hvad support.

There are two ways to use this module.

The first one is by subclassing HvadAutocompleteModelBase.
The advantage here is that you can specify the language at request
time with the GET parameter 'lang'.

Example::

  from autocomplete_light.contrib.hvad import HvadAutocompleteModelBase

  class YourModelAutocomplete(HvadAutocompleteModelBase):
      search_fields = ('name', )
      autocomplete_js_attributes={'placeholder': 'name it ..'}

  register(YourModel, YourModelAutocomplete)


The other way sets the language at registration.

Example::

    from autocomplete_light.contrib.hvad import register

    register(YourModel, lang='ru')


.. Warning::
  Don't mix these two ways. After setting the language at registration
  you can't (re)set the language at request time!


"""

import autocomplete_light
from django.db.models import Q

class HvadAutocompleteModelBase(autocomplete_light.AutocompleteModelBase):

    def choices_for_request(self):
        assert self.choices is not None, 'choices should be a queryset'
        assert self.search_fields, 'autocomplete.search_fields must be set'
        q = self.request.GET.get('q', '')
        lang = self.request.GET.get('lang', '')
        exclude = self.request.GET.getlist('exclude', [])
        lang = self.request.GET.get('lang', '')

        if lang:
            self.choices = self.choices.model.objects.language(lang).all()

        conditions = Q()
        if q:
            for search_field in self.search_fields:
                conditions |= Q(**{search_field + '__icontains': q})

        return self.order_choices(self.choices.filter(
            conditions).exclude(pk__in=exclude))[0:self.limit_choices]


def register(*args, **kwargs):
    """
    Decorate the stock register() function, generating an hvad-compatible
    choices queryset.
    """
    model, autocomplete = autocomplete_light.AutocompleteRegistry.extract_args(*args)

    if model is not None and 'choices' not in kwargs and 'lang' in kwargs:
        kwargs['choices'] = model.objects.language(kwargs['lang']).all()

    return autocomplete_light.register(*args, **kwargs)
