"""Base views for autocomplete widgets."""

import json

from django.utils import six
from django.views.generic.list import BaseListView


class ViewMixin(object):
    """Common methods for autocomplete views.

    .. py:attribute:: forwarded

        Dict of field values that were forwarded from the form, may be used to
        filter autocompletion results based on the form state. See
        ``linked_data`` example for reference.
    """

    def get(self, request, *args, **kwargs):
        """Wrap around get to set :py:attr:`forwarded`."""
        self.forwarded = json.loads(request.GET.get('forward', '{}'))
        self.q = request.GET.get('q', '')
        return super(ViewMixin, self).get(request, *args, **kwargs)


class BaseQuerySetView(ViewMixin, BaseListView):
    """Base view to get results from a QuerySet."""

    paginate_by = 10
    context_object_name = 'results'

    def has_more(self, context):
        """For widgets that have infinite-scroll feature."""
        return context['page_obj'].has_next()

    def get_result_value(self, result):
        """Return the value of a result."""
        return result.pk

    def get_result_label(self, result):
        """Return the label of a result."""
        return six.text_type(result)

    def get_queryset(self):
        """Filter the queryset with GET['q']."""
        qs = super(BaseQuerySetView, self).get_queryset()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class SmartViewMixin(ViewMixin):
    @classmethod
    def as_widget(cls, widget):
        return cls(widget=widget)

    @classmethod
    def as_field(cls, field):
        return cls(field=field)

    @classmethod
    def as_url(cls):
        return url(
            r'^%s/$' % cls.__name__,
            cls.as_view(),
            name=cls.__name__,
        )

    def clean(self, value):
        pass

    def render(self, name, value, attrs=None):
        pass

    def decompress(self, value):
        pass
