"""Autocomplete form fields for django-taggit."""

from dal.fields import CreateModelMultipleField

from taggit.models import Tag


class TaggitField(CreateModelMultipleField):
    """Form field for django-taggit."""

    def __init__(self, queryset=None, *args, **kwargs):
        """Make Tag.objects.all() the default queryset."""
        kwargs['queryset'] = queryset or Tag.objects.all()
        super(TaggitField, self).__init__(*args, **kwargs)

    def value_from_object(self, instance, name):
        """Retrieve the initial form value."""
        return None if not instance.pk else [
            x for x in getattr(instance, name).all()]
