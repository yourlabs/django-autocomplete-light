from django.db import models

from django import forms
from django.forms.models import BaseModelForm, ModelFormMetaclass
from django.utils import six


class MagicFieldMixin(object):
    pass


class MagicFormMetaclass(ModelFormMetaclass):
    registry = {}

    @classmethod
    def register_formfield_for_modelfield(cls, model_field, form_field):
        cls.registry[model_field] = form_field

    @classmethod
    def get_meta(cls, name, bases, attrs):
        meta = attrs.get('Meta', None)

        # Maybe the parent has a meta ?
        if meta is None:
            for parent in bases + type(cls).__mro__:
                meta = getattr(parent, 'Meta', None)

                if meta is not None:
                    break

        return meta

    @classmethod
    def get_fields(cls, meta):
        fields = getattr(meta, 'fields', None)

        if fields == '__all__':
            return [f for f in meta.model._meta.fields]
        elif fields is None:
            exclude = getattr(meta, 'exclude', None)

            if exclude is None:
                raise Exception()

            return [f for f in meta.model._meta.fields
                    if f.name not in exclude]

        return meta.model._meta.fields

    def __new__(cls, name, bases, attrs):
        meta = cls.get_meta(name, bases, attrs)

        if meta is not None:
            for field in cls.get_fields(meta):
                if field.name in attrs:
                    # Skip manually declared field
                    continue

                if type(field) not in cls.registry:
                    # No form filed is registered for this type of field
                    continue

                attrs[field.name] = cls.registry[type(field)].factory(model, form, field)

        new_class = super(MagicFormMetaclass, cls).__new__(cls, name, bases,
                attrs)

        return new_class


class MagicForm(six.with_metaclass(MagicFormMetaclass, BaseModelForm)):
    __metaclass__ = MagicFormMetaclass
