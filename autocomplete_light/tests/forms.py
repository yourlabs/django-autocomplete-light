import unittest

from django.contrib.contenttypes.models import ContentType

import autocomplete_light

from .apps.basic.models import *
from .apps.basic.forms import *


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
        return getattr(model, 'relation')

    def test_appropriate_field_on_modelform(self):
        form = self.model_form_class()

        self.assertTrue(isinstance(form.fields['relation'],
            self.field_class))

    def test_create_with_relation(self):
        form = self.model_form_class({'relation':
            self.form_value(self.janis), 'name': 'test'})
        self.assertTrue(form.is_valid())

        result = form.save()
        self.assertEqual(self.field_value(result), self.janis)

    def test_add_relation(self):
        form = self.model_form_class({'relation':
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
    field_class = autocomplete_light.ModelChoiceField


class OtoModelFormTestCase(ModelFormBaseTestCase):
    model_class = OtoModel
    model_form_class = OtoModelForm
    field_class = autocomplete_light.ModelChoiceField


class GfkModelFormTestCase(GenericModelFormTestCaseMixin,
        ModelFormBaseTestCase):
    model_class = GfkModel
    model_form_class = GfkModelForm
    field_class = autocomplete_light.GenericModelChoiceField


class MtmModelFormTestCase(MultipleRelationTestCaseMixin, ModelFormBaseTestCase):
    model_class = MtmModel
    model_form_class = MtmModelForm
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
        field_class = autocomplete_light.GenericModelMultipleChoiceField

        def field_value(self, model):
            return getattr(model, 'relation').all().generic_objects()[0]
