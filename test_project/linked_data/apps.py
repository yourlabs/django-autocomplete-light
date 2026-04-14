from django.apps import AppConfig
from django.db.models.signals import post_migrate

from dal.test.utils import OwnedFixtures


class TestApp(AppConfig):
    name = 'linked_data'

    def ready(self):
        post_migrate.connect(OwnedFixtures(), sender=self)
