"""Autocomplete fields for QuerySetSequence choices."""
from dal_contenttypes.fields import (
    GenericModelMixin,
)


from django import forms
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist

from queryset_sequence import QuerySetSequence

import six


class QuerySetSequenceFieldMixin(object):
    """Base methods for QuerySetSequence fields."""

    def prepare_value(self, value):
        """Return a querysetid-objpk string for value.

        value must be an object sourced from a querysetsequence lookup,
        such that the querset index property ('#') is populated
        """
        if not value:
            return ''

        if not hasattr(value, '#'):
            return ''

        if isinstance(value, six.string_types):
            # Apparently Django's ModelChoiceField also expects two kinds of
            # "value" to be passed in this method.
            return value

        return '%s-%s' % (value.get('#'), value.pk)

    def raise_invalid_choice(self, params=None):
        """
        Raise a ValidationError for invalid_choice.

        The validation error left unprecise about the exact error for security
        reasons, to prevent an attacker doing information gathering to reverse
        valid queryset sequence id and object ids.
        """
        raise forms.ValidationError(
            self.error_messages['invalid_choice'],
            code='invalid_choice',
            params=params,
        )

    def get_queryset_index_object_id(self, value):
        """Return a tuple of queryset id, object id for value."""
        return value.split('-', 1)

    def get_model_for_queryset_index_object_id(self,
                                               queryset_index,
                                               object_id):
        """Return an object matching queryset_index and object_id."""
        return self.queryset.get(**{'#': queryset_index, 'id': object_id})


class QuerySetSequenceMultipleFieldMixin(QuerySetSequenceFieldMixin):
    """Same as ContentTypeModelFieldMixin, but supports value list."""

    def prepare_value(self, value):
        """Run the parent's method for each value."""
        if not value:  # ModelMultipleChoiceField does it too
            return []

        return [
            super(QuerySetSequenceMultipleFieldMixin, self).prepare_value(v)
            for v in value
        ]


class QuerySetSequenceModelField(GenericModelMixin,
                                 QuerySetSequenceFieldMixin,
                                 forms.ModelChoiceField):
    """Replacement for ModelChoiceField supporting QuerySetSequence choices."""

    def to_python(self, value):
        """
        Given a string like '3-5', return the model of queryset #3 and pk 5.

        Note that in the case of ModelChoiceField, to_python is also in charge
        of security, it's important to get the results from self.queryset.
        """
        if not value:
            return value

        queryset_index, object_id = self.get_queryset_index_object_id(value)
        try:
            return self.get_model_for_queryset_index_object_id(queryset_index,
                                                               object_id)
        except ObjectDoesNotExist:
            self.raise_invalid_choice()


class QuerySetSequenceModelMultipleField(QuerySetSequenceMultipleFieldMixin,
                                         forms.ModelMultipleChoiceField):
    """ModelMultipleChoiceField with support for QuerySetSequence choices."""

    def _deduplicate_values(self, value):
        # deduplicate given values to avoid creating many querysets or
        # requiring the database backend deduplicate efficiently.
        try:
            return frozenset(value)
        except TypeError:
            # list of lists isn't hashable, for example
            raise forms.ValidationError(
                self.error_messages['list'],
                code='list',
            )

    def _get_queryset_index_objects(self, values):
        pks = {}
        for val in values:
            queryset_index, object_id = self.get_queryset_index_object_id(val)

            pks.setdefault(queryset_index, [])
            pks[queryset_index].append(object_id)
        return pks

    def _get_queryset_for_pks(self, pks):
        querysets = []
        for queryset_index, object_ids in pks.items():

            querysets.append(self.queryset.filter(**{'#': queryset_index,
                                                     'pk__in': object_ids}))
        return QuerySetSequence(*querysets)

    def _check_values(self, value):
        values = self._deduplicate_values(value)
        pks = self._get_queryset_index_objects(values)
        queryset = self._get_queryset_for_pks(pks)

        fetched_values = [
            '%s-%s' % (o.get('#'), o.pk)
            for o in queryset
        ]

        for val in value:
            if val not in fetched_values:
                self.raise_invalid_choice(params={'value': val})

        return queryset


class GenericForeignKeyModelField(QuerySetSequenceModelField):
    """Field that generate automatically the view for compatible widgets."""

    def __init__(
        self, *args,
        model_choice=None, widget=None, view=None, field_id=None, **kwargs
    ):
        """Initialize GenericForeignKeyModelField."""
        self.field_id = field_id if field_id else id(self)
        if model_choice:
            self.model_choice = model_choice
            models_queryset = [model[0].objects.all()
                               for model in model_choice]
            kwargs['queryset'] = QuerySetSequence(*models_queryset)

        # check if they are classes
        if isinstance(widget, type) and isinstance(view, type):
            self.widget_obj = widget
            self.view_obj = view
        else:
            raise AttributeError(
                "Class object are required (not instantiated)")

        super().__init__(*args, **kwargs)

    def as_url(self, form):
        """Return url."""
        url_name = '{}_autocomp_{}'.format(form.__name__, self.field_id)

        self.widget = self.widget_obj(url=url_name)

        auto_view = type('Autoview{}{}'.format(form.__name__, self.field_id),
                         (self.view_obj,), {})
        return url(r'^{}_{}_autocomp$'.format(form.__name__, self.field_id),
                   auto_view.as_view(queryset=self.queryset), name=url_name)
