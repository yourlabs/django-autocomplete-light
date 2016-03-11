"""Model choice fields that take a ContentType too: for generic relations."""

from django.contrib.contenttypes.models import ContentType
from django.utils import six


class ContentTypeModelFieldMixin(object):
    """
    Common methods for form fields for GenericForeignKey.

    ModelChoiceFieldMixin expects options to look like::

        <option value="4">Model #4</option>

    With a ContentType of id 3 for that model, it becomes::

        <option value="3-4">Model #4</option>
    """

    def prepare_value(self, value):
        """Return a ctypeid-objpk string for value."""
        if not value:
            return ''

        if isinstance(value, six.string_types):
            # Apparently Django's ModelChoiceField also expects two kinds of
            # "value" to be passed in this method.
            return value

        return '%s-%s' % (ContentType.objects.get_for_model(value).pk,
                          value.pk)


class ContentTypeModelMultipleFieldMixin(ContentTypeModelFieldMixin):
    """Same as ContentTypeModelFieldMixin, but supports value list."""

    def prepare_value(self, value):
        """Run the parent's method for each value."""
        if not value:  # ModelMultipleChoiceField does it too
            return []

        return [
            super(ContentTypeModelMultipleFieldMixin, self).prepare_value(v)
            for v in value
        ]


class GenericModelMixin(ContentTypeModelFieldMixin):
    """GenericForeignKey support for form fields, with FutureModelForm.

    GenericForeignKey enforce editable=false, this class implements
    save_object_data() and value_from_object() to allow FutureModelForm to
    compensate.
    """

    def save_object_data(self, instance, name, value):
        """Set the attribute, for FutureModelForm."""
        setattr(instance, name, value)

    def value_from_object(self, instance, name):
        """Get the attribute, for FutureModelForm."""
        return getattr(instance, name)
