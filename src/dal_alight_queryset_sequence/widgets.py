"""
Widgets for autocomplete-light and QuerySetSequence.

They combine :py:class:`~dal_alight.widgets.AlightWidgetMixin` and
:py:class:`~dal_queryset_sequence.widgets.QuerySetSequenceSelectMixin` with
Django's TextInput widget, and are meant to be used with generic model form
fields such as those in :py:mod:`dal_contenttypes.fields`.
"""

from django.contrib.admin.widgets import AdminTextInputWidget

from dal_alight.widgets import AlightChoiceMixin, AlightMultipleMixin, AlightWidgetMixin
from dal_queryset_sequence.widgets import QuerySetSequenceSelectMixin


class QuerySetSequenceAlight(
    QuerySetSequenceSelectMixin,
    AlightWidgetMixin,
    AlightChoiceMixin,
    AdminTextInputWidget,
):
    """Single-select autocomplete-light widget for QuerySetSequence."""


class QuerySetSequenceAlightMultiple(
    QuerySetSequenceSelectMixin,
    AlightWidgetMixin,
    AlightMultipleMixin,
    AlightChoiceMixin,
    AdminTextInputWidget,
):
    """Multi-select autocomplete-light widget for QuerySetSequence."""
