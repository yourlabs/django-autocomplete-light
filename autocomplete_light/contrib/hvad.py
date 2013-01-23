"""
This module provides out of the box django-hvad support.

Example::

    from autocomplete_light.contrib.hvad import register

    register(YourModel, lang='ru')
"""

import autocomplete_light


def register(*args, **kwargs):
    """
    Decorate the stock register() function, generating an hvad-compatible
    choices queryset.
    """
    model, autocomplete = autocomplete_light.AutocompleteRegistry.extract_args(*args)

    if model is not None and 'choices' not in kwargs and 'lang' in kwargs:
        kwargs['choices'] = model.objects.language(kwargs['lang']).all()

    return autocomplete_light.register(*args, **kwargs)
