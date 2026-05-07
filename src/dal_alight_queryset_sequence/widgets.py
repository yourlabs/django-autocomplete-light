"""
Widgets for autocomplete-light and QuerySetSequence.

They combine :py:class:`~dal_alight.widgets.AlightWidgetMixin` and
:py:class:`~dal_queryset_sequence.widgets.QuerySetSequenceSelectMixin` with
Django's Select and SelectMultiple widgets, and are meant to be used with
generic model form fields such as those in :py:mod:`dal_contenttypes.fields`.
"""

from django import forms

from dal_alight.widgets import AlightWidgetMixin
from dal_queryset_sequence.widgets import QuerySetSequenceSelectMixin

# AlightInitialRenderMixin is intentionally NOT included: it filters
# self.choices.queryset by pk__in=[…], which breaks on the composite
# "ctype_pk-object_pk" values used by dal_queryset_sequence.
# WidgetMixin.optgroups() → filter_choices_to_render() decodes them correctly.


class QuerySetSequenceAlight(
    QuerySetSequenceSelectMixin,
    AlightWidgetMixin,
    forms.Select,
):
    """Single-select autocomplete-light widget for QuerySetSequence."""


class QuerySetSequenceAlightMultiple(
    QuerySetSequenceSelectMixin,
    AlightWidgetMixin,
    forms.SelectMultiple,
):
    """Multi-select autocomplete-light widget for QuerySetSequence."""
