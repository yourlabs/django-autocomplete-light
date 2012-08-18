import autocomplete_light


class CityListAutocomplete(autocomplete_light.AutocompleteListBase):
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


autocomplete_light.register(CityListAutocomplete)
