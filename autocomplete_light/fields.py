from django import forms
from django.db import models
from django import forms
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ModelChoiceField(forms.ModelChoiceField):
    pass


class ModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    pass


class GenericModelChoiceField(forms.Field):
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

        content_type_id, object_id = value.split('-', 1)
        try:
            content_type = ContentType.objects.get_for_id(content_type_id)
        except ContentType.DoesNotExist:
            raise forms.ValidationError(u'Wrong content type')
        else:
            model = content_type.model_class()

        return model.objects.get(pk=object_id)


class GenericModelMultipleChoiceField(GenericModelChoiceField):
    """
    Simple form field that converts strings to models.
    """
    def prepare_value(self, value):
        return [super(GenericModelMultipleChoiceField, self
            ).prepare_value(v) for v in value]

    def to_python(self, value):
        return [super(GenericModelMultipleChoiceField, self).to_python(v)
            for v in value]
