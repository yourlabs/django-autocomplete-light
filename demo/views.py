import os
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

import alight_foreign_key.models as fk_models
import alight_foreign_key.forms as fk_forms
import alight_many_to_many.models as m2m_models
import alight_many_to_many.forms as m2m_forms
import alight_linked_data.models as linked_models
import alight_linked_data.forms as linked_forms
import alight_list.models as list_models
import alight_list.forms as list_forms
import alight_tag.models as tag_models
import alight_tag.forms as tag_forms


def component_test(request):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'component_test.html')) as f:
        return HttpResponse(f.read())


INDEX_HTML = """
<!doctype html>
<html>
<head><title>dal_alight demo</title></head>
<body>
<h1>dal_alight Demo</h1>
<p>No <code>dal_select2</code> used anywhere — pure web-component autocomplete.</p>
<ul>
  <li><a href="/fk/new/">Foreign Key autocomplete (ModelAlight)</a></li>
  <li><a href="/m2m/new/">Many-to-Many autocomplete with create (ModelAlightMultiple)</a></li>
  <li><a href="/linked/new/">Forward / linked-data autocomplete</a></li>
  <li><a href="/list/new/">List autocomplete with create (ListAlight)</a></li>
  <li><a href="/tag/new/">Tag autocomplete with free-text create (TagAlight)</a></li>
  <li><a href="/admin/">Django admin (all features registered)</a></li>
</ul>
<h2>How to use</h2>
<ol>
  <li>Create a superuser: <code>python manage.py createsuperuser</code></li>
  <li>Start the server: <code>python manage.py runserver</code></li>
  <li>Visit <a href="/admin/">the admin</a> to pre-populate data, then try the
      standalone form pages above.</li>
</ol>
</body>
</html>
"""


def index(request):
    return HttpResponse(INDEX_HTML)


# ---- Foreign Key ----

class FKCreateView(CreateView):
    model = fk_models.TModel
    form_class = fk_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('fk_create')
    extra_context = {'title': 'FK autocomplete (ModelAlight)', 'list_url': '/fk/'}


class FKUpdateView(UpdateView):
    model = fk_models.TModel
    form_class = fk_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('fk_create')
    extra_context = {'title': 'FK autocomplete (ModelAlight)'}


# ---- Many-to-Many ----

class M2MCreateView(CreateView):
    model = m2m_models.TModel
    form_class = m2m_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('m2m_create')
    extra_context = {'title': 'M2M autocomplete with create (ModelAlightMultiple)'}


class M2MUpdateView(UpdateView):
    model = m2m_models.TModel
    form_class = m2m_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('m2m_create')
    extra_context = {'title': 'M2M autocomplete with create (ModelAlightMultiple)'}


# ---- Linked data (forward) ----

class LinkedCreateView(CreateView):
    model = linked_models.TModel
    form_class = linked_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('linked_create')
    extra_context = {'title': 'Forward / linked-data (group → member filter)'}


class LinkedUpdateView(UpdateView):
    model = linked_models.TModel
    form_class = linked_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('linked_create')
    extra_context = {'title': 'Forward / linked-data (group → member filter)'}


# ---- List ----

class ListCreateView(CreateView):
    model = list_models.TModel
    form_class = list_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('list_create')
    extra_context = {'title': 'List autocomplete with create (ListAlight)'}


class ListUpdateView(UpdateView):
    model = list_models.TModel
    form_class = list_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('list_create')
    extra_context = {'title': 'List autocomplete with create (ListAlight)'}


# ---- Tag ----

class TagCreateView(CreateView):
    model = tag_models.TModel
    form_class = tag_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('tag_create')
    extra_context = {'title': 'Tag autocomplete with free-text create (TagAlight)'}


class TagUpdateView(UpdateView):
    model = tag_models.TModel
    form_class = tag_forms.TForm
    template_name = 'demo_form.html'
    success_url = reverse_lazy('tag_create')
    extra_context = {'title': 'Tag autocomplete with free-text create (TagAlight)'}
