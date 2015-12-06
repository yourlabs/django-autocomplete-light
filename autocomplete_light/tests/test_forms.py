import unittest

import autocomplete_light.shortcuts as autocomplete_light
import lxml.html
from django import forms, http, VERSION
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory
from django.test import TestCase
from django.utils import translation
from django.utils.encoding import force_text

from ..example_apps.basic.forms import (DjangoCompatMeta, FkModelForm,
                                        GfkModelForm, MtmModelForm,
                                        OtoModelForm)
from ..example_apps.basic.models import FkModel, GfkModel, MtmModel, OtoModel
from ..example_apps.autocomplete_test_case_app.models import NonIntegerPk
from ..example_apps.autocomplete_test_case_app.forms import NonIntegerPkForm

try:
    from unittest import mock
except ImportError:  # python2
    import mock

try:
    from ..example_apps.basic.forms import GmtmModelForm
except ImportError:
    GmtmModelForm = None
    GmtmModel = None
else:
    from ..example_apps.basic.models import GmtmModel

try:
    from ..example_apps.basic.forms import TaggitModelForm
except ImportError:
    TaggitModelForm = None
    TaggitModel = None
else:
    from ..example_apps.basic.models import TaggitModel


@unittest.skipIf(VERSION < (1, 5), 'Django < 1.5')
class TestUnuseableVirtualfield(TestCase):
    def test_modelform_factory(self):
        from ..example_apps.unuseable_virtualfield.models import HasVotes

        class MyForm(autocomplete_light.ModelForm):
            class Meta(DjangoCompatMeta):
                model = HasVotes
        MyForm()


class SelectMultipleHelpTextRemovalMixin(object):
    def test_help_text_removed(self):
        class ModelForm(forms.ModelForm):
            class Meta(DjangoCompatMeta):
                model = MtmModel
        form = ModelForm()
        help_text = force_text(form.fields['relation'].help_text).strip()

        class ModelForm(autocomplete_light.ModelForm):
            class Meta(DjangoCompatMeta):
                model = MtmModel
        form = ModelForm()
        my_help_text = force_text(form.fields['relation'].help_text).strip()

        # If help_text is not empty (which is wasn't before Django 1.8 fixed
        # #9321), test that it's empty in autocomplete_light's ModelForm.
        assert not help_text or help_text not in my_help_text


class SelectMultipleHelpTextRemovalMixinFrTestCase(
        SelectMultipleHelpTextRemovalMixin, TestCase):

    def setUp(self):
        translation.activate('fr_FR')


class BaseModelFormMixin(object):
    def setUp(self):
        self.james = self.model_class.objects.create(name='James')
        self.janis = self.model_class.objects.create(name='Janis')
        self.test_instance = self.james

    def tearDown(self):
        self.model_class.objects.all().delete()


class ModelFormBaseMixin(BaseModelFormMixin):
    widget_class = autocomplete_light.ChoiceWidget

    def get_new_autocomplete_class(self):
        class SpecialAutocomplete(autocomplete_light.AutocompleteModelBase):
            model = self.model_class
        return SpecialAutocomplete

    def form_value(self, model):
        return 'relation=%s' % model.pk

    def field_value(self, model):
        return getattr(model, 'relation')

    def assertExpectedFormField(self, name='relation'):
        self.assertInForm(name)

        if self.__class__.__name__ != 'TaggitModelFormTestCase':
            # django-taggit enforces verbose_name=_('Tags')
            # bug reported at:
            # https://github.com/alex/django-taggit/issues/177
            self.assertEqual(force_text(self.form[name].label), name.capitalize())

        self.assertTrue(isinstance(self.form.fields[name],
            self.field_class))
        self.assertTrue(isinstance(self.form.fields[name].widget,
            self.widget_class))
        self.assertEqual(self.form.fields[name].autocomplete.__name__,
                self.autocomplete_name)

    def assertInForm(self, name):
        self.assertIn(name, self.form.fields)

    def assertNotInForm(self, name):
        self.assertNotIn(name, self.form.fields)

    def assertIsAutocomplete(self, name):
        self.assertIsInstance(self.form.fields[name],
                autocomplete_light.FieldBase)

    def assertNotIsAutocomplete(self, name):
        self.assertNotIsInstance(self.form.fields[name],
                autocomplete_light.FieldBase)

    def test_appropriate_field_on_modelform(self):
        self.form = self.model_form_class()

        self.assertExpectedFormField()
        self.assertIsAutocomplete('noise')

    def test_appropriate_field_with_modelformfactory(self):
        form_class = modelform_factory(self.model_class,
                form=self.model_form_class, exclude=[])
        self.form = form_class()

        self.assertExpectedFormField()
        self.assertIsAutocomplete('noise')

    @unittest.skipUnless(VERSION >= (1, 6), 'Django >= 1.6')
    def test_appropriate_field_on_modelform_with_all(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta:
                model = self.model_class
                fields = '__all__'
        self.form = ModelForm()

        self.assertExpectedFormField()
        self.assertIsAutocomplete('noise')

    def test_appropriate_field_on_modelform_with_formfield_callback(self):
        # This tests what django admin does
        def cb(f, **kwargs):
            return f.formfield(**kwargs)

        form_class = modelform_factory(self.model_class,
                form=self.model_form_class, formfield_callback=cb,
                exclude=[])
        self.form = form_class()

        self.assertExpectedFormField()
        self.assertIsAutocomplete('noise')
        self.assertInForm('name')

    def test_widget_override(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta(DjangoCompatMeta):
                model = self.model_class
                widgets = {'relation': self.widget_class(widget_attrs={
                    'class': 'test-class', 'data-foo': 'bar'})}

        self.form = ModelForm()

        et = lxml.html.fromstring(self.form.as_p())
        attrib = et.cssselect('.autocomplete-light-widget.relation')[0].attrib
        self.assertEquals(attrib['data-foo'], 'bar')
        self.assertIn('test-class', attrib['class'])

    def test_meta_exclude_name(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta:
                model = self.model_class
                exclude = ('name',)

        self.form = ModelForm()

        self.assertExpectedFormField()
        self.assertNotInForm('name')
        self.assertIsAutocomplete('noise')

    def test_meta_exclude_relation(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta:
                model = self.model_class
                exclude = ['relation']

        self.form = ModelForm()

        self.assertInForm('name')
        self.assertIsAutocomplete('noise')
        self.assertNotInForm('relation')

    def test_meta_fields_name(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta:
                model = self.model_class
                fields = ['name']

        self.form = ModelForm()

        self.assertInForm('name')
        self.assertNotInForm('noise')
        self.assertNotInForm('relation')

    def test_meta_fields_relation(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta:
                model = self.model_class
                fields = ['relation']

        self.form = ModelForm()

        self.assertExpectedFormField()
        self.assertNotInForm('name')
        self.assertNotInForm('noise')

    def test_meta_autocomplete_fields(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta(DjangoCompatMeta):
                model = self.model_class
                autocomplete_fields = ['relation']

        self.form = ModelForm()

        self.assertExpectedFormField()
        self.assertNotIsAutocomplete('noise')
        self.assertInForm('name')

    def test_meta_autocomplete_exclude(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta(DjangoCompatMeta):
                model = self.model_class
                autocomplete_exclude = ['relation']

        self.form = ModelForm()

        self.assertInForm('name')
        self.assertNotIsAutocomplete('relation')
        self.assertIsAutocomplete('noise')

    def test_meta_autocomplete_names(self):
        SpecialAutocomplete = self.get_new_autocomplete_class()
        autocomplete_light.register(SpecialAutocomplete)

        class ModelForm(autocomplete_light.ModelForm):
            class Meta(DjangoCompatMeta):
                model = self.model_class
                autocomplete_names = {
                    'relation': 'SpecialAutocomplete'
                }

        self.form = ModelForm()

        self.assertInForm('name')
        self.assertIsAutocomplete('relation')
        self.assertIsAutocomplete('noise')

        self.assertTrue(issubclass(self.form.fields['relation'].autocomplete,
                                   SpecialAutocomplete))
        autocomplete_light.registry.unregister('SpecialAutocomplete')


    def test_modelform_factory(self):
        self.form = autocomplete_light.modelform_factory(self.model_class,
                exclude=[])()

        self.assertExpectedFormField()

    @unittest.skipUnless((1, 8) >= VERSION >= (1, 6), 'Django >= 1.6')
    def test_modelform_factory_does_not_warn(self):
        # fix for #257
        with mock.patch('warnings.warn') as warn:
            self.form = autocomplete_light.modelform_factory(self.model_class,
                    fields='__all__')()
            self.assertEqual(warn.call_count, 0)

        self.assertExpectedFormField()

    def test_modelform_factory_fields_relation(self):
        self.form = autocomplete_light.modelform_factory(self.model_class,
                fields=['relation'])()

        self.assertExpectedFormField()
        self.assertNotInForm('name')
        self.assertNotInForm('noise')

    def test_modelform_factory_exclude_relation(self):
        self.form = autocomplete_light.modelform_factory(self.model_class,
                exclude=['relation'])()

        self.assertNotInForm('relation')
        self.assertInForm('name')
        self.assertIsAutocomplete('noise')

    def test_modelform_factory_autocomplete_fields_relation(self):
        if VERSION < (1, 7):
            fields = None
        else:
            fields = '__all__'

        self.form = autocomplete_light.modelform_factory(self.model_class,
                autocomplete_fields=['relation'], fields=fields)()

        self.assertExpectedFormField()
        self.assertNotIsAutocomplete('noise')
        self.assertInForm('name')

    def test_modelform_factory_autocomplete_exclude_relation(self):
        self.form = autocomplete_light.modelform_factory(self.model_class,
                autocomplete_exclude=['relation'], exclude=[])()

        self.assertNotIsAutocomplete('relation')
        self.assertInForm('name')
        self.assertIsAutocomplete('noise')

    def test_modelform_factory_fields_name(self):
        self.form = autocomplete_light.modelform_factory(self.model_class,
                fields=['name'])()

        self.assertInForm('name')
        self.assertNotInForm('relation')
        self.assertNotInForm('noise')

    def test_modelform_factory_exclude_name(self):
        self.form = autocomplete_light.modelform_factory(self.model_class,
                exclude=['name'])()

        self.assertNotInForm('name')
        self.assertExpectedFormField()
        self.assertIsAutocomplete('noise')

    def test_modelform_factory_autocomplete_names(self):
        SpecialAutocomplete = self.get_new_autocomplete_class()
        autocomplete_light.registry.register(SpecialAutocomplete)

        ModelForm = autocomplete_light.modelform_factory(self.model_class,
            autocomplete_names={'relation': 'SpecialAutocomplete'}, 
            exclude=[])

        self.form = ModelForm()

        self.assertInForm('name')
        self.assertIsAutocomplete('relation')
        self.assertIsAutocomplete('noise')

        self.assertTrue(issubclass(self.form.fields['relation'].autocomplete,
                                   SpecialAutocomplete))

    def test_empty_registry(self):
        registry = autocomplete_light.AutocompleteRegistry()

        class ModelForm(autocomplete_light.ModelForm):
            relation = self.field_class(registry=registry,
                autocomplete=registry.register(self.model_class))
            relation2 = self.field_class(registry=registry,
                autocomplete=registry.register(self.model_class))

            class Meta(DjangoCompatMeta):
                model = self.model_class

        self.form = ModelForm()

        self.assertExpectedFormField()
        self.assertExpectedFormField('relation2')

    def test_create_with_relation(self):
        form = self.model_form_class(http.QueryDict(
            'name=test&%s' % self.form_value(self.janis)))

        self.assertTrue(form.is_valid())

        result = form.save()
        self.assertEqual(self.field_value(result), self.janis)

    def test_add_relation(self):
        form = self.model_form_class(http.QueryDict(
            'name=test&%s' % self.form_value(self.janis)),
            instance=self.test_instance)

        self.assertTrue(form.is_valid())

        result = form.save()
        self.assertEqual(self.field_value(result), self.janis)

    def test_meta_in_parent(self):
        class DefaultForm(autocomplete_light.ModelForm):
            class Meta:
                model = self.model_class
                exclude = []

        class MyForm(DefaultForm):
            pass

        self.form = MyForm()

        self.assertExpectedFormField()
        self.assertIsAutocomplete('noise')

    def test_modelform_without_model(self):
        class DefaultForm(autocomplete_light.ModelForm):
            class Meta:
                pass

        class MyForm(DefaultForm):
            class Meta:
                model = self.model_class
                exclude = []

        self.form = MyForm()

        self.assertExpectedFormField()
        self.assertIsAutocomplete('noise')


class GenericModelFormMixin(object):
    autocomplete_name = 'A'


    def get_new_autocomplete_class(self):
        class SpecialAutocomplete(autocomplete_light.AutocompleteGenericBase):
            choices = autocomplete_light.registry[self.autocomplete_name].choices
            search_fields = autocomplete_light.registry[self.autocomplete_name].search_fields
        return SpecialAutocomplete

    def test_meta_autocomplete_exclude(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta(DjangoCompatMeta):
                model = self.model_class
                autocomplete_exclude = ['relation']

        self.form = ModelForm()

        self.assertNotInForm('relation')
        self.assertInForm('name')
        self.assertIsAutocomplete('noise')

    def test_modelform_factory_autocomplete_exclude_relation(self):
        self.form = autocomplete_light.modelform_factory(self.model_class,
                autocomplete_exclude=['relation'], exclude=[])()

        self.assertNotInForm('relation')
        self.assertInForm('name')
        self.assertIsAutocomplete('noise')

    def test_empty_registry(self):
        registry = autocomplete_light.AutocompleteRegistry()

        class ModelForm(autocomplete_light.ModelForm):
            relation = self.field_class(registry=registry,
                autocomplete=registry.register(autocomplete_light.AutocompleteGenericBase,
                    choices=[self.model_class.objects.all()],
                    search_fields=['name']))

            class Meta(DjangoCompatMeta):
                model = self.model_class

        self.form = ModelForm()

        self.assertExpectedFormField()
        self.assertInForm('name')
        self.assertIsAutocomplete('noise')

    def form_value(self, model):
        return 'relation=%s-%s' % (ContentType.objects.get_for_model(model).pk, model.pk)


class MultipleRelationMixin(ModelFormBaseMixin):
    widget_class = autocomplete_light.MultipleChoiceWidget

    def field_value(self, model):
        return super(MultipleRelationMixin, self).field_value(model).all()[0]


class FkModelFormTestCase(ModelFormBaseMixin, TestCase):
    model_class = FkModel
    model_form_class = FkModelForm
    field_class = autocomplete_light.ModelChoiceField
    autocomplete_name = 'FkModelAutocomplete'


class OtoModelFormTestCase(ModelFormBaseMixin, TestCase):
    model_class = OtoModel
    model_form_class = OtoModelForm
    field_class = autocomplete_light.ModelChoiceField
    autocomplete_name = 'OtoModelAutocomplete'


class GfkModelFormTestCase(GenericModelFormMixin,
        ModelFormBaseMixin, TestCase):
    model_class = GfkModel
    model_form_class = GfkModelForm
    field_class = autocomplete_light.GenericModelChoiceField


class MtmModelFormTestCase(MultipleRelationMixin, ModelFormBaseMixin,
        TestCase):
    model_class = MtmModel
    model_form_class = MtmModelForm
    field_class = autocomplete_light.ModelMultipleChoiceField
    autocomplete_name = 'MtmModelAutocomplete'


@unittest.skipIf(TaggitModelForm is None, "taggit is not available.")
class TaggitModelFormTestCase(ModelFormBaseMixin, TestCase):
    model_class = TaggitModel
    model_form_class = TaggitModelForm
    field_class = autocomplete_light.TaggitField
    widget_class = autocomplete_light.TaggitWidget
    autocomplete_name = 'TagAutocomplete'

    def setUp(self):
        self.james = 'james'
        self.janis = 'janis'
        self.test_instance = self.model_class.objects.create(name='test')

    def form_value(self, model):
        return 'relation=%s' % model

    def field_value(self, model):
        return model.relation.all().values_list('name', flat=True)[0]

    def test_empty_registry(self):
        pass

    def test_widget_override(self):
        class ModelForm(autocomplete_light.ModelForm):
            class Meta(DjangoCompatMeta):
                model = self.model_class
                widgets = {'relation': self.widget_class(attrs={
                    'class': 'test-class', 'data-foo': 'bar'})}

        self.form = ModelForm()

        et = lxml.html.fromstring(self.form.as_p())
        attrib = et.cssselect('input[name=relation].autocomplete')[0].attrib
        self.assertEquals(attrib['data-foo'], 'bar')
        self.assertIn('test-class', attrib['class'])


@unittest.skipIf(GmtmModelForm is None, "genericm2m is not available.")
class GmtmModelFormTestCase(MultipleRelationMixin,
        GenericModelFormMixin,
        ModelFormBaseMixin, TestCase):
    model_class = GmtmModel
    model_form_class = GmtmModelForm
    field_class = autocomplete_light.GenericModelMultipleChoiceField

    def field_value(self, model):
        return getattr(model, 'relation').all().generic_objects()[0]


class NonIntegerPkTestCase(ModelFormBaseMixin, TestCase):
    model_class = NonIntegerPk
    model_form_class = NonIntegerPkForm
    field_class = autocomplete_light.ModelChoiceField
    autocomplete_name = 'NonIntegerPkAutocomplete'
