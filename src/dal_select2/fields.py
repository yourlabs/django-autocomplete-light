from django import forms

from dal_magic.forms import MagicFieldMixin

from .widgets import ModelSelect2, ModelSelect2Multiple


class Select2ModelChoiceField(MagicFieldMixin,
                              forms.ModelChoiceField):
    widget = ModelSelect2

    @classmethod
    def factory(cls, model, form, field):
        raise NotImplemented()


class Select2ModelMultipleChoiceField(
    MagicFieldMixin,
    forms.ModelMultipleChoiceField):

    widget = ModelSelect2Multiple

    @classmethod
    def factory(cls, model, form, field):
        raise NotImplemented()
