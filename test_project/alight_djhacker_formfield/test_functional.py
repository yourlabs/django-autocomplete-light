from alight_foreign_key import test_functional

from .models import TModel


class AdminForeignKeyTestCase(test_functional.AdminForeignKeyTestCase):
    model = TModel
    inline_related_name = 'inline_test_models_adf'
