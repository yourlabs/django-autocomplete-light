from dal.test.utils import OwnedFixtures

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class TestApp(AppConfig):
    name = 'linked_data_feedback'

    def ready(self):
        post_migrate.connect(OwnedFixtures(), sender=self)
