from select2_foreign_key import test_functional

from .models import TModel


class AdminForeignKeyTestCase(test_functional.AdminForeignKeyTestCase):
    model = TModel
