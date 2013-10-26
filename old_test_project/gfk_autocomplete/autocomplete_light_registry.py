import autocomplete_light
from cities_light.models import Country, City
from django.contrib.auth.models import User, Group


class AutocompleteTaggableItems(autocomplete_light.AutocompleteGenericBase):
    choices = (
        User.objects.all(),
        Group.objects.all(),
        City.objects.all(),
        Country.objects.all(),
    )

    search_fields = (
        ('username', 'email'),
        ('name',),
        ('search_names',),
        ('name_ascii',),
    )


autocomplete_light.register(AutocompleteTaggableItems)
