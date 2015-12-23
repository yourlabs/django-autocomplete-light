from django import test
from django import forms

from autocomplete_light import shortcuts as al
from autocomplete_light.example_apps.security_test.models import Item
from .secure_autocomplete import SecureAutocomplete
from .case import User


class SecureForm(forms.Form):
    item = al.ModelChoiceField(SecureAutocomplete)


class SecurityTest(test.TestCase):
    def setUp(self):
        self.owner = User.objects.create(username='owner')
        self.non_owner = User.objects.create(username='non_owner')
        self.item = Item.objects.create(name='secure item', owner=self.owner)
        self.request = test.RequestFactory().get('/')
        self.autocomplete = SecureAutocomplete(request=self.request)
        self.form = SecureForm({'item': self.item.pk})

        # Enable security switch
        self.form.fields['item'].request = self.request

    def test_no_user_cant_see_nor_saveitem(self):
        assert list(self.autocomplete.choices_for_request()) == []
        assert self.form.is_valid() is False

    def test_non_owner_cant_see_item(self):
        self.request.user = self.non_owner
        assert list(self.autocomplete.choices_for_request()) == []
        assert self.form.is_valid() is False

    def test_owner_can_see_and_save_item(self):
        self.request.user = self.owner
        assert list(self.autocomplete.choices_for_request()) == [self.item]
        assert self.form.is_valid() is True
