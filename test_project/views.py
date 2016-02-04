import os

from django.views import generic

from docutils.core import publish_parts


class IndexView(generic.TemplateView):
    template_name = 'base.html'
