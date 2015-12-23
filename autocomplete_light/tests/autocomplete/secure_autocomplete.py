from autocomplete_light import shortcuts as al

from autocomplete_light.example_apps.security_test.models import Item


class SecureAutocomplete(al.AutocompleteModelBase):
    # We need to have all items by default for Field.clean() to be able to get
    # a value out for field.validate()
    choices = Item.objects.all()

    # BIGFATWARNING
    # A typo in this method name would mean that the default, open-to-all,
    # choices_for_request() method would be called instead.
    def choices_for_request(self):
        if getattr(self, 'request', None):
            user = getattr(self.request, 'user', None)

            if user and user.pk:
                return Item.objects.filter(owner=user)

        return Item.objects.none()
