from __future__ import unicode_literals

from autocomplete_light.fields import GenericModelChoiceField
import six

from ..settings import DEFAULT_SEARCH_FIELDS
from .model import AutocompleteModel

__all__ = ['AutocompleteGeneric']


class AutocompleteGenericMetaClass(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(AutocompleteGenericMetaClass, cls).__new__(cls, name,
                bases, attrs)

        if attrs.get('__module__',
                '').startswith('autocomplete_light.autocomplete'):
            # We are defining one of our own classes.
            return new_class

        if not new_class.search_fields:
            default = DEFAULT_SEARCH_FIELDS
            new_class.search_fields = [default] * len(new_class.choices)

        return new_class


class AutocompleteGeneric(six.with_metaclass(AutocompleteGenericMetaClass,
        AutocompleteModel)):
    """
    :py:class:`~.model.AutocompleteModel` extension which considers choices as
    a **list of querysets**, and composes a choice value with both the content
    type pk and the actual model pk.

    .. py:attribute:: choices

        A list of querysets. Example::

            choices = (
                User.objects.all(),
                Group.objects.all(),
            )

    .. py:attribute:: search_fields

        A list of lists of fields to search in, configurable like on
        ModelAdmin.search_fields. The first list of fields will be used for the
        first queryset in choices and so on. Example::

            search_fields = (
                ('email', '^name'),  # Used for User.objects.all()
                ('name',)            # User for Group.objects.all()
            )

    AutocompleteGeneric inherits from :py:class:`.model.AutocompleteModel` and
    supports :py:attr:`~.model.AutocompleteModel.limit_choices` and
    :py:attr:`~.model.AutocompleteModel.split_words` exactly like
    AutocompleteModel.

    However :py:attr:`~.model.AutocompleteModel.order_by` is not supported
    (yet) in AutocompleteGeneric.
    """
    choices = None
    search_fields = None

    def choice_value(self, choice):
        """
        Rely on :py:class:`~autocomplete_light.generic.GenericModelChoiceField`
        to return a string containing the content type id and object id of the
        result.
        """
        field = GenericModelChoiceField()
        return field.prepare_value(choice)

    def validate_values(self):
        """
        Ensure that every choice is part of a queryset in :py:attr:`choices`.
        """
        assert self.choices, 'autocomplete.choices should be a queryset list'

        for value in self.values:
            if not isinstance(value, six.string_types):
                return False

            try:
                content_type_id, object_id = value.split('-', 1)
            except ValueError:
                return False

            from django.contrib.contenttypes.models import ContentType
            try:
                content_type = ContentType.objects.get_for_id(content_type_id)
            except ContentType.DoesNotExist:
                return False

            model_class = content_type.model_class()

            found = False
            for queryset in self.choices:
                if queryset.model != model_class:
                    continue

                if queryset.filter(pk=object_id).count() == 1:
                    found = True
                else:
                    return False

            if not found:
                # maybe a user would cheat by using a forbidden ctype id !
                return False

        return True

    def choices_for_request(self):
        """
        Return a list of choices from every queryset in :py:attr:`choices`.
        """
        assert self.choices, 'autocomplete.choices should be a queryset list'

        q = self.request.GET.get('q', '')

        request_choices = []
        querysets_left = len(self.choices)

        i = 0
        for queryset in self.choices:
            conditions = self._choices_for_request_conditions(q,
                    self.search_fields[i])

            limit = ((self.limit_choices - len(request_choices)) /
                querysets_left)
            for choice in queryset.filter(conditions)[:limit]:
                request_choices.append(choice)

            querysets_left -= 1
            i += 1

        return request_choices

    def choices_for_values(self):
        """
        Values which are not found in any querysets of :py:attr:`choices` are
        ignored.
        """
        values_choices = []

        for queryset in self.choices:
            from django.contrib.contenttypes.models import ContentType
            ctype = ContentType.objects.get_for_model(queryset.model).pk

            try:
                ids = [x.split('-')[1] for x in self.values
                    if x is not None and int(x.split('-')[0]) == ctype]
            except ValueError:
                continue

            for choice in queryset.filter(pk__in=ids):
                values_choices.append(choice)

        return values_choices
