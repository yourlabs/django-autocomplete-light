try:
    from django.contrib.auth.views import LoginView
except ImportError:  # old django, lol it
    from django.views.generic import TemplateView as LoginView

from django.forms.models import ModelChoiceIterator, ModelMultipleChoiceField
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from dal import autocomplete

from select2_many_to_many.models import TModel


class LoginView(LoginView):
    template_name = 'login.html'


class IndexView(generic.TemplateView):
    template_name = 'base.html'


def BasicDALView(request):
    """
    A very basic DAL widget alone on a page for minimalist testing. Not a
    dressed demo of what DAL can do, rather an isolated functional widget page
    against which comparisons can be made if someone has a DAL widget not
    working,

    This is the basic DAL (single selected) widget.
    """
    js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.js" crossorigin="anonymous"></script>
    """

    dal_media = autocomplete.Select2().media

    url = reverse_lazy('select2_many_to_many_autocomplete')
    field = ModelMultipleChoiceField(TModel.objects.all())

    widget = autocomplete.ModelSelect2(
        url=url,
        attrs={"class": "selector", "id": id, "data-placeholder": "Placeholder"})

    widget.choices = ModelChoiceIterator(field)

    default = None
    widget_html = widget.render(TModel.__name__, default)

    html = f"<head>{js}\n{dal_media}</head><body><p>{widget_html}</p></body>"

    return HttpResponse(html)


def BasicDALMultiView(request):
    """
    A very basic DAL widget alone on a page for minimalist testing. Not a dressed demo of what DAL can do,
    rather an isolated functional widget page against which comparisons can be made if someone has a DAL
    widget not working,

    This is the multi select DAL widget.
    """
    js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.js" crossorigin="anonymous"></script>
    """
    # <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/select2-bootstrap-theme/0.1.0-beta.10/select2-bootstrap.min.css" integrity="sha512-kq3FES+RuuGoBW3a9R2ELYKRywUEQv0wvPTItv3DSGqjpbNtGWVdvT8qwdKkqvPzT93jp8tSF4+oN4IeTEIlQA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    # <script>$.fn.select2.defaults.set( "theme", "bootstrap" );</script>
    # <script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.full.js" crossorigin="anonymous"></script>

    dal_media = autocomplete.Select2().media

    url = reverse_lazy('select2_many_to_many_autocomplete')
    field = ModelMultipleChoiceField(TModel.objects.all())

    widget = autocomplete.ModelSelect2Multiple(
        url=url, attrs={"class": "selector", "id": id, "data-placeholder": "Placeholder"})
    widget.choices = ModelChoiceIterator(field)

    default = None
    widget_html = widget.render(TModel.__name__, default)

    html = f"<head>{js}\n{dal_media}</head><body><p>{widget_html}</p></body>"

    return HttpResponse(html)
