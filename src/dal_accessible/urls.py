from django.urls import path
from django.views import generic


class AccessibleView(generic.FormView):
    template_name = 'form.html'


urlpatterns = [
    path('/', AccessibleView.as_view(), name='accessible')
]
