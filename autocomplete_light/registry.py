"""
The registry module provides tools to maintain a registry of channels.

ChannelRegistry
    Subclass of Python's dict type with specific methods

registry
    Instance of ChannelRegistry

register
    Shortcut to registry.register()

autodiscover
    Find channels and javascript and css, fill registry and static_list

static_list
    List of static files found in other apps, used by the templatetag
"""

import os.path

from django.db import models

from .channel import ChannelBase

__all__ = ('ChannelRegistry', 'registry', 'register', 'autodiscover', 'static_list')

static_list = []

class ChannelRegistry(dict):
    """
    Dict with some shortcuts to handle a registry of channels.
    """

    # warning: this variable may change structure, rely on channel_for_model
    _models = {}

    def channel_for_model(self, model):
        """Return the channel class for a given model."""
        try:
            return self._models[model]
        except KeyError:
            return

    def unregister(self, arg):
        """
        Unregister a channel or the channel for a model. Return True on
        success.

        arg
            May be a model, or channel class.
        """
        if issubclass(arg, models.Model):
            if arg in self._models.keys():
                del self._models[arg]
                return True
        else:
            for key, value in self._models.items():
                if value == arg:
                    del self._models[key]
                    return True

    def register(self, model, channel=None):
        """
        Add a model to the registry, optionnaly with a given channel class.

        model
            the model class to register

        channel
            the channel class to register the model with, default to ChannelBase

        Three cases are possible:

        - specify model class and ModelNameChannel will be generated extending
          ChannelBase, with attribute model=model
        - specify a model and a channel class that does not have a model attribute,
          and a ModelNameChannel will be generated, with attribute model=model
        - specify a model and a channel class with a model attribute, and the
          channel is directly registered

        To keep things simple, the name of a channel is it's class name.
        """
        if channel is None:
            channel = type('%sChannel' % model.__name__, (ChannelBase,), {'model': model})
        elif channel.model is None:
            channel = type('%sChannel' % model.__name__, (channel,), {'model': model})

        for path in getattr(channel, 'static_list', []):
            if path not in static_list:
                static_list.append(path)

        self[channel.__name__] = channel
        self._models[channel.model] = channel


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
        if os.path.exists(os.path.join(mod.__path__[0], css_path)) and \
            css_path[7:] not in static_list:
            static_list.append(css_path[7:])
        js_path = 'static/%s/autocomplete_light.js' % mod.__name__
        if os.path.exists(os.path.join(mod.__path__[0], js_path)) and \
            js_path[7:] not in static_list:
            static_list.append(js_path[7:])

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

    Also, 'cities_light/autocomplete_light.js' and 'cities_light/autocomplete_light.css'
    will be appended to static_list. This list is used by the autocomplete_light_static
    templatetag, read it's documentation for details.
    """
    _autodiscover(registry)


def register(model, channel=None):
    """Pass arguments to registry.register"""
    registry.register(model, channel)
