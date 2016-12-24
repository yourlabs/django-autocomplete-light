from django import http
from django import test
from django.apps import apps

from .forms import TForm
from .models import TModel


class LinkedDataFormTest(test.TestCase):  # noqa
    """Linked data form test."""

    def setUp(self):
        super(LinkedDataFormTest, self).setUp()
        User = apps.get_model('auth.user')  # noqa
        self.owner, c = User.objects.get_or_create(
            username='owner'
        )
        self.other_user, c = User.objects.get_or_create(
            username='other'
        )

    def test_save(self):
        # Create an option to select
        fixture = TModel.objects.create(
            name='relation' + self.id(),
            owner=self.owner
        )

        # Instantiate the form with the fixture selected
        form = TForm(http.QueryDict('name=%s&owner=%s&test=%s' % (
            self.id(), self.owner.id, fixture.id)))

        # Ensure that the form is valid
        self.assertTrue(form.is_valid())

        # Ensure that form.save updates the relation field
        instance = form.save()
        self.assertEqual(fixture, instance.test)

        # Ensure that the relation field was properly saved
        self.assertEqual(TModel.objects.get(pk=instance.pk).test, fixture)

    def test_validate(self):
        pass
        # Create an option to select
        fixture = TModel.objects.create(name=self.id(), owner=self.owner)

        # Instantiate the form with the fixture selected but with wrong owner
        form = TForm(http.QueryDict('name=%s&owner=%s&test=%s' % (
            self.id(), self.other_user.id, fixture.id)))

        # Form should not validate
        self.assertFalse(form.is_valid())
