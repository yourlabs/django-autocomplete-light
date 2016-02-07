from dal_magic.forms import MagicFormMetaclass

from dal_select2.fields import (
    Select2ModelChoiceField,
    Select2ModelMultipleChoiceField
)

from django.apps import AppConfig
from django.db import models
from django import forms


class MagicApp(AppConfig):
    name = 'dal_select2'

    def ready(self):
        MagicFormMetaclass.register_formfield_for_modelfield(
            model_field=models.ForeignKey,
            form_field=Select2ModelChoiceField,
        )

        MagicFormMetaclass.register_formfield_for_modelfield(
            model_field=models.OneToOneField,
            form_field=Select2ModelChoiceField,
        )

        MagicFormMetaclass.register_formfield_for_modelfield(
            model_field=models.ManyToManyField,
            form_field=Select2ModelMultipleChoiceField,
        )
