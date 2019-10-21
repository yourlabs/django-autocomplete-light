"""View for a Select2 widget and QuerySetSequence-based business logic."""
from collections import OrderedDict
from functools import reduce

from dal_queryset_sequence.views import BaseQuerySetSequenceView

from dal_select2.views import Select2ViewMixin

from django.db.models import Q
from django.template.defaultfilters import capfirst

from queryset_sequence import QuerySetSequence

import six


class Select2QuerySetSequenceView(BaseQuerySetSequenceView, Select2ViewMixin):
    """
    Combines support QuerySetSequence and Select2 in a single view.

    Example usage::

        url(
            '^your-generic-autocomplete/$',
            autocomplete.Select2QuerySetSequenceView.as_view(
                queryset=autocomplete.QuerySetSequence(
                    Group.objects.all(),
                    TestModel.objects.all(),
                )
            ),
            name='your-generic-autocomplete',
        )

    It is compatible with the :py:mod:`~dal_select2_queryset_sequence.widgets`
    and the fields of :py:mod:`dal_contenttypes`, suits generic relation
    autocompletes.
    """

    def get_results(self, context):
        """
        Return a list of results usable by Select2.

        It will render as a list of one <optgroup> per different content type
        containing a list of one <option> per model.
        """
        groups = OrderedDict()

        for result in context['object_list']:
            groups.setdefault(type(result), [])
            groups[type(result)].append(result)

        return [{
            'id': None,
            'text': capfirst(self.get_model_name(model)),
            'children': [{
                'id': self.get_result_value(result),
                'text': six.text_type(result),
            } for result in results]
        } for model, results in groups.items()]


class Select2QuerySetSequenceAutoView(Select2QuerySetSequenceView):
    """
    Select2QuerySetSequenceAutoView class.

    Filter the queryset based on the models and filter attributes of the
    GenericForeignKeyModelField

    self.model_choice is generated from the Select2GenericForeignKeyModelField,
    see it's docstring
    """

    def get_queryset(self):
        """Return queryset."""
        queryset_models = []
        for model_args in self.model_choice:
            model = model_args[0]
            filter_value = model_args[1]

            kwargs_model = {
                '{}__icontains'.format(filter_value): self.q if self.q else ''
            }
            forward_filtered = [Q(**kwargs_model)]

            try:
                forward_fields = model_args[2]
                for forward in forward_fields:
                    field_key = '{}__icontains'.format(forward[1])
                    field_value = self.forwarded[forward[0]]
                    forward_filtered.append(Q(**{field_key: field_value}))
            except IndexError:
                # if no list on the 3rd index of self.model_choice
                # (reserved for forwarding fields)
                pass

            # link the diffrent field by an & query
            and_forward_filtered = reduce(lambda x, y: x & y, forward_filtered)

            queryset_models.append(model.objects.filter(and_forward_filtered))

        # Aggregate querysets
        qs = QuerySetSequence(*queryset_models)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
