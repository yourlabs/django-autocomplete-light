from dal import autocomplete

from django import forms
from django import http
from django import test
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from queryset_sequence import QuerySetSequence

import six

from .forms import TForm
from .models import TModel, TProxyModel


class GenericFormTest(test.TestCase):  # noqa
    """Demonstrate the requirement for VirtualFieldHandlingMixin."""

    def get_value(self, model):
        view = autocomplete.BaseQuerySetSequenceView
        return view.get_result_value(view(), model)

    def test_model_name(self):
        view = autocomplete.BaseQuerySetSequenceView
        self.assertEqual(view.get_model_name(view(), TProxyModel), 't model')
        self.assertEqual(view.get_model_name(view(), TModel), 't model')

    def test_model_name_index_error(self):
        view = autocomplete.BaseQuerySetSequenceView
        # remove the parents attribute
        TProxyModel._meta.parents = {}
        self.assertEqual(
            view.get_model_name(view(), TProxyModel), 't proxy model')

    def test_save(self):
        # Create an option to select
        fixture = TModel.objects.create(name='relation' + self.id())

        # Instanciate the form with the fixture selected
        form = TForm(http.QueryDict('name=%s&test=%s' % (
            self.id(), self.get_value(fixture))))

        # Ensure that the form is valid
        self.assertTrue(form.is_valid())

        # Ensure that form.save updates the relation field
        instance = form.save()
        self.assertEqual(fixture, instance.test)

        # Ensure that the relation field was properly saved
        self.assertEqual(TModel.objects.get(pk=instance.pk).test, fixture)

    def test_validate(self):
        # Create an option to select
        fixture = TModel.objects.create(name=self.id())

        # Instanciate the form with the fixture selected
        form = TForm(http.QueryDict('name=%s&test=%s' % (
            self.id(), self.get_value(fixture))))

        # Remove the option from field queryset choices
        form.fields['test'].queryset = QuerySetSequence(
            TModel.objects.exclude(pk=fixture.pk))

        # Form should not validate
        self.assertFalse(form.is_valid())

    def test_initial(self):
        # this sets the proper widget
        from . import urls  # noqa

        # Create an initial instance with a created relation
        relation = TModel.objects.create(name='relation' + self.id())
        fixture = TModel(name=self.id())
        fixture.test = relation
        fixture.save()

        # Instanciate the modelform for that instance
        form = TForm(instance=fixture)

        # Ensure that the widget rendered right, with only the selection
        expected = forms.Select(
            choices=(
                (self.get_value(relation), six.text_type(relation)),
            ),
            attrs={
                'data-autocomplete-light-function': 'select2',
                'data-autocomplete-light-url': reverse('TForm_autocomp_test'),
                'data-autocomplete-light-language': 'en',
                'id': 'id_test',
            }
        ).render('test', value=self.get_value(relation))
        result = six.text_type(form['test'].as_widget())

        expected += '''
        <div class="dal-forward-conf" id="dal-forward-conf-for_id_test"
        style="display:none">
        <script type="text/dal-forward-conf">
        [{"type": "field", "src": "name"}]</script>
        </div>
        '''

        self.maxDiff = 10000
        self.assertHTMLEqual(result, expected)
