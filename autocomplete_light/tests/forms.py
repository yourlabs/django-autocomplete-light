import unittest

from django.contrib.contenttypes.models import ContentType

import autocomplete_light

from .test_app.models import *
from .test_app.forms import *

class BaseModelFormTestCase(unittest.TestCase):
    def setUp(self):
        self.james = self.model_class.objects.create(name='James')
        self.janis = self.model_class.objects.create(name='Janis')

    def tearDown(self):
        self.model_class.objects.all().delete()


class SimpleRelationModelFormBaseTestCase(BaseModelFormTestCase):
    def form_value(self, model):
        return model.pk

    def test_000_field(self):
        form = self.model_form_class()

        self.assertTrue(isinstance(form.fields[self.relation_name],
            self.field_class))

    def test_001_create(self):
        form = self.model_form_class({self.relation_name:
            self.form_value(self.janis), 'name': 'test'})
        self.assertTrue(form.is_valid())

        result = form.save()
        self.assertEqual(getattr(result, self.relation_name), self.janis)

    def test_002_update(self):
        form = self.model_form_class({self.relation_name:
            self.form_value(self.janis), 'name': 'test'},
            instance=self.james)
        self.assertTrue(form.is_valid())

        result = form.save()
        self.assertEqual(getattr(result, self.relation_name), self.janis)


class MultipleRelationModelFormBaseTestCase(BaseModelFormTestCase):
    pass


class FkModelFormTestCase(SimpleRelationModelFormBaseTestCase):
    model_class = FkModel
    model_form_class = FkModelForm
    relation_name = 'fk'
    field_class = autocomplete_light.ModelChoiceField


class OtoModelFormTestCase(SimpleRelationModelFormBaseTestCase):
    model_class = OtoModel
    model_form_class = OtoModelForm
    relation_name = 'oto'
    field_class = autocomplete_light.ModelChoiceField


class GfkModelFormTestCase(SimpleRelationModelFormBaseTestCase):
    model_class = GfkModel
    model_form_class = GfkModelForm
    relation_name = 'gfk'
    field_class = autocomplete_light.GenericModelChoiceField

    def form_value(self, model):
        r = '%s-%s' % (ContentType.objects.get_for_model(model).pk, model.pk)
        return r
