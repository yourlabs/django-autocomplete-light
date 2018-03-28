from django.conf.urls import url

from dal_queryset_sequence.fields import QuerySetSequenceModelField

from queryset_sequence import QuerySetSequence

from dal_select2_queryset_sequence.widgets import QuerySetSequenceSelect2
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceAutoView


class Select2GenericForeignKeyModelField(QuerySetSequenceModelField):
    """
    Field that generate automatically the view for the QuerySetSequenceSelect2 widget
    """
    def __init__(self, *args, model_choice=None, **kwargs):
        if model_choice:
            self.model_choice = model_choice
            models_queryset = [model[0].objects.all() for model in model_choice]
            kwargs['queryset'] = QuerySetSequence(*models_queryset)

        super().__init__(*args, **kwargs)

    def as_url(self, form):
        url_name = '{}_autocomp_{}'.format(form.__name__, id(self))

        self.widget = QuerySetSequenceSelect2(url_name)

        # generate the class to work with multiple gfk (can't work on instance level)
        AutoView = type('Autoview{}{}'.format(form.__name__, id(self)),
                        (Select2QuerySetSequenceAutoView,),
                        {'model_choice': self.model_choice})  # send to the view the model and filter list

        return url(r'^{}_{}_autocomp$'.format(form.__name__, id(self)),
                   AutoView.as_view(), name=url_name)
