import unittest

from django import http
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory

import autocomplete_light

from .apps.basic.admin import *
from .apps.basic.models import *
from .apps.basic.forms import *


class BaseModelFormTestCase(unittest.TestCase):
    def setUp(self):
        self.james = self.model_class.objects.create(name='James')
        self.janis = self.model_class.objects.create(name='Janis')

    def tearDown(self):
        self.model_class.objects.all().delete()


class ModelFormBaseTestCase(BaseModelFormTestCase):
    widget_class = autocomplete_light.ChoiceWidget

    def form_value(self, model):
        return 'relation=%s' % model.pk

    def field_value(self, model):
        return getattr(model, 'relation')


    def do_field_test(self, form):
        self.assertTrue(isinstance(form.fields['relation'],
            self.field_class))
        self.assertTrue(isinstance(form.fields['relation'].widget,
            self.widget_class))
        self.assertEqual(form.fields['relation'].autocomplete.__name__,
                self.autocomplete_name)

    def test_appropriate_field_on_modelform(self):
        form = self.model_form_class()
        self.do_field_test(form)

    def test_appropriate_field_with_modelformfactory(self):
        form_class = modelform_factory(self.model_class,
                form=self.model_form_class)
        form = form_class()
        self.do_field_test(form)

    def test_appropriate_field_on_modelform_with_formfield_callback(self):
        # This tests what django admin does
        def cb(f, **kwargs):
            return f.formfield(**kwargs)

        form_class = modelform_factory(self.model_class,
                form=self.model_form_class, formfield_callback=cb)
        form = form_class()
        self.do_field_test(form)

    def test_meta_exclude(self):
        class Meta:
            model = self.model_class
            exclude = ['relation']

        ModelForm = type('ExcludeAutocompleteModelForm',
                (autocomplete_light.ModelForm,), {'Meta': Meta})
        form = ModelForm()

        self.assertFalse('relation' in form.fields)

    def test_meta_fields(self):
        class Meta:
            model = self.model_class
            fields = ['name']

        ModelForm = type('ExcludeAutocompleteModelForm',
                (autocomplete_light.ModelForm,), {'Meta': Meta})
        form = ModelForm()

        self.assertFalse('relation' in form.fields)

    def test_create_with_relation(self):
        form = self.model_form_class(http.QueryDict(
            'name=test&%s' % self.form_value(self.janis)))

        self.assertTrue(form.is_valid())

        result = form.save()
        self.assertEqual(self.field_value(result), self.janis)

    def test_add_relation(self):
        form = self.model_form_class(http.QueryDict(
            'name=test&%s' % self.form_value(self.janis)),
            instance=self.james)

        self.assertTrue(form.is_valid())

        result = form.save()
        self.assertEqual(self.field_value(result), self.janis)


class GenericModelFormTestCaseMixin(object):
    autocomplete_name = 'A'

    def form_value(self, model):
        return 'relation=%s-%s' % (ContentType.objects.get_for_model(model).pk, model.pk)


class MultipleRelationTestCaseMixin(ModelFormBaseTestCase):
    widget_class = autocomplete_light.MultipleChoiceWidget

    def field_value(self, model):
        return super(MultipleRelationTestCaseMixin, self).field_value(model).all()[0]


class FkModelFormTestCase(ModelFormBaseTestCase):
    model_class = FkModel
    model_form_class = FkModelForm
    field_class = autocomplete_light.ModelChoiceField
    autocomplete_name = 'FkModelAutocomplete'


class OtoModelFormTestCase(ModelFormBaseTestCase):
    model_class = OtoModel
    model_form_class = OtoModelForm
    field_class = autocomplete_light.ModelChoiceField
    autocomplete_name = 'OtoModelAutocomplete'


class GfkModelFormTestCase(GenericModelFormTestCaseMixin,
        ModelFormBaseTestCase):
    model_class = GfkModel
    model_form_class = GfkModelForm
    field_class = autocomplete_light.GenericModelChoiceField


class MtmModelFormTestCase(MultipleRelationTestCaseMixin, ModelFormBaseTestCase):
    model_class = MtmModel
    model_form_class = MtmModelForm
    field_class = autocomplete_light.ModelMultipleChoiceField
    autocomplete_name = 'MtmModelAutocomplete'



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
