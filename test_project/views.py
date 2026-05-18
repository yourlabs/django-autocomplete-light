import operator
from functools import reduce

try:
    from django.contrib.auth.views import LoginView
except ImportError:  # old django, lol it
    from django.views.generic import TemplateView as LoginView

from django.contrib import admin
from django.db.models import Q
from django.forms.models import ModelChoiceIterator, ModelMultipleChoiceField
from django.http import HttpResponse, HttpResponseForbidden
from django.http.response import HttpResponse
from django.urls import NoReverseMatch, reverse, reverse_lazy
from django.utils.html import format_html
from django.views import View, generic
from select2_many_to_many.models import TModel

from dal import autocomplete


class LoginView(LoginView):
    template_name = 'login.html'


class IndexView(generic.TemplateView):
    template_name = 'base.html'


class AdminGlobalSearchView(View):
    """Global search across all admin-registered models for the topbar."""

    max_per_model = 5

    def get(self, request):
        if not request.user.is_staff:
            return HttpResponseForbidden()

        q = request.GET.get('q', '').strip()
        if len(q) < 2:
            return HttpResponse('', content_type='text/html; charset=utf-8')

        html = []
        for model, model_admin in sorted(
            admin.site._registry.items(),
            key=lambda x: x[0]._meta.verbose_name,
        ):
            app_label = model._meta.app_label
            model_name = model._meta.model_name

            search_fields = list(model_admin.search_fields) if model_admin.search_fields else []
            if not search_fields:
                for f in model._meta.fields:
                    if not f.primary_key and f.get_internal_type() in ('CharField', 'TextField'):
                        search_fields.append(f.name)
                        break

            if not search_fields:
                continue

            try:
                qs = model_admin.get_queryset(request)
                or_queries = [Q(**{'%s__icontains' % f: q}) for f in search_fields]
                qs = qs.filter(reduce(operator.or_, or_queries))[:self.max_per_model]

                for obj in qs:
                    try:
                        url = reverse(
                            'admin:%s_%s_change' % (app_label, model_name),
                            args=[obj.pk],
                        )
                    except NoReverseMatch:
                        continue
                    html.append(format_html(
                        '<div data-value="{}" data-url="{}">{}: {}</div>',
                        obj.pk,
                        url,
                        model._meta.verbose_name.capitalize(),
                        str(obj),
                    ))
            except Exception:
                continue

        return HttpResponse(''.join(html), content_type='text/html; charset=utf-8')


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
