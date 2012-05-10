"""
A couple of shortcut functions to enable AutocompleteWidget in ModelForms.

get_widgets_dict
    Return a dict of field_name: widget_instance for model.

modelform_factory
    Return a modelform with AutocompleteWidgets.
"""
from django.forms.models import modelform_factory as django_modelform_factory
from django.db.models import ForeignKey, OneToOneField

from .widgets import AutocompleteWidget
from .registry  import registry

__all__ = ['get_widgets_dict', 'modelform_factory']

def get_widgets_dict(model, autocomplete_exclude=None):
    """
    Return a dict of field_name: widget_instance for model that is compatible
    with Django.
    
    autocomplete_exclude
        the list of model field names to ignore

    Inspect the model's field and many to many fields, calls
    registry.channel_for_model to get the channel for the related model. If a
    channel is returned, then an AutocompleteWidget will be spawned using this
    channel.

    More information:
    https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-field-types-or-widgets
    """
    if autocomplete_exclude is None:
        autocomplete_exclude = []

    widgets = {}

    for field in model._meta.fields:
        if field.name in autocomplete_exclude:
            continue

        if not isinstance(field, (ForeignKey, OneToOneField)):
            continue

        channel = registry.channel_for_model(field.rel.to)
        if not channel:
            continue
        
        widgets[field.name] = AutocompleteWidget(channel_name=channel.__name__, 
            max_items=1)

    for field in model._meta.many_to_many:
        if field.name in autocomplete_exclude:
            continue

        channel = registry.channel_for_model(field.rel.to)
        if not channel:
            continue

        widgets[field.name] = AutocompleteWidget(channel_name=channel.__name__)

    return widgets

def modelform_factory(model, autocomplete_exclude=None,
    **kwargs):
    """
    Wraps around Django's django_modelform_factory, using get_widgets_dict.
    """

    widgets = get_widgets_dict(model, autocomplete_exclude=autocomplete_exclude)
    widgets.update(kwargs.pop('widgets', {}))
    kwargs['widgets'] = widgets

    return django_modelform_factory(model, **kwargs)
