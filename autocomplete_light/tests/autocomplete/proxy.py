import unittest

from django.contrib.auth.models import User

from cities_light.models import Country, Region, City
import autocomplete_light


class AutocompleteUser(autocomplete_light.AutocompleteModelProxyBase):
    choices = User.objects.all()


class AutocompleteCity(autocomplete_light.AutocompleteModelProxyBase):
    choices = City.objects.all()


class AutocompleteProxyTest(unittest.TestCase):
    def test_model_dict_no_recreate_user(self):
        fixture = User.objects.get(pk=1)

        autocomplete = AutocompleteUser()
        text = autocomplete.choice_serialize(fixture)
        result = autocomplete.choice_unserialize(text)

        self.assertEqual(result, fixture.pk)

    def test_model_dict_no_recreate_country(self):
        country, c = Country.objects.get_or_create(name=u'France')
        region, c = Region.objects.get_or_create(country=country,
            name='IDF')

        autocomplete = AutocompleteCity()
        text = autocomplete.choice_serialize(City(name='Paris',
            region=region, country=country))
        result = autocomplete.choice_unserialize(text)

        import ipdb; ipdb.set_trace()
