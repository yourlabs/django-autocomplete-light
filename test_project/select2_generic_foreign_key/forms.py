from dal import autocomplete

from django.contrib.auth.models import Group

from .models import TModel


class TForm(autocomplete.FutureModelForm):
    test = autocomplete.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Group.objects.all(),
            TModel.objects.all(),
        ),
        required=False,
        widget=autocomplete.QuerySetSequenceSelect2('select2_gfk'),
    )

    class Meta:
        model = TModel
        fields = ('name',)
