from dal import autocomplete

from django import forms
from django import http
from django import test
from django.core.urlresolvers import reverse
from django.utils import six

from queryset_sequence import QuerySetSequence

from .forms import TestForm
from .models import TestModel


class GenericFormTest(test.TestCase):  # noqa
    """Demonstrate the requirement for VirtualFieldHandlingMixin."""

    def get_value(self, model):
        view = autocomplete.BaseQuerySetSequenceView
        return view.get_result_value(view(), model)

    def test_save(self):
        # Create an option to select
        fixture = TestModel.objects.create(name='relation' + self.id())

        # Instanciate the form with the fixture selected
        form = TestForm(http.QueryDict('name=%s&test=%s' % (
            self.id(), self.get_value(fixture))))

        # Ensure that the form is valid
        self.assertTrue(form.is_valid())

        # Ensure that form.save updates the relation field
        instance = form.save()
        self.assertEqual(fixture, instance.test)

        # Ensure that the relation field was properly saved
        self.assertEqual(TestModel.objects.get(pk=instance.pk).test, fixture)

    def test_validate(self):
        # Create an option to select
        fixture = TestModel.objects.create(name=self.id())

        # Instanciate the form with the fixture selected
        form = TestForm(http.QueryDict('name=%s&test=%s' % (
            self.id(), self.get_value(fixture))))

        # Remove the option from field queryset choices
        form.fields['test'].queryset = QuerySetSequence(
            TestModel.objects.exclude(pk=fixture.pk))

        # Form should not validate
        self.assertFalse(form.is_valid())

    def test_initial(self):
        # Create an initial instance with a created relation
        relation = TestModel.objects.create(name='relation' + self.id())
        fixture = TestModel(name=self.id())
        fixture.test = relation
        fixture.save()

        # Instanciate the modelform for that instance
        form = TestForm(instance=fixture)

        # Ensure that the widget rendered right, with only the selection
        self.assertEquals(
            forms.Select(
                choices=(
                    (self.get_value(relation), six.text_type(relation)),
                ),
                attrs={
                    'data-autocomplete-light-function': 'select2',
                    'data-autocomplete-light-url': reverse('select2_gfk'),
                    'id': 'id_test',
                }
            ).render('test', value=self.get_value(relation)),
            six.text_type(form['test'].as_widget())
        )
