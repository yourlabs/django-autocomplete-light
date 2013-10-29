"""
Most of this deserve to be realesed in its own app.

I want a better implementation for this, so don't expect the low level internal
API to be stable until this comment is removed.
"""
from __future__ import unicode_literals

import six

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django import forms
from django.db.models import ForeignKey, OneToOneField, ManyToManyField
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory as django_modelform_factory
from django.forms.models import ModelFormMetaclass as DjangoModelFormMetaclass

try:
    from genericm2m.models import RelatedObjectsDescriptor
except ImportError:
    RelatedObjectsDescriptor = None

from .registry import registry as default_registry
from .fields import (ModelChoiceField, ModelMultipleChoiceField,
        GenericModelChoiceField, GenericModelMultipleChoiceField)
from .widgets import ChoiceWidget, MultipleChoiceWidget

__all__ = ['get_widgets_dict', 'modelform_factory', 'FormfieldCallback',
'ModelForm', 'SelectMultipleHelpTextRemovalMixin', 'VirtualFieldHandlingMixin',
'SecureModelFormMixin', 'GenericM2MRelatedObjectDescriptorHandlingMixin']

M = _(' Hold down "Control", or "Command" on a Mac, to select more than one.')


class SelectMultipleHelpTextRemovalMixin(forms.BaseModelForm):
    """
    Simple child of mixin that removes the 'Hold down "Control" ...'
    message that is enforced in select multiple fields.

    See https://code.djangoproject.com/ticket/9321
    """

    def __init__(self, *args, **kwargs):
        super(SelectMultipleHelpTextRemovalMixin, self).__init__(*args,
                **kwargs)
        msg = force_text(M)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, RelatedFieldWidgetWrapper):
                widget = widget.widget

            if not isinstance(widget, MultipleChoiceWidget):
                continue

            field.help_text = field.help_text.replace(msg, '')


class VirtualFieldHandlingMixin(forms.BaseModelForm):
    """
    This simple subclass of ModelForm fixes a couple of issues with django's
    ModelForm.

    - treat virtual fields like GenericForeignKey as normal fields, Django
      should already do that but it doesn't,
    - when setting a GenericForeignKey value, also set the object id and
      content type id fields, again Django could probably afford to do that.
    """
    def __init__(self, *args, **kwargs):
        """
        What ModelForm does, but also add virtual field values to self.initial.
        """
        super(VirtualFieldHandlingMixin, self).__init__(*args, **kwargs)

        # do what model_to_dict doesn't
        for field in self._meta.model._meta.virtual_fields:
            self.initial[field.name] = getattr(self.instance, field.name, None)

    def _post_clean(self):
        """
        What ModelForm does, but also set virtual field values from
        cleaned_data.
        """
        super(VirtualFieldHandlingMixin, self)._post_clean()

        # take care of virtual fields since django doesn't
        for field in self._meta.model._meta.virtual_fields:
            value = self.cleaned_data.get(field.name, None)

            if value:
                setattr(self.instance, field.name, value)

                self.cleaned_data[field.ct_field] = \
                    ContentType.objects.get_for_model(value)
                self.cleaned_data[field.fk_field] = value.pk


class GenericM2MRelatedObjectDescriptorHandlingMixin(forms.BaseModelForm):
    """
    Extension of autocomplete_light.GenericModelForm, that handles
    genericm2m's RelatedObjectsDescriptor.
    """

    def __init__(self, *args, **kwargs):
        """
        Add related objects to initial for each generic m2m field.
        """
        super(GenericM2MRelatedObjectDescriptorHandlingMixin, self).__init__(
            *args, **kwargs)

        for name, field in self.generic_m2m_fields():
            related_objects = getattr(self.instance, name).all()
            self.initial[name] = [x.object for x in related_objects]

    def generic_m2m_fields(self):
        """
        Yield name, field for each RelatedObjectsDescriptor of the model of
        this ModelForm.
        """
        for name, field in self.fields.items():
            if not isinstance(field, GenericModelMultipleChoiceField):
                continue

            model_class_attr = getattr(self._meta.model, name, None)
            if not isinstance(model_class_attr, RelatedObjectsDescriptor):
                continue

            yield name, field

    def save(self, commit=True):
        """
        Save the form and particularely the generic many to many relations.
        """
        instance = super(GenericM2MRelatedObjectDescriptorHandlingMixin,
                self).save(commit=commit)

        def save_m2m():
            for name, field in self.generic_m2m_fields():
                model_attr = getattr(instance, name)
                selected_relations = self.cleaned_data.get(name, [])

                for related in model_attr.all():
                    if related.object not in selected_relations:
                        model_attr.remove(related)

                for related in selected_relations:
                    model_attr.connect(related)

        if hasattr(self, 'save_m2m'):
            old_m2m = self.save_m2m

            def _():
                save_m2m()
                old_m2m()
            self.save_m2m = _
        else:
            save_m2m()

        return instance


class SecureModelFormMixin(object):
    def secure_for_request(self, request):
        pass


class FormfieldCallback(object):
    """
    Decorate `model_field.formfield()` to use a
    `autocomplete_light.ModelChoiceField` for `OneToOneField` and
    `ForeignKey` or a `autocomplete_light.ModelMultipleChoiceField` for a
    `ManyToManyField`.

    It is the very purpose of our `ModelFormMetaclass` !
    """

    def __init__(self, default=None):
        def _default(model_field, **kwargs):
            return model_field.formfield(**kwargs)

        self.default = default or _default

    def __call__(self, model_field, **kwargs):
        if hasattr(model_field, 'rel') and hasattr(model_field.rel, 'to'):
            autocomplete = default_registry.autocomplete_for_model(
                model_field.rel.to)

            if autocomplete is not None:
                if isinstance(model_field, (OneToOneField, ForeignKey)):
                    kwargs['form_class'] = ModelChoiceField
                elif isinstance(model_field, ManyToManyField):
                    kwargs['form_class'] = ModelMultipleChoiceField

                kwargs['autocomplete'] = autocomplete

        if self.default:
            return self.default(model_field, **kwargs)
        else:
            return model_field.formfield(**kwargs)


class ModelFormMetaclass(DjangoModelFormMetaclass):
    """
    Wrap around django's ModelFormMetaclass to add autocompletes.
    """
    def __new__(cls, name, bases, attrs):
        """
        Add autocompletes in three steps:

        - use our formfield_callback for basic field autocompletes: one to one,
        foreign key, many to many
        - exclude generic foreign key content type foreign key and object id
        field,
        - add autocompletes for generic foreign key and generic many to many.
        """
        # use our formfield_callback to add autocompletes
        attrs['formfield_callback'] = FormfieldCallback(
            attrs.pop('formfield_callback', None))

        meta = attrs.get('Meta', None)

        if meta is not None:
            cls.pre_new(meta)

        new_class = super(ModelFormMetaclass, cls).__new__(cls, name, bases,
                attrs)

        if meta is not None:
            cls.post_new(new_class, meta)

        return new_class

    @classmethod
    def pre_new(cls, meta):
        fields = getattr(meta, 'fields', None)
        exclude = getattr(meta, 'exclude', [])
        add_exclude = []

        # exclude gfk content type and object id fields
        for field in meta.model._meta.virtual_fields:
            if exclude and field.name in exclude:
                continue

            if fields and field.name not in fields:
                continue

            if isinstance(field, GenericForeignKey):
                add_exclude += [field.ct_field, field.fk_field]

        if exclude:
            # safe concatenation of list/tuple
            meta.exclude = add_exclude + [f for f in exclude]

    @classmethod
    def post_new(cls, new_class, meta):
        cls.add_generic_fk_fields(new_class, meta)

        if RelatedObjectsDescriptor:
            # if genericm2m is installed
            cls.add_generic_m2m_fields(new_class, meta)

    @classmethod
    def add_generic_fk_fields(cls, new_class, meta):
        fields = getattr(meta, 'fields', None)
        exclude = getattr(meta, 'exclude', [])

        # Add generic fk and m2m autocompletes
        for field in meta.model._meta.virtual_fields:
            if field.name in exclude:
                continue

            if fields and field.name not in fields:
                continue

            new_class.base_fields[field.name] = GenericModelChoiceField(
                required=not meta.model._meta.get_field_by_name(
                    field.fk_field))

    @classmethod
    def add_generic_m2m_fields(cls, new_class, meta):
        fields = getattr(meta, 'fields', None)
        exclude = getattr(meta, 'exclude', [])

        for field in meta.model.__dict__.values():
            if not isinstance(field, RelatedObjectsDescriptor):
                continue

            if field.name in exclude:
                continue

            if fields and field.name not in fields:
                continue

            new_class.base_fields[field.name] = \
                GenericModelMultipleChoiceField()


class ModelForm(six.with_metaclass(ModelFormMetaclass,
        SelectMultipleHelpTextRemovalMixin, VirtualFieldHandlingMixin,
        GenericM2MRelatedObjectDescriptorHandlingMixin, forms.ModelForm)):
    """ Simple ModelForm override that adds our various mixins. """
    pass


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

    if 'form' not in kwargs.keys():
        kwargs['form'] = ModelForm

    kwargs['formfield_callback'] = FormfieldCallback(
        kwargs.pop('formfield_callback'))

    return django_modelform_factory(model, **kwargs)
