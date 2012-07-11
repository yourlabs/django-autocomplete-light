"""
The registry module provides tools to maintain a registry of autocompletes.

The first thing that should happen when django starts is registration of
autocompletes. It should happen first, because autocompletes are required for
widgets. And autocomplete widgets are required for forms. And forms are
required for ModelAdmin.

It looks like this:

- in ``yourapp/autocomplete_light_registry.py``, register your autocompletes
  with ``autocomplete_light.register()``,
- in ``urls.py``, do ``autocomplete_light.autodiscover()`` **before**
  ``admin.autodiscover()``.

AutocompleteRegistry
    Subclass of Python's dict type with registration/unregistration methods.

registry
    Instance of AutocompleteRegistry.

register
    Proxy registry.register.

autodiscover
    Find autocompletes and fill registry.
"""

from django.db import models

from .autocomplete import AutocompleteModelBase

__all__ = ('AutocompleteRegistry', 'registry', 'register', 'autodiscover')


class AutocompleteRegistry(dict):
    """
    Dict with some shortcuts to handle a registry of autocompletes.
    """

    def __init__(self):
        self._models = {}

    def autocomplete_for_model(self, model):
        """ Return the autocomplete class for a given model. """
        try:
            return self._models[model]
        except KeyError:
            return

    def unregister(self, name):
        """ Unregister a autocomplete. """
        autocomplete = self[name]
        del self[name]

        try:
            if autocomplete.choices.model:
                del self._models[autocomplete.choices.model]
        except AttributeError:
            pass

    def register(self, *args, **kwargs):
        """
        Register an autocomplete.

        Two unordered arguments are accepted, at least one should be passed:

        - a model if not a generic autocomplete,
        - an autocomplete class if necessary, else one will be generated.

        'name' is also an acceptable keyword argument, that can be used to
        override the default autocomplete name (which is its class name).

        In addition, keyword arguments will be set as class attributes. For
        thread safety reasons, a copy of the autocomplete class is stored in
        the registry.
        """
        autocomplete = None
        model = None

        assert len(args) <= 2, 'register takes at most 2 args'
        assert len(args) > 0, 'register takes at least 1 arg'

        for arg in args:
            if issubclass(arg, models.Model):
                model = arg
            else:
                autocomplete = arg

        if not model:
            try:
                model = autocomplete.choices.model
            except AttributeError:
                pass

        if model:
            self._register_model_autocomplete(model, autocomplete, **kwargs)
        else:
            name = kwargs.get('name', autocomplete.__name__)
            autocomplete = type(name, (autocomplete,), kwargs)
            self._register_autocomplete(autocomplete)

    def _register_model_autocomplete(self, model, autocomplete=None,
                                    name=None, **kwargs):

        if name is not None:
            pass
        elif autocomplete is not None:
            if autocomplete.__name__.find(model.__name__) == 0:
                name = autocomplete.__name__
            else:
                name = '%s%s' % (model.__name__, autocomplete.__name__)
        else:
            name = '%sAutocomplete' % model.__name__

        if autocomplete is None:
            base = AutocompleteModelBase
        else:
            base = autocomplete

        if base.choices is None:
            kwargs['choices'] = model.objects.all()

        if base.search_fields is None and 'search_fields' not in kwargs:
            try:
                model._meta.get_field('name')
            except:
                raise Exception(u'Add search_fields kwargs to .register(%s)'
                    % model.__name__)
            else:
                kwargs['search_fields'] = ['name']

        autocomplete = type(name, (base,), kwargs)

        self._register_autocomplete(autocomplete)
        self._models[model] = autocomplete

    def _register_autocomplete(self, autocomplete):
        """
        Register a autocomplete without model, like a generic autocomplete.
        """
        self[autocomplete.__name__] = autocomplete


def _autodiscover(registry):
    """See documentation for autodiscover (without the underscore)"""
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            before_import_registry = copy.copy(registry)
            import_module('%s.autocomplete_light_registry' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'autocomplete_light_registry'):
                raise

registry = AutocompleteRegistry()


def autodiscover():
    """
    Check all apps in INSTALLED_APPS for stuff related to autocomplete_light.

    For each app, autodiscover imports app.autocomplete_light_registry if
    available, resulting in execution of register() statements in that module,
    filling registry.

    Consider a standard app called 'cities_light' with such a structure::

        cities_light/
            __init__.py
            models.py
            urls.py
            views.py
            autocomplete_light_registry.py

    With such a autocomplete_light_registry.py::

        from models import City, Country
        import autocomplete_light
        autocomplete_light.register(City)
        autocomplete_light.register(Country)

    When autodiscover() imports cities_light.autocomplete_light_registry, both
    CityAutocomplete and CountryAutocomplete will be registered. For details on
    how these autocomplete classes are generated, read the documentation of
    AutocompleteRegistry.register.
    """
    _autodiscover(registry)


def register(*args, **kwargs):
    """Proxy registry.register"""
    return registry.register(*args, **kwargs)
