from .list import AutocompleteList

__all__ = ('AutocompleteChoiceList',)


class AutocompleteChoiceList(AutocompleteList):
    order_by = lambda cls, choice: unicode(choice[1]).lower()

    def choices_for_values(self):
        values_choices = []

        for choice in self.choices:
            if choice[0] in self.values:
                values_choices.append(choice)

        return self.order_choices(values_choices)[0:self.limit_choices]

    def choices_for_request(self):
        requests_choices = []
        q = self.request.GET.get('q', '').lower().strip()

        for choice in self.choices:
            if q in unicode(choice[0]).lower() + unicode(choice[1]).lower():
                requests_choices.append(choice)

        return self.order_choices(requests_choices)[0:self.limit_choices]

    def choice_value(self, choice):
        return choice[0]

    def choice_label(self, choice):
        return choice[1]
