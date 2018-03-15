"""View for a Select2 widget and QuerySetSequence-based business logic."""
from collections import OrderedDict

from dal_queryset_sequence.views import BaseQuerySetSequenceView

from dal_select2.views import Select2ViewMixin
from queryset_sequence import QuerySetSequence

from django.template.defaultfilters import capfirst
from django.utils import six


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
    Filter the queryset based on the models and filter attributes of the GenericForeignKeyModelField
    self.model_choice is generated from the GenericForeignKeyModelField
    """
    def get_queryset(self):
        queryset_models = []
        if self.q:
            for model, filter_value in self.model_choice:
                kwargs = {'{}__icontains'.format(filter_value): self.q}
                queryset_models.append(model.objects.filter(**kwargs))
        else:
            queryset_models = [model[0].objects.all() for model in self.model_choice]

        # Aggregate querysets
        qs = QuerySetSequence(*queryset_models)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs
