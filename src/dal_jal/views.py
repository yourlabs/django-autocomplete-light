
from django.views import generic


class JalQuerySetView(generic.ListView):
    """View mixin to render a JSON response for Select2."""
    template_name_suffix = '_autocomplete'
