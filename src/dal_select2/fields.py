import importlib

from django import forms
from django.conf import settings

from dal.fields import FutureModelFieldMixin

from .widgets import ModelSelect2, ModelSelect2Multiple


class Select2ModelChoiceField(FutureModelFieldMixin,
                              forms.ModelChoiceField):
    widget = ModelSelect2

    @classmethod
    def factory(cls, meta, field):
        return cls(factory=dict(meta=meta, field=field))


class Select2ModelMultipleChoiceField(FutureModelFieldMixin,
                                      forms.ModelMultipleChoiceField):

    widget = ModelSelect2Multiple

    @classmethod
    def factory(cls, meta, field):
        raise NotImplemented()
