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

autocomplete_light.register(CityListAutocomplete)
