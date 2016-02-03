"""
Django-autocomplete-light extension for django-querysetsequence.

It provides view encapsulating business-logic for QuerySetSequence in
:py:class:`~dal_queryset_sequence.views.BaseQuerySetSequenceView` as well as
the widget encapsulating business logic for rendering only selected options in
:py:class:~dal_queryset_sequence.widgets.QuerySetSequenceSelectMixin`.

Add `dal_queryset_sequence` to INSTALLED_APPS to enable it in
:py:mod:`dal.autocomplete` shortcut module.

For example usage, refer to the ``select2_generic_foreign_key`` example app in
the ``test_project``.
"""
