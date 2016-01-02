"""Tagulous TagField support."""

from dal.fields import CreateModelMultipleField


class TagulousField(CreateModelMultipleField):
    """FutureModelForm support for tagulous TagField."""

    def value_from_object(self, instance, name):
        """Return a list of Tags for the TagField."""
        return None if not instance.pk else [
            x for x in getattr(instance, name).all()]
