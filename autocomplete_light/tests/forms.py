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


class ModelFormBaseTestCase(BaseModelFormTestCase):
    def form_value(self, model):
        return model.pk

    def field_value(self, model):
        return getattr(model, self.relation_name)

    def test_000_field(self):
        form = self.model_form_class()

        self.assertTrue(isinstance(form.fields[self.relation_name],
            self.field_class))

    def test_001_create(self):
        form = self.model_form_class({self.relation_name:
            self.form_value(self.janis), 'name': 'test'})
        self.assertTrue(form.is_valid())

        result = form.save()
        self.assertEqual(self.field_value(result), self.janis)

    def test_002_update(self):
        form = self.model_form_class({self.relation_name:
            self.form_value(self.janis), 'name': 'test'},
            instance=self.james)
        self.assertTrue(form.is_valid())

        result = form.save()
        self.assertEqual(self.field_value(result), self.janis)


class GenericModelFormTestCaseMixin(object):
    def form_value(self, model):
        return '%s-%s' % (ContentType.objects.get_for_model(model).pk, model.pk)


class MultipleRelationTestCaseMixin(ModelFormBaseTestCase):
    def form_value(self, model):
        return [super(MultipleRelationTestCaseMixin, self).form_value(model)]

    def field_value(self, model):
        return super(MultipleRelationTestCaseMixin, self).field_value(model).all()[0]


class FkModelFormTestCase(ModelFormBaseTestCase):
    model_class = FkModel
    model_form_class = FkModelForm
    relation_name = 'fk'
    field_class = autocomplete_light.ModelChoiceField


class OtoModelFormTestCase(ModelFormBaseTestCase):
    model_class = OtoModel
    model_form_class = OtoModelForm
    relation_name = 'oto'
    field_class = autocomplete_light.ModelChoiceField


class GfkModelFormTestCase(GenericModelFormTestCaseMixin,
        ModelFormBaseTestCase):
    model_class = GfkModel
    model_form_class = GfkModelForm
    relation_name = 'gfk'
    field_class = autocomplete_light.GenericModelChoiceField


class MtmModelFormTestCase(MultipleRelationTestCaseMixin, ModelFormBaseTestCase):
    model_class = MtmModel
    model_form_class = MtmModelForm
    relation_name = 'mtm'
    field_class = autocomplete_light.ModelMultipleChoiceField


try:
    import genericm2m
except ImportError:
    class GmtmModelFormTestCase(object):
        pass
else:
    class GmtmModelFormTestCase(MultipleRelationTestCaseMixin,
            GenericModelFormTestCaseMixin,
            ModelFormBaseTestCase):
        model_class = GmtmModel
        model_form_class = GmtmModelForm
        relation_name = 'gmtm'
        field_class = autocomplete_light.GenericModelMultipleChoiceField

        def field_value(self, model):
            return getattr(model, self.relation_name).all().generic_objects()[0]
