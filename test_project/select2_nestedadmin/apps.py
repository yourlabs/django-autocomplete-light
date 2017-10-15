from django.apps import AppConfig
from django.db.models.signals import post_migrate


class TestApp(AppConfig):
    name = 'select2_nestedadmin'
