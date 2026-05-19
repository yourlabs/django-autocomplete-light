"""Views for autocomplete-light widget and QuerySetSequence-based business logic."""

from collections import OrderedDict
from functools import reduce

from django import http
from django.db.models import Q
from django.utils.html import format_html
from queryset_sequence import QuerySetSequence

from dal_queryset_sequence.views import BaseQuerySetSequenceView


class AlightQuerySetSequenceView(BaseQuerySetSequenceView):
    """
    Combines QuerySetSequence support with autocomplete-light HTML fragments.

    Returns results grouped by model type, rendered as HTML divs instead of
    JSON.  Group headers use ``class="autocomplete-light-group"``; individual
    results carry a ``data-value`` attribute with the ``ctype_pk-object_pk``
    composite identifier used by ``dal_queryset_sequence``.

    Example usage::

        path(
            'your-generic-autocomplete/',
            autocomplete.AlightQuerySetSequenceView.as_view(
                queryset=autocomplete.QuerySetSequence(
                    Group.objects.all(),
                    TestModel.objects.all(),
                )
            ),
            name='your-generic-autocomplete',
        )

    Compatible with :py:mod:`~dal_alight_queryset_sequence.widgets` and the
    fields of :py:mod:`~dal_contenttypes.fields` for generic-relation
    autocompletes.
    """

    def render_to_response(self, context):
        """Return an HTML fragment grouped by model type."""
        groups = OrderedDict()
        for result in context['object_list']:
            groups.setdefault(type(result), []).append(result)

        html = []
        for model, results in groups.items():
            verbose_name = model._meta.verbose_name
            html.append(format_html(
                '<div class="autocomplete-light-group">{}</div>',
                verbose_name,
            ))
            for result in results:
                html.append(format_html(
                    '<div data-value="{}">{}</div>',
                    self.get_result_value(result),
                    str(result),
                ))

        return http.HttpResponse(
            ''.join(html),
            content_type='text/html; charset=utf-8',
        )


class AlightQuerySetSequenceAutoView(AlightQuerySetSequenceView):
    """
    AlightQuerySetSequenceAutoView class.

    Filters the queryset based on the models and filter attributes defined on
    an :py:class:`AlightGenericForeignKeyModelField
    <dal_alight_queryset_sequence.fields.AlightGenericForeignKeyModelField>`.

    ``self.model_choice`` is generated from that field; see its docstring for
    the expected structure.
    """

    def get_queryset(self):
        """Return queryset filtered according to self.model_choice."""
        queryset_models = []
        for model_args in self.model_choice:
            model = model_args[0]
            filter_value = model_args[1]

            kwargs_model = {
                '{}__icontains'.format(filter_value): self.q if self.q else ''
            }
            forward_filtered = [Q(**kwargs_model)]

            for forward in model_args[2] if len(model_args) > 2 else []:
                field_value = self.forwarded.get(forward[0])
                if field_value is None:
                    continue
                field_key = '{}__icontains'.format(forward[1])
                forward_filtered.append(Q(**{field_key: field_value}))

            # Combine filters with AND.
            and_forward_filtered = reduce(lambda x, y: x & y, forward_filtered)
            queryset_models.append(model.objects.filter(and_forward_filtered))

        # Aggregate querysets and limit each to an equal share of the page.
        qs = QuerySetSequence(*queryset_models)
        qs = self.mixup_querysets(qs)
        return qs
