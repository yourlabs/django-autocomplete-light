from django.forms.models import modelform_factory as django_modelform_factory
from django.db.models import ForeignKey, OneToOneField

from .widgets import *
from .registry  import *

def get_widgets_dict(model, autocomplete_exclude=None):
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
            print "Excluding", field.name
            continue

        channel = registry.channel_for_model(field.rel.to)
        if not channel:
            continue

        widgets[field.name] = AutocompleteWidget(channel_name=channel.__name__)

    return widgets

def modelform_factory(model, autocomplete_exclude=None,
    **kwargs):

    widgets = get_widgets_dict(model, autocomplete_exclude=autocomplete_exclude)
    widgets.update(kwargs.pop('widgets', {}))
    kwargs['widgets'] = widgets

    return django_modelform_factory(model, **kwargs)
