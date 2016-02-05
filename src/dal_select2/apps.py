from dal_magic.forms import MagicFormMetaclass

from dal_select2.widgets import ModelSelect2, ModelSelect2Multiple

from django.apps import AppConfig
from django.db import models
from django import forms


class MagicApp(AppConfig):
    name = 'dal_select2'

    def ready(self):
        MagicFormMetaclass.add_rule(
            modelfield=models.ForeignKey,
            widget=ModelSelect2,
        )

        MagicFormMetaclass.register_field(
            modelfield=ModelMultipleChoiceField,
            widget=ModelSelect2Multiple,
        )
