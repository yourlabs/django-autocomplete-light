"""Autocomplete fields for QuerySetSequence choices."""

from dal_contenttypes.fields import (
    ContentTypeModelMultipleFieldMixin,
    GenericModelMixin,
)

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.urls import re_path as url

from queryset_sequence import QuerySetSequence


class QuerySetSequenceFieldMixin(object):
    """Base methods for QuerySetSequence fields."""

    def get_queryset_for_content_type(self, content_type_id):
        """Return the QuerySet from the QuerySetSequence for a ctype."""
        content_type = ContentType.objects.get_for_id(content_type_id)

        for queryset in self.queryset.get_querysets():
            if queryset.model.__name__ == 'QuerySequenceModel':
                # django-queryset-sequence 0.7 support dynamically created
                # QuerySequenceModel which replaces the original model when it
                # patches the queryset since 6394e19
                model = queryset.model.__bases__[0]
            else:
                model = queryset.model

            if model == content_type.model_class():
                return queryset

    def raise_invalid_choice(self, params=None):
        """
        Raise a ValidationError for invalid_choice.

        The validation error left imprecise about the exact error for security
        reasons, to prevent an attacker doing information gathering to reverse
        valid content type and object ids.
        """
        raise forms.ValidationError(
            self.error_messages['invalid_choice'],
            code='invalid_choice',
            params=params,
        )

    def get_content_type_id_object_id(self, value):
        """Return a tuple of ctype id, object id for value."""
        return value.split('-', 1)


class QuerySetSequenceModelField(GenericModelMixin,
                                 QuerySetSequenceFieldMixin,
                                 forms.ModelChoiceField):
    """Replacement for ModelChoiceField supporting QuerySetSequence choices."""

    def to_python(self, value):
        """
        Given a string like '3-5', return the model of ctype #3 and pk 5.

        Note that in the case of ModelChoiceField, to_python is also in charge
        of security, it's important to get the results from self.queryset.
        """
        if not value:
            return value

        content_type_id, object_id = self.get_content_type_id_object_id(value)
        queryset = self.get_queryset_for_content_type(content_type_id)

        if queryset is None:
            self.raise_invalid_choice()

        try:
            return queryset.get(pk=object_id)
        except queryset.model.DoesNotExist:
            self.raise_invalid_choice()


class QuerySetSequenceModelMultipleField(ContentTypeModelMultipleFieldMixin,
                                         QuerySetSequenceFieldMixin,
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

    def _get_ctype_objects(self, values):
        pks = {}
        for val in values:
            content_type_id, object_id = self.get_content_type_id_object_id(
                val)

            pks.setdefault(content_type_id, [])
            pks[content_type_id].append(object_id)
        return pks

    def _get_queryset_for_pks(self, pks):
        querysets = []
        for content_type_id, object_ids in pks.items():
            queryset = self.get_queryset_for_content_type(content_type_id)

            if queryset is None:
                self.raise_invalid_choice(
                    params=dict(
                        value='%s-%s' % (content_type_id, object_ids[0])
                    )
                )

            querysets.append(queryset.filter(pk__in=object_ids))
        return QuerySetSequence(*querysets)

    def _check_values(self, value):
        values = self._deduplicate_values(value)
        pks = self._get_ctype_objects(values)
        queryset = self._get_queryset_for_pks(pks)

        fetched_values = [
            '%s-%s' % (ContentType.objects.get_for_model(o).pk, o.pk)
            for o in queryset
        ]

        for val in value:
            if val not in fetched_values:
                self.raise_invalid_choice(params={'value': val})

        return queryset


class GenericForeignKeyModelField(QuerySetSequenceModelField):
    """Field that generate automatically the view for compatible widgets."""

    def __init__(self, *args, **kwargs):
        """Initialize GenericForeignKeyModelField."""
        model_choice = kwargs.pop('model_choice', None)
        widget = kwargs.pop('widget', None)
        view = kwargs.pop('view', None)
        field_id = kwargs.pop('field_id', None)
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

        super(GenericForeignKeyModelField, self).__init__(*args, **kwargs)

    def as_url(self, form):
        """Return url."""
        url_name = '{}_autocomp_{}'.format(form.__name__, self.field_id)

        self.widget = self.widget_obj(url=url_name)

        auto_view = type('Autoview{}{}'.format(form.__name__, self.field_id),
                         (self.view_obj,), {})
        return url(r'^{}_{}_autocomp$'.format(form.__name__, self.field_id),
                   auto_view.as_view(queryset=self.queryset), name=url_name)
