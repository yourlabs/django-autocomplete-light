from django import apps


class AppConfig(apps.AppConfig):
    name = 'dal_alight'
    verbose_name = 'Django-Autocomplete-Light'
    components = {
        'autocomplete-select': 'autocomplete-light/dist/autocomplete-light.js',
        'autocomplete-light': 'autocomplete-light/dist/autocomplete-light.js',
    }
