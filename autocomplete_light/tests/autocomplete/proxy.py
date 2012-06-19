import unittest

from django.contrib.auth.models import User

from cities_light.models import Country, Region, City
import autocomplete_light


class AutocompleteUser(autocomplete_light.AutocompleteModelProxyBase):
    choices = User.objects.all()


class AutocompleteProxyTest(unittest.TestCase):
    def test_model_dict_no_recreate_user(self):
        fixture = User.objects.get(pk=1)

        autocomplete = AutocompleteUser()
        text = autocomplete.choice_serialize(fixture)
        result = autocomplete.choice_unserialize(text)

        self.assertEqual(result, fixture.pk)
