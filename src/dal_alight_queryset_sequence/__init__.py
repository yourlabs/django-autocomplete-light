"""
Django-autocomplete-light extension for django-querysetsequence.

Provides view and widget classes that combine the QuerySetSequence
business logic from :py:mod:`dal_queryset_sequence` with the
autocomplete-light web component from :py:mod:`dal_alight`.

Add ``dal_alight`` and ``dal_queryset_sequence`` to ``INSTALLED_APPS`` to
enable the shortcut imports in :py:mod:`dal.autocomplete`.

For example usage, refer to the ``select2_generic_foreign_key`` example app
in ``test_project`` (which this mirrors, using autocomplete-light instead of
Select2).
"""
