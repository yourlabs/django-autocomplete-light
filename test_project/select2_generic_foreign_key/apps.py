from django.apps import AppConfig
from django.db.models.signals import post_migrate

from dal.test.utils import Fixtures, fixtures


class TestApp(AppConfig):
    name = 'select2_generic_foreign_key'

    def ready(self):
        post_migrate.connect(fixtures, sender=self)
        post_migrate.connect(Fixtures('auth.group'), sender=self)
