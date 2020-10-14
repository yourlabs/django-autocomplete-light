"""
Widget mixin that only renders selected options with QuerySetSequence.

For details about why this is required, see :mod:`dal.widgets`.
"""

from dal.widgets import WidgetMixin

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text


class QuerySetSequenceSelectMixin(WidgetMixin):
    """Support QuerySetSequence in WidgetMixin."""

    def label_from_instance(self, obj):
        """Convert an object into string. Override it to customize display."""
        return force_text(obj)

    def filter_choices_to_render(self, selected_choices):
        """Overwrite self.choices to exclude unselected values."""
        if len(selected_choices) == 1 and not selected_choices[0]:
            selected_choices = []

        ctype_models = {}

        for choice in selected_choices:
            ctype_pk, model_pk = choice.split('-', 1)
            ctype_pk = int(ctype_pk)
            ctype_models.setdefault(ctype_pk, [])
            ctype_models[ctype_pk].append(model_pk)

        self.choices = []
        ctype = ContentType.objects.get_for_id
        for ctype_pk, ids in ctype_models.items():
            results = ctype(ctype_pk).model_class().objects.filter(pk__in=ids)

            self.choices += [
                ('%s-%s' % (ctype_pk, r.pk), self.label_from_instance(r))
                for r in results
            ]


class QuerySetSequenceSelect(QuerySetSequenceSelectMixin,
                             forms.Select):
    """Select widget for QuerySetSequence choices."""


class QuerySetSequenceSelectMultiple(QuerySetSequenceSelectMixin,
                                     forms.SelectMultiple):
    """SelectMultiple widget for QuerySetSequence choices."""
