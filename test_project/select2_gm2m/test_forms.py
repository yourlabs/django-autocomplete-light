from django import test

from select2_generic_m2m.test_forms import GenericSelect2TestMixin

from .forms import TForm
from .models import TModel


class GM2MFormTest(GenericSelect2TestMixin, test.TestCase):
    model = TModel
    form = TForm
    url_name = 'select2_gm2m'

    def add_relations(self, fixture, relations):
        fixture.test = relations

    def assert_relation_equals(self, expected, result):
        self.assertEquals(len(expected), len(result))

        for o in result:
            self.assertIn(o, expected)
