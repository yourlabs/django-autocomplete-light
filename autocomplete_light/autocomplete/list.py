__all__ = ('AutocompleteList',)


class AutocompleteList(object):
    limit_choices = 20
    order_by = lambda cls, choice: unicode(choice).lower()

    def choices_for_values(self):
        values_choices = []

        for choice in self.choices:
            if choice in self.values:
                values_choices.append(choice)

        return self.order_choices(values_choices)[0:self.limit_choices]

    def choices_for_request(self):
        assert self.choices, 'autocomplete.choices is not set'

        requests_choices = []
        q = self.request.GET.get('q', '').lower().strip()

        for choice in self.choices:
            if q in unicode(choice).lower():
                requests_choices.append(choice)

        return self.order_choices(requests_choices)[0:self.limit_choices]

    def order_choices(self, choices):
        return sorted(choices, key=self.order_by)
