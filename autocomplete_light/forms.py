"""
A couple of helper functions to help enabling Widget in ModelForms.
"""
from django.forms.models import modelform_factory as django_modelform_factory
from django.db.models import ForeignKey, OneToOneField

from .widgets import ChoiceWidget, MultipleChoiceWidget

__all__ = ['get_widgets_dict', 'modelform_factory']


def get_widgets_dict(model, autocomplete_exclude=None, registry=None):
    """
    Return a dict of field_name: widget_instance for model that is compatible
    with Django.

    autocomplete_exclude
        List of model field names to ignore

    registry
        Registry to use.

    Inspect the model's field and many to many fields, calls
    registry.autocomplete_for_model to get the autocomplete for the related
    model. If a autocomplete is returned, then an Widget will be spawned using
    this autocomplete.

    The dict is usable by ModelForm.Meta.widgets. In django 1.4, with
    modelform_factory too.
    """
    if autocomplete_exclude is None:
        autocomplete_exclude = []

    if registry is None:
        from .registry import registry

    widgets = {}

    for field in model._meta.fields:
        if field.name in autocomplete_exclude:
            continue

        if not isinstance(field, (ForeignKey, OneToOneField)):
            continue

        autocomplete = registry.autocomplete_for_model(field.rel.to)
        if not autocomplete:
            continue

        widgets[field.name] = ChoiceWidget(autocomplete=autocomplete)

    for field in model._meta.many_to_many:
        if field.name in autocomplete_exclude:
            continue

        autocomplete = registry.autocomplete_for_model(field.rel.to)
        if not autocomplete:
            continue

        widgets[field.name] = MultipleChoiceWidget(autocomplete=autocomplete)

    return widgets


def modelform_factory(model, autocomplete_exclude=None, registry=None,
                      **kwargs):
    """
    Wraps around Django's django_modelform_factory, using get_widgets_dict.

    autocomplete_exclude
        List of model field names to ignore

    registry
        Registry to use.

    Basically, it will use the dict returned by get_widgets_dict in order and
    pass it to django's modelform_factory, and return the resulting modelform.
    """

    if registry is None:
        from .registry import registry

    widgets = get_widgets_dict(model, registry=registry,
                               autocomplete_exclude=autocomplete_exclude)
    widgets.update(kwargs.pop('widgets', {}))
    kwargs['widgets'] = widgets

    return django_modelform_factory(model, **kwargs)
