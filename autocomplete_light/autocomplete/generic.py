from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from autocomplete_light.generic import GenericModelChoiceField

from .model import AutocompleteModel

__all__ = ['AutocompleteGeneric']


class AutocompleteGeneric(AutocompleteModel):
    """
    Autocomplete which considers choices as a list of querysets. It inherits
    from AutocompleteModel so make sure that you've read the docs and
    docstrings for AutocompleteModel before using this class.

    choices
        A list of querysets.
    search_fields
        A list of lists of fields to search in, configurable like on
        ModelAdmin.search_fields. The first list of fields will be used for the
        first queryset in choices and so on.

    AutocompleteGeneric inherits from AutocompleteModel and supports
    `limit_choices` and `split_words` exactly like AutocompleteModel.

    However `order_by` is not supported (yet) in AutocompleteGeneric.
    """
    choices = None
    search_fields = None

    def choice_value(self, choice):
        """
        Rely on GenericModelChoiceField to return a string containing the
        content type id and object id of the result.

        Because this autocomplete is made for that field, and to avoid code
        duplication.
        """
        field = GenericModelChoiceField()
        return field.prepare_value(choice)

    def validate_values(self):
        """
        Ensure that every choice is part of a queryset.
        """
        assert self.choices, 'autocomplete.choices should be a queryset list'

        for value in self.values:
            if not isinstance(value, basestring):
                return False

            try:
                content_type_id, object_id = value.split('-', 1)
            except ValueError:
                return False

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
        Propose local results and fill the autocomplete with remote
        suggestions.
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
        Values which are not found in the querysets are ignored.
        """
        values_choices = []

        for queryset in self.choices:
            ctype = ContentType.objects.get_for_model(queryset.model).pk

            try:
                ids = [x.split('-')[1] for x in self.values
                    if x is not None and int(x.split('-')[0]) == ctype]
            except ValueError:
                continue

            for choice in queryset.filter(pk__in=ids):
                values_choices.append(choice)

        return values_choices
