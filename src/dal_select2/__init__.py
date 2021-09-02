"""Select2 support for DAL."""
import django

if django.VERSION < (3, 2): # pragma: no cover
    default_app_config = 'dal_select2.apps.DefaultApp'
