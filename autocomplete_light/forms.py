from django.forms.models import modelform_factory as django_modelform_factory
from django.db.models import ForeignKey, OneToOneField

from .widgets import *
from .registry  import *

def get_widgets_dict(model):
    widgets = {}

    for field in model._meta.fields:
        if not isinstance(field, (ForeignKey, OneToOneField)):
            continue

        channel = registry.channel_for_model(field.rel.to)
        if not channel:
            continue
        
        widgets[field.name] = AutocompleteWidget(channel_name=channel.__name__, 
            max_items=1)

    for field in model._meta.many_to_many:
        channel = registry.channel_for_model(field.rel.to)
        if not channel:
            continue

        widgets[field.name] = AutocompleteWidget(channel_name=channel.__name__)

    return widgets

def modelform_factory(model, **kwargs):
    widgets = get_widgets_dict(model)
    widgets.update(kwargs.pop('widgets', {}))
    kwargs['widgets'] = widgets

    return django_modelform_factory(model, **kwargs)
