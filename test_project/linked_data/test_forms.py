from dal import autocomplete

from django import forms
from django import http
from django import test
from django.apps import apps
from django.core.urlresolvers import reverse
from django.utils import six

from queryset_sequence import QuerySetSequence

from .forms import TestForm
from .models import TestModel


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
        fixture = TestModel.objects.create(name='relation' + self.id(), owner=self.owner)

        # Instantiate the form with the fixture selected
        form = TestForm(http.QueryDict('name=%s&owner=%s&test=%s' % (
            self.id(), self.owner.id, fixture.id)))

        # Ensure that the form is valid
        self.assertTrue(form.is_valid())

        # Ensure that form.save updates the relation field
        instance = form.save()
        self.assertEqual(fixture, instance.test)

        # Ensure that the relation field was properly saved
        self.assertEqual(TestModel.objects.get(pk=instance.pk).test, fixture)

    def test_validate(self):
        pass
        # Create an option to select
        fixture = TestModel.objects.create(name=self.id(), owner=self.owner)

        # Instantiate the form with the fixture selected but with wrong owner
        form = TestForm(http.QueryDict('name=%s&owner=%s&test=%s' % (
            self.id(), self.other_user.id, fixture.id)))

        # Form should not validate
        self.assertFalse(form.is_valid())

    def test_initial(self):
        # Create an initial instance with a created relation
        relation = TestModel.objects.create(name='relation' + self.id(), owner=self.owner)
        fixture = TestModel(name=self.id(), owner=self.owner)
        fixture.test = relation
        fixture.save()

        # Instanciate the modelform for that instance
        form = TestForm(instance=fixture)

        # Ensure that the widget rendered right, with only the selection
        self.assertEquals(
            forms.Select(
                choices=(
                    (None, "---------"),
                    (relation.id, six.text_type(relation)),
                ),
                attrs={
                    'data-autocomplete-light-function': 'select2',
                    'data-autocomplete-light-url': reverse('linked_data'),
                    'data-autocomplete-light-forward': 'owner',
                    'id': 'id_test',
                }
            ).render('test', value=relation.id),
            six.text_type(form['test'].as_widget())
        )
