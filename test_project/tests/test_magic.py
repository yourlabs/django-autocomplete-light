import importlib
import unittest

from dal_magic.forms import MagicForm

from django.apps import apps
from django.conf import settings


class TestMagicForm(unittest.TestCase):
    def test_magicform(self):
        #for app in settings.INSTALLED_APPS:
        for app in ['select2_foreign_key']:
            try:
                TestModel = apps.get_model('%s.TestModel' % app)
            except:
                continue

            try:
                forms = importlib.import_module('%s.forms' % app)
            except:
                continue

            expected = getattr(forms, 'TestForm', None)

            if expected is None:
                continue

            class result(MagicForm):
                class Meta:
                    model = expected.Meta.model
                    fields = expected.Meta.fields

            self.assert_fields_equals(expected, result)

    def assert_field_equals(self, expected, result):
        self.assertIsInstance(result, type(expected))

    def assert_fields_equals(self, expected, result):
        for name, field in expected.base_fields.items():
            self.assert_field_equals(field, result.base_fields.get(name))
