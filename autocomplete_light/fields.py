from __future__ import unicode_literals

import six
from django import forms
from django.db import models
from django.db.models.query import QuerySet

from .registry import registry as default_registry
from .widgets import ChoiceWidget, MultipleChoiceWidget

__all__ = ['FieldBase', 'ChoiceField', 'MultipleChoiceField',
    'ModelChoiceField', 'ModelMultipleChoiceField', 'GenericModelChoiceField',
    'GenericModelMultipleChoiceField']


class FieldBase(object):
    def __init__(self, autocomplete=None, registry=None, widget=None,
            widget_js_attributes=None, autocomplete_js_attributes=None,
            extra_context=None, *args, **kwargs):

        self.autocomplete = self.get_autocomplete(autocomplete, registry,
                widget)

        widget = widget or self.widget
        if isinstance(widget, type):
            widget = widget(autocomplete, widget_js_attributes,
                    autocomplete_js_attributes, extra_context)
        kwargs['widget'] = widget

        # Does the subclass have ModelChoiceField or ModelMultipleChoiceField
        # as a base class?
        parents = type(self).__mro__
        if ((forms.ModelChoiceField in parents or
                forms.ModelMultipleChoiceField in parents) and
                isinstance(self.autocomplete.choices, QuerySet)):
            kwargs['queryset'] = self.autocomplete.choices

        super(FieldBase, self).__init__(*args, **kwargs)

    def get_autocomplete(self, autocomplete, registry, widget):
        if widget:
            # BC: maybe defining the autocomplete as a widget argument ?
            autocomplete = getattr(widget, 'autocomplete', None)

        registry = registry or default_registry
        return registry.get_autocomplete_from_arg(autocomplete)

    def validate(self, value):
        """
        Wrap around forms.Field and Autocomplete.validate_values().

        Field.validate_values() handles the required option.
        """
        forms.Field.validate(self, value)

        # FIXME: we might actually want to change the Autocomplete API to
        # support python values instead of raw values, that would probably be
        # more performant.
        values = self.prepare_value(value)

        if value and not self.autocomplete(values=values).validate_values():
            raise forms.ValidationError('%s cannot validate %s' % (
                self.autocomplete.__name__, value))


class ChoiceField(FieldBase, forms.ChoiceField):
    widget = ChoiceWidget

    def __init__(self, autocomplete=None, registry=None, widget=None,
            widget_js_attributes=None, autocomplete_js_attributes=None,
            extra_context=None, *args, **kwargs):

        kwargs.update({'choices':
            self.get_choices(autocomplete, registry, widget)})

        super(ChoiceField, self).__init__(autocomplete, registry, widget,
                widget_js_attributes, autocomplete_js_attributes,
                extra_context, *args, **kwargs)

    def get_choices(self, autocomplete, registry, widget):
        a = self.get_autocomplete(autocomplete, registry, widget)()
        return ((a.choice_value(c), a.choice_label(c)) for c in a.choices)


class MultipleChoiceField(ChoiceField, forms.MultipleChoiceField):
    widget = MultipleChoiceWidget


class ModelChoiceFieldBase(FieldBase):
    def _get_queryset(self):
        return self._queryset

    def _set_queryset(self, queryset):
        self._queryset = queryset
        self.widget.choices = self.choices

        # Also update autocomplete choices
        self.autocomplete.choices = queryset

    queryset = property(_get_queryset, _set_queryset)


class ModelChoiceField(ModelChoiceFieldBase, forms.ModelChoiceField):
    widget = ChoiceWidget


class ModelMultipleChoiceField(ModelChoiceFieldBase,
        forms.ModelMultipleChoiceField):
    widget = MultipleChoiceWidget


class GenericModelChoiceField(ModelChoiceFieldBase, forms.Field):
    """
    Simple form field that converts strings to models.
    """
    widget = ChoiceWidget

    def prepare_value(self, value):
        """
        Given a model instance as value, with content type id of 3 and pk of 5,
        return such a string '3-5'.
        """
        from django.contrib.contenttypes.models import ContentType

        if isinstance(value, six.string_types):
            # Apparently there's a bug in django, that causes a python value to
            # be passed here. This ONLY happens when in an inline ....
            return value
        elif isinstance(value, models.Model):
            return '%s-%s' % (ContentType.objects.get_for_model(value).pk,
                              value.pk)

    def to_python(self, value):
        """
        Given a string like '3-5', return the model of content type id 3 and pk
        5.
        """
        from django.contrib.contenttypes.models import ContentType

        if not value:
            return value

        content_type_id, object_id = value.split('-', 1)
        try:
            content_type = ContentType.objects.get_for_id(content_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError('Wrong content type')
        else:
            model = content_type.model_class()

        try:
            return model.objects.get(pk=object_id)
        except model.DoesNotExist:
            raise forms.ValidationError('Wrong object id')


class GenericModelMultipleChoiceField(GenericModelChoiceField):
    """
    Simple form field that converts strings to models.
    """
    widget = MultipleChoiceWidget

    def prepare_value(self, value):
        return [super(GenericModelMultipleChoiceField, self
            ).prepare_value(v) for v in value]

    def to_python(self, value):
        return [super(GenericModelMultipleChoiceField, self).to_python(v)
            for v in value]
