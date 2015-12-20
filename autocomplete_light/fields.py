from __future__ import unicode_literals

import six
from django import forms
from django.db import models
from django.db.models.query import QuerySet

from .registry import registry as default_registry
from .widgets import ChoiceWidget, MultipleChoiceWidget
from .exceptions import AutocompleteChoicesMustBeQuerySet

__all__ = ['FieldBase', 'ChoiceField', 'MultipleChoiceField',
    'ModelChoiceField', 'ModelMultipleChoiceField', 'GenericModelChoiceField',
    'GenericModelMultipleChoiceField']


class FieldBase(object):
    """
    FieldBase for autocomplete widgets.

    .. py:attribute:: request

        If set before the form validates, then enable it to be part of the
        validation process, enabling custom security based on the request user,
        please read the :doc:`tutorial` section about this for complete
        details.
    """

    default_error_messages = {
        'invalid': '%(autocomplete)s cannot validate %(value)s',
    }

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
        if (forms.ModelChoiceField in parents or
                forms.ModelMultipleChoiceField in parents):

            if not isinstance(self.autocomplete.choices, QuerySet):
                raise AutocompleteChoicesMustBeQuerySet(self.autocomplete)
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

        # Security: if the field was added a ``request`` object, then force
        # override of autocomplete.choices using choices_for_request() before
        # validating values.
        request = getattr(self, 'request', None)
        autocomplete = self.autocomplete(values=values, request=request)
        if request is not None:
            autocomplete.choices = autocomplete.choices_for_request()

        if value and not self.autocomplete(values=values).validate_values():
            error_params = {
                'autocomplete': self.autocomplete.__name__, 'value': value
            }

            raise forms.ValidationError(self.error_messages['invalid'],
                                        code='invalid', params=error_params)


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


class ModelChoiceField(FieldBase, forms.ModelChoiceField):
    widget = ChoiceWidget


class ModelMultipleChoiceField(FieldBase,
        forms.ModelMultipleChoiceField):
    widget = MultipleChoiceWidget


class GenericModelChoiceField(FieldBase, forms.Field):
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
