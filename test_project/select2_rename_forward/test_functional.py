import linked_data.test_functional

from .models import TModel


class RenameForwardAdminLinkedDataTestTest(
        linked_data.test_functional.AdminLinkedDataTest):
    """Reusing functional test scenarios from linked_data app."""

    model = TModel
    inline_related_name = 'inline_test_models_rf'
