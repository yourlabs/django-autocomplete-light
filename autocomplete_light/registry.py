from __future__ import unicode_literals

import six

from django.db import models
from .compat import get_model, import_string

from .exceptions import (AutocompleteArgNotUnderstood,
                         AutocompleteNotRegistered,
                         NoGenericAutocompleteRegistered,
                         NonDjangoModelSubclassException)

"""
The registry module provides tools to maintain a registry of autocompletes.

The first thing that should happen when django starts is registration of
autocompletes. It should happen first, because autocompletes are required for
widgets. And autocomplete widgets are required for forms. And forms are
required for ModelAdmin.

It looks like this:

- in ``yourapp/autocomplete_light_registry.py``, register your autocompletes
  with :py:func:`autocomplete_light.register() <register>`,
- in ``urls.py``, call :py:func:`autocomplete_light.autodiscover()
  <autodiscover>` **before** :py:func:`admin.autodiscover()`.

.. py:data:: registry

    Module-level instance of :py:class:`AutocompleteRegistry`.
"""

try:
    from django.utils.module_loading import autodiscover_modules
except ImportError:
    autodiscover_modules = None

__all__ = ('AutocompleteRegistry', 'registry', 'register', 'autodiscover')


class AutocompleteRegistry(dict):
    """
    AutocompleteRegistry is a dict of ``AutocompleteName: AutocompleteClass``
    with some shortcuts to handle a registry of autocompletes.

    .. py:attribute:: autocomplete_model_base

        The default model autocomplete class to use when registering a Model
        without Autocomplete class. Default is
        :py:class:`~.autocomplete.AutocompleteModelBase`. You can override
        it just before calling autodiscover() in urls.py as such::

            import autocomplete_light.shortcuts as al
            al.registry.autocomplete_model_base = al.AutocompleteModelTemplate
            al.autodiscover()
    """

    def __init__(self, autocomplete_model_base=None):
        """
        You can pass a custom base autocomplete which will be set to
        :py:attr:`autocomplete_model_base` when instanciating an
        AutocompleteRegistry.
        """
        self._models = {}
        self.default_generic = None
        self.autocomplete_model_base = autocomplete_model_base

    def autocomplete_for_model(self, model):
        """
        Return the default autocomplete class for a given model or None.
        """
        try:
            return self._models[model]
        except KeyError:
            return

    def autocomplete_for_generic(self):
        """ Return the default generic autocomplete. """
        if self.default_generic is None:
            raise NoGenericAutocompleteRegistered(self)

        return self.default_generic

    def unregister(self, name):
        """ Unregister a autocomplete given a name. """
        autocomplete = self[name]
        del self[name]

        try:
            if self._models[autocomplete.choices.model].name == name:
                del self._models[autocomplete.choices.model]
        except AttributeError:
            pass

    @classmethod
    def extract_args(cls, *args):
        """
        Takes any arguments like a model and an autocomplete, or just one of
        those, in any order, and return a model and autocomplete.
        """
        model = None
        autocomplete = None

        for arg in args:
            if issubclass(arg, models.Model):
                model = arg
            else:
                autocomplete = arg

        return [model, autocomplete]

    def register(self, *args, **kwargs):
        """
        Register an autocomplete.

        Two unordered arguments are accepted, at least one should be passed:

        - a model if not a generic autocomplete,
        - an autocomplete class if necessary, else one will be generated.

        'name' is also an acceptable keyword argument, that can be used to
        override the default autocomplete name which is the class name by
        default, which could cause name conflicts in some rare cases.

        In addition, keyword arguments will be set as class attributes.

        For thread safety reasons, a copy of the autocomplete class is stored
        in the registry.
        """
        assert len(args) <= 2, 'register takes at most 2 args'
        assert len(args) > 0, 'register takes at least 1 arg'

        processed_args = []

        for arg in args:
            if isinstance(arg, six.string_types):
                parts = arg.split('.')
                if len(parts) == 2:
                    # if 'app_name.ModelName'
                    app_label = parts[0]
                    model_name = parts[-1]
                    model = get_model(app_label=app_label, model_name=model_name)  # noqa
                    processed_args.append(model)
                elif len(parts) > 2:
                    # if 'full.path.to.Model'
                    model = import_string(arg)
                    if not issubclass(model, models.Model):
                        raise NonDjangoModelSubclassException('%s not is subclass of django Model'  # noqa
                                                              % model.__name__)
                    processed_args.append(model)
                else:
                    processed_args.append(arg)
            else:
                processed_args.append(arg)

        model, autocomplete = self.__class__.extract_args(*processed_args)

        # If calling register(YourBaseAutocomplete, YourModel) then you want
        # the autocomplete name to be YourModelYourBaseAutocomplete, but if
        # calling register(YourBaseAutocomplete) then name should be
        # YourBaseAutocomplete
        derivate_name = model and autocomplete

        if autocomplete and not model:
            try:
                model = autocomplete.choices.model
            except AttributeError:
                model = getattr(autocomplete, 'model', None)

        if model:
            autocomplete = self._register_model_autocomplete(model,
                                                             autocomplete,
                                                             derivate_name,
                                                             **kwargs)
        else:
            name = kwargs.get('name', autocomplete.__name__)
            autocomplete = type(str(name), (autocomplete,), kwargs)
            self._register_autocomplete(autocomplete)

        return autocomplete

    def _register_model_autocomplete(self, model, autocomplete=None,
                                     derivate_name=False, name=None, **kwargs):
        if name is not None:
            pass

        elif autocomplete is not None:
            if autocomplete.__name__.find(model.__name__) == 0:
                derivate_name = False

            if derivate_name:
                name = '%s%s' % (model.__name__, autocomplete.__name__)
            else:
                name = autocomplete.__name__
        else:
            name = '%sAutocomplete' % model.__name__

        if autocomplete is None:
            if self.autocomplete_model_base is None:
                from .autocomplete.shortcuts import AutocompleteModelBase
                self.autocomplete_model_base = AutocompleteModelBase
            base = self.autocomplete_model_base
        else:
            base = autocomplete

        if base.choices is None and 'choices' not in kwargs:
            kwargs['choices'] = model._default_manager.all()

        if base.search_fields is None and 'search_fields' not in kwargs:
            try:
                model._meta.get_field('name')
            except:
                raise Exception('Add search_fields kwargs to .register(%s)'
                                % model.__name__)
            else:
                kwargs['search_fields'] = ['name']

        kwargs.update({'model': model})

        autocomplete = type(str(name), (base,), kwargs)

        self._register_autocomplete(autocomplete)

        if model not in self._models.keys():
            self._models[model] = autocomplete

        return autocomplete

    def _register_autocomplete(self, autocomplete):
        """
        Register a autocomplete without model, like a generic autocomplete.
        """
        self[autocomplete.__name__] = autocomplete

        if not getattr(autocomplete, 'model', False):
            if not self.default_generic:
                self.default_generic = autocomplete

    def __getitem__(self, name):
        """
        Return the Autocomplete class registered for this name. If none is
        registered, raise AutocompleteNotRegistered.
        """
        try:
            return super(AutocompleteRegistry, self).__getitem__(name)
        except KeyError:
            raise AutocompleteNotRegistered(name, self)

    def get_autocomplete_from_arg(self, arg=None):
        from .autocomplete.base import AutocompleteInterface
        if isinstance(arg, six.string_types):
            return self[arg]
        elif isinstance(arg, type) and issubclass(arg, models.Model):
            return self.autocomplete_for_model(arg)
        elif isinstance(arg, models.Model):
            return self.autocomplete_for_model(arg.__class__)
        elif isinstance(arg, type) and issubclass(arg, AutocompleteInterface):
            return arg
        elif arg is None:
            return self.default_generic
        else:
            raise AutocompleteArgNotUnderstood(arg, self)


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

    For each app, autodiscover imports ``app.autocomplete_light_registry`` if
    possing, resulting in execution of :py:func:`register()` statements in that
    module, filling up :py:data:`registry`.

    Consider a standard app called ``cities_light`` with such a structure::

        cities_light/
            __init__.py
            models.py
            urls.py
            views.py
            autocomplete_light_registry.py

    Where autocomplete_light_registry.py contains something like::

        from models import City, Country
        import autocomplete_light.shortcuts as al
        al.register(City)
        al.register(Country)

    When ``autodiscover()`` imports
    ``cities_light.autocomplete_light_registry``, both ``CityAutocomplete`` and
    ``CountryAutocomplete`` will be registered. See
    :py:meth:`AutocompleteRegistry.register()` for details on how these
    autocomplete classes are generated.
    """
    if autodiscover_modules:
        autodiscover_modules('autocomplete_light_registry')
    else:
        _autodiscover(registry)


def register(*args, **kwargs):
    """
    Proxy method :py:meth:`AutocompleteRegistry.register` of the
    :py:data:`registry` module level instance.
    """
    return registry.register(*args, **kwargs)
