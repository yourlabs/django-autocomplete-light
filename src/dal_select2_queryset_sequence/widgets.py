"""
Widgets for Select2 and QuerySetSequence.

They combine :py:class:`~dal_select2.widgets.Select2WidgetMixin` and
:py:class:`~dal_queryset_sequence.widgets.QuerySetSequenceSelectMixin` with
Django's Select and SelectMultiple widgets, and are meant to be used with
generic model form fields such as those in :py:mod:`dal_contenttypes.fields`.
"""

from dal_queryset_sequence.widgets import QuerySetSequenceSelectMixin

from dal_select2.widgets import Select2WidgetMixin

from django import forms


class QuerySetSequenceSelect2(Select2WidgetMixin,
                              QuerySetSequenceSelectMixin,
                              forms.Select):
    """Single model select for a generic select2 autocomplete."""


class QuerySetSequenceSelect2Multiple(Select2WidgetMixin,
                                      QuerySetSequenceSelectMixin,
                                      forms.SelectMultiple):
    """Multiple model select for a generic select2 autocomplete."""
