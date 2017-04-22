"""View for a Select2 widget and QuerySetSequence-based business logic."""

from dal_queryset_sequence.views import BaseQuerySetSequenceView

from dal_select2.views import Select2ViewMixin

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
        groups = {}

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
