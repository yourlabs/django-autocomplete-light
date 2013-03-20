"""
This is how to enable `language()` for one Autocomplete::

    import autocomplete_light
    from autocomplete_light.contrib.hvad import AutocompleteModelBase

    autocomplete_light.register(YourModel, AutocompleteModelBase)

Or, enable it globally by updating your `autodiscover()` call like this::

    import autocomplete_light
    from autocomplete_light.contrib.hvad import AutocompleteModelBase
    autocomplete_light.registry.autocomplete_model_base = AutocompleteModelBase
    autocomplete_light.autodiscover()

In that case, you can just register as usual::

    autocomplete_light.register(YourTranslatableModel)
"""

import autocomplete_light


class AutocompleteModel(autocomplete_light.AutocompleteModel):
    """ Ensure that `.language()` is called. """
    def __init__(self, request=None, values=None):
        """
        Overridden init to call .language(). Note: this will replace the
        base `choices`.
        """
        if getattr(self.choices.model.objects, 'language', False):
            self.choices = self.choices.model.objects.language()
        super(AutocompleteModel, self).__init__(request, values)


class AutocompleteModelBase(AutocompleteModel,
                            autocomplete_light.AutocompleteBase):
    """ Drop-in replacement for AutocompleteModelBase """
    pass


class AutocompleteModelTemplate(AutocompleteModel,
                                autocomplete_light.AutocompleteTemplate):
    """ Drop-in replacement for AutocompleteModelTemplate """
    pass
