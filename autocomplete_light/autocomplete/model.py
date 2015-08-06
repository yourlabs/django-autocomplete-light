from __future__ import unicode_literals

import six
from django.db.models import Q
from django.utils.encoding import force_text
from django.db import connection

from ..settings import DEFAULT_SEARCH_FIELDS

__all__ = ('AutocompleteModel', )


class AutocompleteModel(object):
    """
    Autocomplete which considers choices as a queryset.

    .. py:attribute:: choices

        A queryset.

    .. py:attribute:: limit_choices

        Maximum number of choices to display.

    .. py:attribute:: search_fields

        Fields to search in, configurable like on
        :py:attr:`django:django.contrib.admin.ModelAdmin.search_fields`

    .. py:attribute:: split_words

        If True, AutocompleteModel splits the search query into words and
        returns all objects that contain each of the words, case insensitive,
        where each word must be in at least one of search_fields. This mimics
        the mechanism of django's
        :py:attr:`django:django.contrib.admin.ModelAdmin.search_fields`.

        If 'or', AutocompleteModel does the same but returns all objects that
        contain **any** of the words.

    .. py:attribute:: order_by

        If set, it will be used to order choices in the deck. It can be a
        single field name or an iterable (ie. list, tuple).
        However, if AutocompleteModel is instanciated with a list of values,
        it'll reproduce the ordering of values.
    """
    limit_choices = 20
    choices = None
    search_fields = DEFAULT_SEARCH_FIELDS
    split_words = False
    order_by = None

    def choice_value(self, choice):
        """
        Return the pk of the choice by default.
        """
        return choice.pk

    def choice_label(self, choice):
        """
        Return the textual representation of the choice by default.
        """
        return force_text(choice)

    def order_choices(self, choices):
        """
        Order choices using :py:attr:`order_by` option if it is set.
        """
        if isinstance(self.order_by, six.string_types):
            self.order_by = (self.order_by,)

        if self.values:
            pk_name = ('id' if not getattr(choices.model._meta, 'pk', None)
                    else choices.model._meta.pk.column)

            field = '"%s"."%s"' if connection.vendor == 'postgresql' \
                    else '%s.%s'
            pk_name = field % (choices.model._meta.db_table, pk_name)

            # Order in the user selection order when self.values is set.
            clauses = ' '.join(['WHEN %s=\'%s\' THEN %s' % (pk_name, pk, i)
                for i, pk in enumerate(self.values)])
            ordering = 'CASE %s END' % clauses

            _order_by = ('ordering',)
            if self.order_by:
                # safe concatenation of list/tuple
                # thanks lvh from #python@freenode
                _order_by = set(_order_by) | set(self.order_by)

            return choices.extra(
                select={'ordering': ordering},
                order_by=_order_by)

        if self.order_by is None:
            return choices

        return choices.order_by(*self.order_by)

    def choices_for_values(self):
        """
        Return ordered choices which pk are in
        :py:attr:`~.base.AutocompleteInterface.values`.
        """
        assert self.choices is not None, 'choices should be a queryset'
        return self.order_choices(self.choices.filter(
            pk__in=[x for x in self.values if x != '']))

    def choices_for_request(self):
        """
        Return a queryset based on :py:attr:`choices` using options
        :py:attr:`split_words`, :py:attr:`search_fields` and
        :py:attr:`limit_choices`.
        """
        assert self.choices is not None, 'choices should be a queryset'
        assert self.search_fields, 'autocomplete.search_fields must be set'
        assert not isinstance(self.search_fields, six.string_types), \
            'autocomplete.search_fields must not be a string'
        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude')

        conditions = self._choices_for_request_conditions(q,
                self.search_fields)

        return self.order_choices(self.choices.filter(
            conditions).exclude(pk__in=exclude))[0:self.limit_choices]

    def _construct_search(self, field_name):
        """
        Using a field name optionnaly prefixed by `^`, `=`, `@`, return a
        case-insensitive filter condition name usable as a queryset `filter()`
        keyword argument.
        """
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    def _choices_for_request_conditions(self, q, search_fields):
        """
        Return a `Q` object usable by `filter()` based on a list of fields to
        search in `search_fields` for string `q`.

        It uses options `split_words` and `search_fields` . Refer to the
        class-level documentation for documentation on each of these options.
        """
        conditions = Q()

        if self.split_words:
            for word in q.strip().split():
                word_conditions = Q()
                for search_field in search_fields:
                    word_conditions |= Q(**{
                        self._construct_search(search_field): word})

                if self.split_words == 'or':
                    conditions |= word_conditions
                else:
                    conditions &= word_conditions
        else:
            for search_field in search_fields:
                conditions |= Q(**{self._construct_search(search_field): q})

        return conditions

    def validate_values(self):
        """
        Return True if all values where found in :py:attr:`choices`.
        """
        return len(self.choices_for_values()) == len(self.values)
