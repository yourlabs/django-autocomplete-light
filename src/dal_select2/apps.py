"""Default AppConfig for dal_select2."""
from django.apps import AppConfig
from django.core import checks

from .checks import select2_submodule_check


class DefaultApp(AppConfig):
    """Default app for dal_select2."""

    name = 'dal_select2'

    def ready(self):
        """Register select2_submodule_check."""
        checks.register(select2_submodule_check)
