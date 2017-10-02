from django.contrib.auth.views import LoginView
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'base.html'


class LoginView(LoginView):
    template_name = 'login.html'
