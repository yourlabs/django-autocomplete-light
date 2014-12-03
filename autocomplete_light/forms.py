"""
High-level API for django-autocomplete-light.

Before, django-autocomplete-light was just a container for a loosely coupled
set of tools. You had to go for a treasure hunt in the docs and source to find
just what you need and add it to your project.

While you can still do that, this module adds a high-level API which couples
all the little pieces together. Basically you could just inherit from ModelForm
or use modelform_factory() and expect everything to work out of the box, from
simple autocompletes to generic many to many autocompletes including a bug fix
for django bug #9321 or even added security.
"""
from __future__ import unicode_literals

import six

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django import forms
from django.db.models import ForeignKey, OneToOneField, ManyToManyField
from django.contrib.contenttypes.generic import (GenericForeignKey,
                                                 GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory as django_modelform_factory
from django.forms.models import ModelFormMetaclass as DjangoModelFormMetaclass

try:
    from genericm2m.models import RelatedObjectsDescriptor
except ImportError:
    RelatedObjectsDescriptor = None

try:
    from taggit.managers import TaggableManager
except ImportError:
    class TaggableManager(object):
        pass

from .registry import registry as default_registry
from .fields import (ModelChoiceField, ModelMultipleChoiceField,
        GenericModelChoiceField, GenericModelMultipleChoiceField)
from .contrib.taggit_field import TaggitField
from .widgets import ChoiceWidget, MultipleChoiceWidget

__all__ = ['modelform_factory', 'FormfieldCallback', 'ModelForm',
'SelectMultipleHelpTextRemovalMixin', 'VirtualFieldHandlingMixin',
'GenericM2MRelatedObjectDescriptorHandlingMixin']

# OMG #9321 why do we have to hard-code this ?
M = _('Hold down "Control", or "Command" on a Mac, to select more than one.')


class SelectMultipleHelpTextRemovalMixin(forms.BaseModelForm):
    """
    This mixin that removes the 'Hold down "Control" ...' message that is
    enforced in select multiple fields.

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
    Enable virtual field (generic foreign key) handling in django's ModelForm.

    - treat virtual fields like GenericForeignKey as normal fields,
    - when setting a GenericForeignKey value, also set the object id and
      content type id fields.

    Probably, django doesn't do that for legacy reasons: virtual fields were
    added after ModelForm and simply nobody asked django to add virtual field
    support in ModelForm.
    """
    def __init__(self, *args, **kwargs):
        """
        The constructor adds virtual field values to
        :py:attr:`django:django.forms.Form.initial`
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

                # Required for django-hstore support
                if not hasattr(value, '_meta'):
                    continue

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


class FormfieldCallback(object):
    """
    Decorate `model_field.formfield()` to use a
    `autocomplete_light.ModelChoiceField` for `OneToOneField` and
    `ForeignKey` or a `autocomplete_light.ModelMultipleChoiceField` for a
    `ManyToManyField`.

    It is the very purpose of our `ModelFormMetaclass` !
    """

    def __init__(self, default=None, meta=None):
        self.autocomplete_exclude = getattr(meta, 'autocomplete_exclude', None)
        self.autocomplete_fields = getattr(meta, 'autocomplete_fields', None)
        self.autocomplete_names = getattr(meta, 'autocomplete_names', {})

        def _default(model_field, **kwargs):
            return model_field.formfield(**kwargs)

        self.default = default or _default

    def __call__(self, model_field, **kwargs):
        if (self.autocomplete_exclude and
                model_field.name in self.autocomplete_exclude):
            pass

        elif (self.autocomplete_fields and
                model_field.name not in self.autocomplete_fields):
            pass

        elif hasattr(model_field, 'rel') and hasattr(model_field.rel, 'to'):
            if model_field.name in self.autocomplete_names:
                autocomplete = default_registry.get(
                    self.autocomplete_names[model_field.name])
            else:
                autocomplete = default_registry.autocomplete_for_model(
                    model_field.rel.to)

            if autocomplete is not None:
                kwargs['autocomplete'] = autocomplete

                if isinstance(model_field, (OneToOneField, ForeignKey)):
                    kwargs['form_class'] = ModelChoiceField
                elif isinstance(model_field, ManyToManyField):
                    kwargs['form_class'] = ModelMultipleChoiceField
                elif isinstance(model_field, TaggableManager):
                    kwargs['form_class'] = TaggitField
                else:
                    # none of our concern
                    kwargs.pop('form_class')

        return self.default(model_field, **kwargs)


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
        meta = attrs.get('Meta', None)

        # use our formfield_callback to add autocompletes if not already used
        formfield_callback = attrs.get('formfield_callback', None)

        if not isinstance(formfield_callback, FormfieldCallback):
            attrs['formfield_callback'] = FormfieldCallback(formfield_callback,
                    meta)

        if meta is not None:
            cls.clean_meta(meta)
            cls.pre_new(meta)

        new_class = super(ModelFormMetaclass, cls).__new__(cls, name, bases,
                attrs)

        if meta is not None:
            cls.post_new(new_class, meta)

        return new_class

    @classmethod
    def skip_field(cls, meta, field):
        if isinstance(field, GenericRelation):
            # skip reverse generic foreign key
            return True

        all_fields = set(getattr(meta, 'fields', [])) | set(getattr(meta,
            'autocomplete_fields', []))
        all_exclude = set(getattr(meta, 'exclude', [])) | set(getattr(meta,
            'autocomplete_exclude', []))

        if getattr(meta, 'fields', None) == '__all__':
            return field.name in all_exclude

        if len(all_fields) and field.name not in all_fields:
            return True

        if len(all_exclude) and field.name in all_exclude:
            return True

    @classmethod
    def clean_meta(cls, meta):
        # All virtual fields/excludes must be move to
        # autocomplete_fields/exclude
        fields = getattr(meta, 'fields', [])

        for field in fields:
            model_field = getattr(meta.model._meta.virtual_fields, field, None)

            if model_field is None:
                model_field = getattr(meta.model, field, None)

            if model_field is None:
                continue

            if ((RelatedObjectsDescriptor and isinstance(model_field,
                (RelatedObjectsDescriptor, GenericForeignKey))) or
                    isinstance(model_field, GenericForeignKey)):

                meta.fields.remove(field)

                if not hasattr(meta, 'autocomplete_fields'):
                    meta.autocomplete_fields = tuple()

                meta.autocomplete_fields += (field,)

    @classmethod
    def pre_new(cls, meta):
        exclude = tuple(getattr(meta, 'exclude', []))
        add_exclude = []

        # exclude gfk content type and object id fields
        for field in meta.model._meta.virtual_fields:
            if cls.skip_field(meta, field):
                continue

            if isinstance(field, GenericForeignKey):
                add_exclude += [field.ct_field, field.fk_field]

        if exclude:
            # safe concatenation of list/tuple
            # thanks lvh from #python@freenode
            meta.exclude = set(add_exclude) | set(exclude)

    @classmethod
    def post_new(cls, new_class, meta):
        cls.add_generic_fk_fields(new_class, meta)

        if RelatedObjectsDescriptor:
            # if genericm2m is installed
            cls.add_generic_m2m_fields(new_class, meta)

    @classmethod
    def add_generic_fk_fields(cls, new_class, meta):
        widgets = getattr(meta, 'widgets', {})

        # Add generic fk and m2m autocompletes
        for field in meta.model._meta.virtual_fields:
            if cls.skip_field(meta, field):
                continue

            # Check needed for compatibility with django-hstore
            if not hasattr(field, 'fk_field'):
                continue

            new_class.base_fields[field.name] = GenericModelChoiceField(
                widget=widgets.get(field.name, None),
                autocomplete=cls.get_generic_autocomplete(meta, field.name),
                required=not meta.model._meta.get_field_by_name(
                    field.fk_field)
            )

    @classmethod
    def add_generic_m2m_fields(cls, new_class, meta):
        widgets = getattr(meta, 'widgets', {})

        for field in meta.model.__dict__.values():
            if not isinstance(field, RelatedObjectsDescriptor):
                continue

            if cls.skip_field(meta, field):
                continue

            new_class.base_fields[field.name] = \
                GenericModelMultipleChoiceField(
                    widget=widgets.get(field.name, None),
                    autocomplete=cls.get_generic_autocomplete(
                        meta, field.name))

    @classmethod
    def get_generic_autocomplete(self, meta, name):
        autocomplete_name = getattr(meta, 'autocomplete_names', {}).get(
            name, None)

        if autocomplete_name:
            return default_registry[autocomplete_name]
        else:
            return default_registry.default_generic


class ModelForm(six.with_metaclass(ModelFormMetaclass,
        SelectMultipleHelpTextRemovalMixin, VirtualFieldHandlingMixin,
        GenericM2MRelatedObjectDescriptorHandlingMixin, forms.ModelForm)):
    """
    ModelForm override using our metaclass that adds our various mixins.

    .. py:attribute:: autocomplete_fields

        A list field names on which you want automatic autocomplete fields.

    .. py:attribute:: autocomplete_exclude

        A list of field names on which you do not want automatic autocomplete
        fields.

    .. py:attribute:: autocomplete_names

        A dict of ``field_name: AutocompleteName`` to override the default
        autocomplete that would be used for a field.

    Note: all of ``autocomplete_fields``, ``autocomplete_exclude`` and
    ``autocomplete_names`` understand generic foreign key and generic many to
    many descriptor names.
    """
    __metaclass__ = ModelFormMetaclass


def modelform_factory(model, autocomplete_fields=None,
                      autocomplete_exclude=None, autocomplete_names=None,
                      registry=None, **kwargs):
    """
    Wrap around Django's django_modelform_factory, using our ModelForm and
    setting autocomplete_fields and autocomplete_exclude.
    """
    if 'form' not in kwargs.keys():
        kwargs['form'] = ModelForm

    attrs = {'model': model}

    if autocomplete_fields is not None:
        attrs['autocomplete_fields'] = autocomplete_fields
    if autocomplete_exclude is not None:
        attrs['autocomplete_exclude'] = autocomplete_exclude
    if autocomplete_names is not None:
        attrs['autocomplete_names'] = autocomplete_names

    # If parent form class already has an inner Meta, the Meta we're
    # creating needs to inherit from the parent's inner meta.
    parent = (object,)
    if hasattr(kwargs['form'], 'Meta'):
        parent = (kwargs['form'].Meta, object)
    Meta = type(str('Meta'), parent, attrs)

    kwargs['form'] = type(kwargs['form'].__name__, (kwargs['form'],),
            {'Meta': Meta})

    if not issubclass(kwargs['form'], ModelForm):
        raise Exception('form kwarg must be an autocomplete_light ModelForm')

    return django_modelform_factory(model, **kwargs)
