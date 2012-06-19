from django import forms
from django.db import models
from django.forms import fields
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

__all__ = ('GenericModelForm', 'GenericModelChoiceField')


class GenericModelForm(forms.ModelForm):
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
        super(GenericModelForm, self).__init__(*args, **kwargs)

        # do what model_to_dict doesn't
        for field in self._meta.model._meta.virtual_fields:
            self.initial[field.name] = getattr(self.instance, field.name, None)

    def _post_clean(self):
        """
        What ModelForm does, but also set virtual field values from
        cleaned_data.
        """
        super(GenericModelForm, self)._post_clean()

        # take care of virtual fields since django doesn't
        for field in self._meta.model._meta.virtual_fields:
            value = self.cleaned_data.get(field.name, None)

            if value:
                setattr(self.instance, field.name, value)

    def save(self, commit=True):
        """
        What ModelForm does, but also set GFK.ct_field and GFK.fk_field if such
        a virtual field has a value.

        This should probably be done in the GFK field itself, but it's here for
        convenience until Django fixes that.
        """
        for field in self._meta.model._meta.virtual_fields:
            if isinstance(field, GenericForeignKey):
                value = self.cleaned_data.get(field.name, None)

                if not value:
                    continue

                setattr(self.instance, field.ct_field,
                        ContentType.objects.get_for_model(value))
                setattr(self.instance, field.fk_field, value.pk)

        return super(GenericModelForm, self).save(commit)


class GenericModelChoiceField(fields.Field):
    """
    Simple form field that converts strings to models.
    """
    def validate(self, value):
        if not value and not self.required:
            return True

        value = self.prepare_value(value)
        valid = self.widget.autocomplete(values=value).validate_values()

        if not valid:
            raise forms.ValidationError(u'%s cannot validate %s' % (
                self, value))

    def prepare_value(self, value):
        """
        Given a model instance as value, with content type id of 3 and pk of 5,
        return such a string '3-5'.
        """
        if isinstance(value, (str, unicode)):
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
        if not value:
            return value

        content_type_id, object_id = value.split('-')
        try:
            content_type = ContentType.objects.get_for_id(content_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError(u'Wrong content type')
        else:
            model = content_type.model_class()

        return model.objects.get(pk=object_id)
