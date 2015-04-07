import mock
import pytest
from django import VERSION

pytestmark = pytest.mark.skipif(VERSION < (1, 7),
                                reason="Checks are not supported before Django 1.7.")


def test_formfield_widget_compatibilty():
    from autocomplete_light.checks import (check_admin_formfield_widget_compatibility,
                                           W001)
    from autocomplete_light.example_apps.incompatible_widget_and_form_field.admin import FilmAdmin  # noqa
    assert check_admin_formfield_widget_compatibility(None) == [W001]


@mock.patch('autocomplete_light.checks.checks.register')
def test_check_registered(mocked_register):
    from autocomplete_light.checks import check_admin_formfield_widget_compatibility
    from autocomplete_light.registry import AutocompleteRegistry

    with mock.patch('autocomplete_light.checks.curry') as curry:
        registry = AutocompleteRegistry()

    mocked_register.assert_called_once_with(curry(
        check_admin_formfield_widget_compatibility,
        registry=registry
    ))
