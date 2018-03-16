from dal import autocomplete

from django.contrib.auth.models import Group

from .models import TModel


class TForm(autocomplete.FutureModelForm):
    test = autocomplete.GenericForeignKeyModelField(
        model_choice=[(Group, 'name'), (TModel, 'name')],  # Model with values to filter
        required=False,
    )

    test2 = autocomplete.GenericForeignKeyModelField(
        model_choice=[(Group, 'name'), (TModel, 'name')],  # Model with values to filter
        required=False,
    )

    class Meta:
        model = TModel
        fields = ('name',)
