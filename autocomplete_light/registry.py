"""
The registry module provides tools to maintain a registry of channels and
static file dependencies.

The first thing that should happen when django starts is registration of
channels. It should happen first, because channels are required for
autocomplete widgets. And autocomplete widgets are required for forms. And
forms are required for ModelAdmin.

It looks like this:

- in ``yourapp/autocomplete_light_registry.py``, register your channels with
  ``autocomplete_light.register()``,
- in ``urls.py``, do ``autocomplete_light.autodiscover()`` **before**
  ``admin.autodiscover()``.

ChannelRegistry
    Subclass of Python's dict type with registration/unregistration methods.

registry
    Instance of ChannelRegistry.

register
    Proxy registry.register.

autodiscover
    Find channels and javascript and css, fill registry and static_list.
"""

import os.path

from django.db import models

from .channel import ChannelBase

__all__ = ('ChannelRegistry', 'registry', 'register', 'autodiscover')


class ChannelRegistry(dict):
    """
    Dict with some shortcuts to handle a registry of channels.
    """

    def __init__(self):
        self.static_list = []
        self._models = {}
        self._static = {}

    def channel_for_model(self, model):
        """Return the channel class for a given model."""
        try:
            return self._models[model]
        except KeyError:
            return

    def unregister(self, name):
        """
        Unregister a channel.
        """
        channel = self[name]
        del self[name]

        if channel.model:
            del self._models[channel.model]

        for path in channel.static_list:
            del self._static[path][self._static[path].index(name)]
            if len(self._static[path]) == 0:
                del self.static_list[self.static_list.index(path)]

    def register(self, *args, **kwargs):
        """
        Proxy registry.register_model_channel() or registry.register_channel()
        if there is no apparent model for the channel.

        Example usages::

            # Will create and register SomeModelChannel, if SomeChannel.model
            # is None (which is the case by default):
            autocomplete_light.register(SomeModel)

            # Same but using SomeChannel as base:
            autocomplete_light.register(SomeModel, SomeChannel)

            # Register a channel without model, ensure that SomeChannel.model
            # is None (which is the default):
            autocomplete_light.register(SomeChannel)

            # As of 0.5, you may also pass attributes*, ie.:
            autocomplete_light.register(SomeModel, search_field='search_names',
                result_template='somemodel_result.html')

        You may pass attributes via kwargs, only if the registry creates a
        type:

        - if no channel class is passed,
        - or if the channel class has no model attribute,
        - and if the channel classs is not generic
        """

        channel = None
        model = None

        for arg in args:
            if issubclass(arg, models.Model):
                model = arg
            elif issubclass(arg, ChannelBase):
                channel = arg

        if channel and getattr(channel, 'model'):
            model = channel.model

        if model:
            self.register_model_channel(model, channel, **kwargs)
        else:
            self.register_channel(channel)

    def register_model_channel(self, model, channel=None, **kwargs):
        """
        Add a model to the registry, optionnaly with a given channel class.

        model
            The model class to register.

        channel
            The channel class to register the model with, default to
            ChannelBase.

        kwargs
            Extra attributes to set to the channel class, if created by this
            method.

        Three cases are possible:

        - specify model class and ModelNameChannel will be generated extending
          ChannelBase, with attribute model=model
        - specify a model and a channel class that does not have a model
          attribute, and a ModelNameChannel will be generated, with attribute
          model=model
        - specify a model and a channel class with a model attribute, and the
          channel is directly registered

        To keep things simple, the name of a channel is it's class name.
        """
        kwargs.update({'model': model})

        if channel is None:
            channel = type('%sChannel' % model.__name__, (ChannelBase,),
                kwargs)
        elif channel.model is None:
            channel = type('%sChannel' % model.__name__, (channel,),
                kwargs)

        self.register_channel(channel)
        self._models[channel.model] = channel

    def register_channel(self, channel):
        """
        Register a channel without model, like a generic channel.
        """
        self[channel.__name__] = channel

        for path in getattr(channel, 'static_list', []):
            if path not in self.static_list:
                self.static_list.append(path)

            if path not in self._static:
                self._static[path] = []
            self._static[path].append(channel.__name__)


def _autodiscover(registry):
    """See documentation for autodiscover (without the underscore)"""
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # check if the app has static/appname/autocomplete_light.js
        css_path = 'static/%s/autocomplete_light.css' % mod.__name__
        if os.path.exists(os.path.join(mod.__path__[0], css_path)):
            if css_path[7:] not in registry.static_list:
                registry.static_list.append(css_path[7:])

        js_path = 'static/%s/autocomplete_light.js' % mod.__name__
        if os.path.exists(os.path.join(mod.__path__[0], js_path)):
            if js_path[7:] not in registry.static_list:
                registry.static_list.append(js_path[7:])

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

registry = ChannelRegistry()


def autodiscover():
    """
    Check all apps in INSTALLED_APPS for stuff related to autocomplete_light.

    For each app, autodiscover:

    - imports app.autocomplete_light_registry if available, resulting in
      execution of register() statements in that module, filling registry
    - checks for app/static/app/autocomplete_light.js, adds it to static_list
    - checks for app/static/app/autocomplete_light.css, adds it to static_list

    Consider a standard app called 'cities_light' with such a structure::

        cities_light/
            __init__.py
            models.py
            urls.py
            views.py
            autocomplete_light_registry.py
            static/
                cities_light/
                    autocomplete_light.js
                    autocomplete_light.css

    With such a autocomplete_light_registry.py::

        from models import City, Country
        import autocomplete_light
        autocomplete_light.register(City)
        autocomplete_light.register(Country)

    When autodiscover() imports cities_light.autocomplete_light_registry, both
    CityChannel and CountryChannel will be registered. For details on how these
    channel classes are generated, read the documentation of
    ChannelRegistry.register.

    Also, 'cities_light/autocomplete_light.js' and
    'cities_light/autocomplete_light.css' will be appended to static_list. This
    list is used by the autocomplete_light_static templatetag, read it's
    documentation for details.
    """
    _autodiscover(registry)


def register(*args, **kwargs):
    """Proxy registry.register"""
    return registry.register(*args, **kwargs)
