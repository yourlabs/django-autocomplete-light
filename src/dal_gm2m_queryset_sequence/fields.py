"""Form fields for using django-gm2m with QuerySetSequence."""

from dal_gm2m.fields import GM2MFieldMixin

from dal_queryset_sequence.fields import QuerySetSequenceModelMultipleField


class GM2MQuerySetSequenceField(GM2MFieldMixin,
                                QuerySetSequenceModelMultipleField):
    """Form field for QuerySetSequence to django-generic-m2m relation."""
