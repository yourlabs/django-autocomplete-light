from django import forms
from django.forms import fields
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class GenericModelForm(forms.ModelForm):
    """
    IMHO, this class should not be necessary: Django should take care of
    virtual fields like normal fields at the forms level (not at the database
    level obviously).
    """
    def __init__(self, *args, **kwargs):
        super(GenericModelForm, self).__init__(*args, **kwargs)

        # do what model_to_dict doesn't
        for field in self._meta.model._meta.virtual_fields:
            self.initial[field.name] = getattr(self.instance, field.name, None)

    def _post_clean(self):
        super(GenericModelForm, self)._post_clean()

        # take care of virtual fields since django doesn't
        for field in self._meta.model._meta.virtual_fields:
            setattr(self.instance, field.name, 
                self.cleaned_data.get(field.name, None))

    def save(self, commit=True):
        # do not require the pre_save signal that converts content_object to
        # content_type and object_id values
        for field in self._meta.model._meta.virtual_fields:
            if isinstance(field, GenericForeignKey):
                value = self.cleaned_data.get(field.name, None)
                
                if not value:
                    continue

                setattr(self.instance, field.ct_field, 
                    ContentType.objects.get_for_model(value))
                setattr(self.instance, field.fk_field, value.pk)

        return super(GenericModelForm, self).save(commit)

class GenericForeignKeyField(fields.Field):
    def prepare_value(self, value):
        if value:
            return '%s-%s' % (ContentType.objects.get_for_model(value).pk,
                value.pk)

    def to_python(self, value):
        content_type_id, object_id = value.split('-')
        model = ContentType.objects.get_for_id(content_type_id).model_class()
        return model.objects.get(pk=object_id)

