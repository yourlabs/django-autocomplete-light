from dal import autocomplete

from django import forms
from django import http
from django import test
from django.contrib.auth.models import Group
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from queryset_sequence import QuerySetSequence

import six

from .forms import TForm
from .models import TModel


class GenericSelect2TestMixin(object):
    maxDiff = 3000

    def get_value(self, model):
        view = autocomplete.BaseQuerySetSequenceView
        return view.get_result_value(view(), model)

    def add_relations(self, fixture, relations):
        fixture.test = relations

    def assert_relation_equals(self, expected, result):
        self.assertEquals(len(expected), len(result))

        for o in result:
            self.assertIn(o, expected)

    def test_save(self):
        m0 = self.model.objects.create(name=self.id())
        m1 = Group.objects.create(name=self.id())

        form = self.form(http.QueryDict('name=%s&test=%s&test=%s' % (
            self.id(), self.get_value(m0), self.get_value(m1))))
        expected = [m0, m1]

        assert form.is_valid()
        instance = form.save()

        self.assert_relation_equals(expected, instance.test.all())
        self.assert_relation_equals(
            expected,
            self.model.objects.get(pk=instance.pk).test.all(),
        )

    def test_validate(self):
        fixture = self.model.objects.create(name=self.id())

        form = self.form(http.QueryDict('name=%s&test=%s' % (
            self.id(), self.get_value(fixture))))

        form.fields['test'].queryset = QuerySetSequence(
            self.model.objects.exclude(pk=fixture.pk))

        self.assertFalse(form.is_valid())

    def test_initial(self):
        relation0 = self.model.objects.create(name='relation0' + self.id())
        relation1 = self.model.objects.create(name='relation1' + self.id())
        fixture = self.model.objects.create(name=self.id())
        self.add_relations(fixture, [relation0, relation1])

        # Instanciate the modelform for that instance
        form = self.form(instance=fixture)

        # Ensure that the widget rendered right, with only the selection
        self.assertHTMLEqual(
            forms.SelectMultiple(
                choices=(
                    (self.get_value(relation0), six.text_type(relation0)),
                    (self.get_value(relation1), six.text_type(relation1)),
                ),
                attrs={
                    'data-autocomplete-light-function': 'select2',
                    'data-autocomplete-light-url': reverse(self.url_name),
                    'id': 'id_test',
                }
            ).render('test', value=[
                self.get_value(relation0),
                self.get_value(relation1),
            ]),
            six.text_type(form['test'].as_widget())
        )


class GenericM2MFormTest(GenericSelect2TestMixin, test.TestCase):
    model = TModel
    form = TForm
    url_name = 'select2_generic_m2m'

    def add_relations(self, fixture, relations):
        for r in relations:
            fixture.test.connect(r)

    def assert_relation_equals(self, expected, result):
        self.assertEquals(len(expected), len(result))

        for o in result:
            self.assertIn(o.object, expected)
