"""Default AppConfig for dal_select2."""
from django.apps import AppConfig
# from django.core import checks


class DefaultApp(AppConfig):
    """Default app for dal_select2."""

    name = 'dal_select2'

    def ready(self):
        """Register select2_submodule_check."""
