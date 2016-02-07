from dal.forms import FutureModelFormMetaclass

from dal_select2.fields import (
    Select2ModelChoiceField,
    Select2ModelMultipleChoiceField
)

from django.apps import AppConfig
from django.db import models
from django import forms


class FutureApp(AppConfig):
    name = 'dal_select2'

    def ready(self):
        FutureModelFormMetaclass.register_formfield_for_modelfield(
            model_field=models.ForeignKey,
            form_field=Select2ModelChoiceField,
        )

        FutureModelFormMetaclass.register_formfield_for_modelfield(
            model_field=models.OneToOneField,
            form_field=Select2ModelChoiceField,
        )

        FutureModelFormMetaclass.register_formfield_for_modelfield(
            model_field=models.ManyToManyField,
            form_field=Select2ModelMultipleChoiceField,
        )
