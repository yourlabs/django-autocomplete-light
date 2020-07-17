from dal import autocomplete

from django.conf.urls import url

from .forms import TForm


urlpatterns = TForm.as_urls()
