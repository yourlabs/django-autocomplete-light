try:
    from django.contrib.auth.views import LoginView
except ImportError:  # old django, lol it
    from django.views.generic import TemplateView as LoginView
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'base.html'


class LoginView(LoginView):
    template_name = 'login.html'
