from django.conf.urls import url
from django.views.generic.base import TemplateView
from autocomplete_light.compat import urls, url

urlpatterns = urls([
    url(r'^$', TemplateView.as_view(template_name="bootstrap_modal/modal.html"), name="bootstrap_modal"),
])
