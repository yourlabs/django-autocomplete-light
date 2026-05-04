from django.contrib.auth.models import Group

from dal import autocomplete
from dal_alight_queryset_sequence.views import AlightQuerySetSequenceView
from dal_alight_queryset_sequence.widgets import QuerySetSequenceAlight

from .models import TModel


class TForm(autocomplete.FutureModelForm):
    test = autocomplete.AlightGenericForeignKeyModelField(
        model_choice=[
            (Group, 'name'),
            (TModel, 'name', [('name', 'name')])
        ],  # Model with values to filter

        required=False,
        field_id='test',
    )

    test2 = autocomplete.GenericForeignKeyModelField(
        model_choice=[(Group,), (TModel,)],
        required=False,
        widget=QuerySetSequenceAlight,
        view=AlightQuerySetSequenceView,
    )

    class Meta:
        model = TModel
        fields = ('name',)
