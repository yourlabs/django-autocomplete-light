"""
Widgets for autocomplete-light and QuerySetSequence.

They combine :py:class:`~dal_alight.widgets.AlightWidgetMixin` and
:py:class:`~dal_queryset_sequence.widgets.QuerySetSequenceSelectMixin` with
Django's TextInput widget, and are meant to be used with generic model form
fields such as those in :py:mod:`dal_contenttypes.fields`.
"""

from django import forms

from dal_alight.widgets import AlightChoiceMixin, AlightMultipleMixin, AlightWidgetMixin
from dal_queryset_sequence.widgets import QuerySetSequenceSelectMixin


class QuerySetSequenceAlight(
    AlightWidgetMixin,
    QuerySetSequenceSelectMixin,
    AlightChoiceMixin,
    forms.TextInput,
):
    """Single-select autocomplete-light widget for QuerySetSequence."""


class QuerySetSequenceAlightMultiple(
    AlightWidgetMixin,
    QuerySetSequenceSelectMixin,
    AlightMultipleMixin,
    AlightChoiceMixin,
    forms.TextInput,
):
    """Multi-select autocomplete-light widget for QuerySetSequence."""
