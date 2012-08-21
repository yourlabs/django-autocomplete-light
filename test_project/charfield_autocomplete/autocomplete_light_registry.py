import autocomplete_light


class CityListAutocompleteMixin:
    limit_choices = 3

    choices = (
        'Paris',
        'London',
        'Mexico',
        'Cairo',
        'Washington',
        'Madrid',
        'Marseilles',
        'Olso',
        )

    def choices_for_request(self):
        return [x for x in self.choices if x.find(
            self.request.GET.get('q', '')
        ) > -1]


class CityListAutocompleteStrict(
    CityListAutocompleteMixin, autocomplete_light.AutocompleteListBase):
    pass

autocomplete_light.register(CityListAutocompleteStrict)


class CityListAutocompleteLoose(
    CityListAutocompleteMixin, autocomplete_light.AutocompleteBase):
    # XXX: TODO: this doesn't work currently, as the self.values is None when
    # the user input is not in self.choices (=> when the value attribute was
    # not set by the Javascript).

    def validate_values(self):
        return True
    pass

autocomplete_light.register(CityListAutocompleteLoose)




