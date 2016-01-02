"""django-generic-m2m field mixin for FutureModelForm."""


class GenericM2MFieldMixin(object):
    """Form field mixin able to get / set instance generic-m2m relations."""

    def value_from_object(self, instance, name):
        """Return the list of related objects."""
        return [x.object for x in getattr(instance, name).all()]

    def save_relation_data(self, instance, name, value):
        """Update the relation to be ``value``."""
        instance_field = getattr(instance, name)

        for related in instance_field.all():
            if related.object not in value:
                instance_field.remove(related)

        for related in value:
            instance_field.connect(related)
