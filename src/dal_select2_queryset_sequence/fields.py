from django.conf.urls import url

from dal_queryset_sequence.fields import QuerySetSequenceModelField

from queryset_sequence import QuerySetSequence

from dal_select2_queryset_sequence.widgets import QuerySetSequenceSelect2
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceAutoView


class Select2GenericForeignKeyModelField(QuerySetSequenceModelField):
    """
    Field that generate automatically the view for the QuerySetSequenceSelect2 widget
    """
    def __init__(self, *args, model_choice=None, field_id=None, **kwargs):
        """
        :param args:
        :param model_choice: [(Model, 'filter_by', [('forwardfield_name', 'filter_by')]), ],
        List of tuples, for each select2 widget. Model is the model to query, 'filter_by' the attribute of the model
        to apply the filter.
        The list in the tuple is optional, its to forward a field from the form to the widget.
        :param field_id: Optional name instead of the automatic one
        :param kwargs:
        """
        self.field_id = field_id if field_id else id(self)
        if model_choice:
            self.model_choice = model_choice
            models_queryset = [model[0].objects.all() for model in model_choice]
            kwargs['queryset'] = QuerySetSequence(*models_queryset)

        super().__init__(*args, **kwargs)

    def as_url(self, form):
        url_name = '{}_autocomp_{}'.format(form.__name__, self.field_id)

        forward_fields = {forward_tuple[0] for field in self.model_choice if len(field) > 2
                          for forward_tuple in field[2]}
        # a set of the fields to forward. it checks if the 3rd index of the list exists

        self.widget = QuerySetSequenceSelect2(url=url_name, forward=forward_fields)

        # generate the class to work with multiple gfk (can't work on instance level)
        AutoView = type('Autoview{}{}'.format(form.__name__, self.field_id),
                        (Select2QuerySetSequenceAutoView,),
                        {'model_choice': self.model_choice})  # send to the view the model and filter list

        return url(r'^{}_{}_autocomp$'.format(form.__name__, self.field_id),
                   AutoView.as_view(), name=url_name)
