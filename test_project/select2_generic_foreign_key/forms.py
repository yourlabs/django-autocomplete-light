from dal import autocomplete

from django.contrib.auth.models import Group

from .models import TModel

from dal_select2_queryset_sequence.widgets import QuerySetSequenceSelect2
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView


class TForm(autocomplete.FutureModelForm):
    test = autocomplete.Select2GenericForeignKeyModelField(
        model_choice=[(Group, 'name'), (TModel, 'name')],  # Model with values to filter
        required=False,
    )

    test2 = autocomplete.GenericForeignKeyModelField(
        model_choice=[(Group, 'name'), (TModel, 'name')],  # Model with values to filter
        required=False,
        widget=QuerySetSequenceSelect2,
        view=Select2QuerySetSequenceView,
    )

    class Meta:
        model = TModel
        fields = ('name',)
