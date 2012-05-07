from .channel import ChannelBase

__all__ = ('ChannelRegistry', 'registry', 'register', 'autodiscover')

class ChannelRegistry(dict):
    _models = {} # warning: this variable may change structure, rely on channel_for_model

    def channel_for_model(self, model):
        try:
            return self._models[model]
        except KeyError:
            return

    def register(self, model, channel=None):
        if channel is None:
            channel = type('%sChannel' % model.__name__, (ChannelBase,), {'model': model})
        elif channel.model is None:
            channel = type('%sChannel' % model.__name__, (channel,), {'model': model})

        self[channel.__name__] = channel
        self._models[channel.model] = channel

def _autodiscover(registry):
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

registry = ChannelRegistry()
autodiscover = lambda: _autodiscover(registry)

def register(model, channel=None):
    registry.register(model, channel)
