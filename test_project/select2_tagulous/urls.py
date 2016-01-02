from dal import autocomplete

from django.conf.urls import url

from .models import TestModel

urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            queryset=TestModel.test.tag_model.objects.all(),
        ),
        name='select2_tagulous',
    ),
]
