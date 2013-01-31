from django.db.models import Q

__all__ = ('AutocompleteModel', )


class AutocompleteModel(object):
    limit_choices = 20
    choices = None
    search_fields = None

    def choice_value(self, choice):
        return choice.pk

    def choice_label(self, choice):
        return unicode(choice)

    def order_choices(self, choices):
        order_by = getattr(self, 'order_by', None)
        if order_by:
            return choices.order_by(order_by)
        return choices

    def choices_for_values(self):
        assert self.choices is not None, 'choices should be a queryset'
        return self.order_choices(self.choices.filter(
            pk__in=self.values or []))

    def choices_for_request(self):
        assert self.choices is not None, 'choices should be a queryset'
        assert self.search_fields, 'autocomplete.search_fields must be set'
        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude', [])

        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        conditions = Q()
        if q:
            for search_field in self.search_fields:
                conditions |= Q(**{construct_search(search_field): q})

        return self.order_choices(self.choices.filter(
            conditions).exclude(pk__in=exclude))[0:self.limit_choices]

    def validate_values(self):
        return len(self.choices_for_values()) == len(self.values)
