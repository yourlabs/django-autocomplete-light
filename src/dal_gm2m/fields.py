"""GM2MField support for autocomplete fields."""


class GM2MFieldMixin(object):
    """GM2MField ror FutureModelForm."""

    def value_from_object(self, instance, name):
        """Return the list of objects in the GM2MField relation."""
        return None if not instance.pk else [
            x for x in getattr(instance, name).all()]

    def save_relation_data(self, instance, name, value):
        """Save the relation into the GM2MField."""
        setattr(instance, name, value)
