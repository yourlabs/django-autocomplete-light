"""
Widgets for autocomplete-light and QuerySetSequence.

They combine :py:class:`~dal_alight.widgets.AlightWidgetMixin` and
:py:class:`~dal_queryset_sequence.widgets.QuerySetSequenceSelectMixin` with
Django's Select and SelectMultiple widgets, and are meant to be used with
generic model form fields such as those in :py:mod:`dal_contenttypes.fields`.
"""

from django import forms

from dal_alight.widgets import AlightInitialRenderMixin, AlightWidgetMixin
from dal_queryset_sequence.widgets import QuerySetSequenceSelectMixin


class QuerySetSequenceAlight(
    AlightInitialRenderMixin,
    QuerySetSequenceSelectMixin,
    AlightWidgetMixin,
    forms.Select,
):
    """Single-select autocomplete-light widget for QuerySetSequence."""

    def render(self, name, value, attrs=None, renderer=None):
        # AlightInitialRenderMixin uses pk__in which breaks on composite
        # ctype_pk-object_pk values. WidgetMixin.optgroups already calls
        # filter_choices_to_render which decodes composite values correctly.
        return super(AlightInitialRenderMixin, self).render(
            name, value, attrs=attrs, renderer=renderer
        )


class QuerySetSequenceAlightMultiple(
    AlightInitialRenderMixin,
    QuerySetSequenceSelectMixin,
    AlightWidgetMixin,
    forms.SelectMultiple,
):
    """Multi-select autocomplete-light widget for QuerySetSequence."""

    def render(self, name, value, attrs=None, renderer=None):
        return super(AlightInitialRenderMixin, self).render(
            name, value, attrs=attrs, renderer=renderer
        )
