from django.contrib.auth.models import User
import autocomplete_light


class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Note that defining *_js_attributes in a Widget also works. Widget has
    # priority since it's the most specific.
    autocomplete_js_attributes = {
        'placeholder': 'type a user name ...',
    }


autocomplete_light.register(User, UserAutocomplete)
