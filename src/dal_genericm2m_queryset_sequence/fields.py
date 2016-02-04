"""Autocomplete fields for django-queryset-sequence and django-generic-m2m."""

from dal_genericm2m.fields import GenericM2MFieldMixin

from dal_queryset_sequence.fields import QuerySetSequenceModelMultipleField


class GenericM2MQuerySetSequenceField(GenericM2MFieldMixin,
                                      QuerySetSequenceModelMultipleField):
    """Autocomplete field for GM2MField() for QuerySetSequence choices."""
