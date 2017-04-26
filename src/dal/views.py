"""Base views for autocomplete widgets."""

import json

from django import http
from django.contrib.auth import get_permission_codename
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.utils import six
from django.views.generic.list import BaseListView


class ViewMixin(object):
    """Common methods for autocomplete views.

    It is assumed this view will be used in conjunction with a Django
    :py:class:`View` based class that will that will implement OPTIONS.

    .. py:attribute:: forwarded

        Dict of field values that were forwarded from the form, may be used to
        filter autocompletion results based on the form state. See
        ``linked_data`` example for reference.

    .. py:attribute:: q

        Query string as typed by the user in the autocomplete field.
    """

    http_method_allowed = ('GET', 'POST')

    def dispatch(self, request, *args, **kwargs):
        """Set :py:attr:`forwarded` and :py:attr:`q`."""
        if request.method.upper() not in self.http_method_allowed:
            return HttpResponseNotAllowed(self.http_method_allowed)

        try:
            self.forwarded = json.loads(
                getattr(request, request.method).get('forward', '{}')
            )
        except ValueError:
            return HttpResponseBadRequest('Invalid JSON data')

        if not isinstance(self.forwarded, dict):
            return HttpResponseBadRequest('Not a JSON object')

        self.q = request.GET.get('q', '')
        return super(ViewMixin, self).dispatch(request, *args, **kwargs)


class BaseQuerySetView(ViewMixin, BaseListView):
    """Base view to get results from a QuerySet.

    .. py:attribute:: create_field

        Name of the field to use to create missing values. For example, if
        create_field='title', and the user types in "foo", then the
        autocomplete view will propose an option 'Create "foo"' if it can't
        find any value matching "foo". When the user does click 'Create "foo"',
        the autocomplete script should POST to this view to create the object
        and get back the newly created object id.
    """

    paginate_by = 10
    context_object_name = 'results'
    create_field = None

    def has_more(self, context):
        """For widgets that have infinite-scroll feature."""
        return context['page_obj'].has_next()

    def get_result_value(self, result):
        """Return the value of a result."""
        return str(result.pk)

    def get_result_label(self, result):
        """Return the label of a result."""
        return six.text_type(result)

    def get_queryset(self):
        """Filter the queryset with GET['q']."""
        qs = super(BaseQuerySetView, self).get_queryset()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

    def create_object(self, text):
        """Create an object given a text."""
        return self.get_queryset().create(**{self.create_field: text})

    def has_add_permission(self, request):
        """Return True if the user has the permission to add a model."""
        if not request.user.is_authenticated():
            return False

        opts = self.get_queryset().model._meta
        codename = get_permission_codename('add', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def post(self, request):
        """Create an object given a text after checking permissions."""
        if not self.has_add_permission(request):
            return http.HttpResponseForbidden()

        if not self.create_field:
            raise ImproperlyConfigured('Missing "create_field"')

        text = request.POST.get('text', None)

        if text is None:
            return http.HttpResponseBadRequest()

        result = self.create_object(text)

        return http.JsonResponse({
            'id': result.pk,
            'text': six.text_type(result),
        })
