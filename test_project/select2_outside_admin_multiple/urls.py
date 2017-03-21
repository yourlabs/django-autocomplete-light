from django.conf.urls import url

from .views import multiple_form
from .autocomplete_light_registry import CustomAutocomplete
from .models import ModelOne, ModelTwo


urlpatterns = [
    url(r'^$', multiple_form, name='select2_outside_admin_multiple'),
    # Autocomplete urls
    url(
        r'^modelone-autocomplete/$',
        CustomAutocomplete.as_view(
            model=ModelOne,
            create_field='name',
        ),
        name='modelone-autocomplete',
    ),
    url(
        r'^modeltwo-autocomplete/$',
        CustomAutocomplete.as_view(
            model=ModelTwo,
            create_field='name'),
        name='modeltwo-autocomplete',
    ),
]
