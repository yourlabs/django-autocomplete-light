from django.contrib.auth.models import User
import autocomplete_light


class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ('username', 'email', 'first_name', 'last_name')

    autocomplete_js_attributes = {
        'placeholder': 'type a user name ...',
    }


autocomplete_light.register(User, UserAutocomplete)
