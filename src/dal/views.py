"""Base views for autocomplete widgets."""

import json
import operator
from functools import reduce

import django
from django import http
if django.VERSION >= (4, 0):
    from django.contrib.admin.utils import lookup_spawns_duplicates
else:
    from django.contrib.admin.utils import lookup_needs_distinct \
        as lookup_spawns_duplicates
from django.contrib.auth import get_permission_codename
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import BaseListView


class ViewMixin(object):
    """Common methods for autocomplete views.

    It is assumed this view will be used in conjunction with a Django
    :py:class:`View` based class that will implement OPTIONS.

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

    .. py:attribute:: model_field_name

        Name of the Model field to run filter against.
    """

    paginate_by = 10
    context_object_name = 'results'
    model_field_name = 'name'
    create_field = None
    search_fields = []
    split_words = None
    template = None
    validate_create = None

    def has_more(self, context):
        """For widgets that have infinite-scroll feature."""
        return context['page_obj'].has_next() if context['page_obj'] else False

    def get_result_value(self, result):
        """Return the value of a result."""
        return str(result.pk)

    def get_result_label(self, result):
        """Return the label of a result."""
        if self.template:
            return render_to_string(self.template, {"result": result})
        else:
            return str(result)

    def get_selected_result_label(self, result):
        """Return the label of a selected result."""
        return self.get_result_label(result)

    def get_queryset(self):
        """Filter the queryset with GET['q']."""
        qs = super(BaseQuerySetView, self).get_queryset()

        qs = self.get_search_results(qs, self.q)

        return qs

    def get_search_fields(self):
        """Get the fields to search over."""
        if self.search_fields:
            return self.search_fields
        else:
            return [self.model_field_name]

    def _construct_search(self, field_name):
        """Apply keyword searches."""
        if field_name.startswith("^"):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith("="):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith("@"):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    def get_search_results(self, queryset, search_term):
        """Filter the results based on the query."""
        search_fields = self.get_search_fields()
        if search_fields and search_term:
            orm_lookups = [
                self._construct_search(search_field) for search_field in search_fields
            ]
            if self.split_words is not None:
                word_conditions = []
                for word in search_term.split():
                    or_queries = [Q(**{orm_lookup: word}) for orm_lookup in orm_lookups]
                    word_conditions.append(reduce(operator.or_, or_queries))
                op_ = operator.or_ if self.split_words == "or" else operator.and_
                queryset = queryset.filter(reduce(op_, word_conditions))
            else:
                or_queries = [
                    Q(**{orm_lookup: search_term}) for orm_lookup in orm_lookups
                ]
                queryset = queryset.filter(reduce(operator.or_, or_queries))

            if self.lookup_needs_distinct(queryset, orm_lookups):
                queryset = queryset.distinct()

        return queryset

    def lookup_needs_distinct(self, queryset, orm_lookups):
        """Return True if an orm_lookup requires calling qs.distinct()."""
        return any(
            lookup_spawns_duplicates(queryset.model._meta, search_spec)
            for search_spec in orm_lookups
        )

    def create_object(self, text):
        """Create an object given a text."""
        return self.get_queryset().get_or_create(
            **{self.create_field: text})[0]

    def has_add_permission(self, request):
        """Return True if the user has the permission to add a model."""
        if django.VERSION < (2, 0, 0):
            auth = request.user.is_authenticated()
        else:
            auth = request.user.is_authenticated

        if not auth:
            return False

        opts = self.get_queryset().model._meta
        codename = get_permission_codename('add', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def post(self, request, *args, **kwargs):
        """
        Create an object given a text after checking permissions.

        Runs self.validate() if self.validate_create is True.
        """
        if not self.has_add_permission(request):
            return http.HttpResponseForbidden()

        if not self.create_field:
            raise ImproperlyConfigured('Missing "create_field"')

        text = request.POST.get('text', None)

        if text is None:
            return http.HttpResponseBadRequest()

        if self.validate_create:
            try:
                self.validate(text)
            except ValidationError as error:
                if self.create_field in error.message_dict:
                    return http.JsonResponse(dict(error=error.message_dict.get(self.create_field, _('Error'))))

        result = self.create_object(text)

        return http.JsonResponse({
            'id': self.get_result_value(result),
            'text': self.get_selected_result_label(result),
        })

    def validate(self, text):
        """
        Validate a given text for new option creation.

        Raise ValidationError or return None.
        """
        model = self.get_queryset().model
        obj = model(**{self.create_field: text})
        obj.full_clean()
