from dal import autocomplete

from django.urls import re_path as url

from .models import TModel


urlpatterns = [TModel.test.djhacker_kwargs.field.as_url()]
