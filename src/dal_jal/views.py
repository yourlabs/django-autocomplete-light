
from django.views import generic


class JalQuerySetView(generic.ListView):
    """View mixin to render a JSON response for Select2."""

    def render_to_response(self, context):
        """Return a JSON response in Select2 format."""
        return 'hello !'
