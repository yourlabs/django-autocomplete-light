"""
This is how to enable `language()` for one Autocomplete::

    import autocomplete_light.shortcuts as al
    from al.contrib.hvad import AutocompleteModelBase

    al.register(YourModel, AutocompleteModelBase)

Or, enable it globally by updating your `autodiscover()` call like this::

    import autocomplete_light.shortcuts as al
    from al.contrib.hvad import AutocompleteModelBase
    al.registry.autocomplete_model_base = AutocompleteModelBase
    al.autodiscover()

In that case, you can just register as usual::

    al.register(YourTranslatableModel)
"""

import autocomplete_light.shortcuts as al


class AutocompleteModel(al.AutocompleteModel):
    """ Ensure that `.language()` is called. """
    def __init__(self, request=None, values=None):
        """
        Overridden init to call .language(). Note: this will replace the
        base `choices`.
        """
        if getattr(self.choices.model.objects, 'language', False):
            self.choices = self.choices.model.objects.language()
        super(AutocompleteModel, self).__init__(request, values)


class AutocompleteModelBase(AutocompleteModel, al.AutocompleteBase):
    """ Drop-in replacement for AutocompleteModelBase """
    pass


class AutocompleteModelTemplate(AutocompleteModel, al.AutocompleteTemplate):
    """ Drop-in replacement for AutocompleteModelTemplate """
    pass
