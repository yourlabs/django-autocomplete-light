Migrating from dal_select2 to dal_alight
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This guide helps you migrate an existing ``dal_select2`` project to
``dal_alight``. It's not a requirement, but it's supposed to be doable.

Why migrate
===========

``dal_select2`` depends on jQuery, which puts the developer in charge of the
JavaScript object lifecycle.  ``dal_alight`` uses native Web Components with no
external library dependency — no jQuery required.

Class name mapping
==================

Replace ``Select2`` with its ``Alight`` counterpart in your views, widgets, and
form fields.

.. list-table:: Views
   :header-rows: 1

   * - ``dal_select2``
     - ``dal_alight``
   * - :py:class:`~dal_select2.views.Select2QuerySetView`
     - :py:class:`~dal_alight.views.AlightQuerySetView`
   * - :py:class:`~dal_select2.views.Select2GroupQuerySetView`
     - :py:class:`~dal_alight.views.AlightGroupQuerySetView`
   * - :py:class:`~dal_select2.views.Select2ListView`
     - :py:class:`~dal_alight.views.AlightListView`
   * - :py:class:`~dal_select2.views.Select2GroupListView`
     - :py:class:`~dal_alight.views.AlightGroupListView`
   * - :py:class:`~dal_select2_queryset_sequence.views.Select2QuerySetSequenceView`
     - :py:class:`~dal_alight_queryset_sequence.views.AlightQuerySetSequenceView`

.. list-table:: Widgets
   :header-rows: 1

   * - ``dal_select2``
     - ``dal_alight``
   * - :py:class:`~dal_select2.widgets.ModelSelect2`
     - :py:class:`~dal_alight.widgets.ModelAlight`
   * - :py:class:`~dal_select2.widgets.ModelSelect2Multiple`
     - :py:class:`~dal_alight.widgets.ModelAlightMultiple`
   * - :py:class:`~dal_select2.widgets.Select2`
     - :py:class:`~dal_alight.widgets.ListAlight`
   * - :py:class:`~dal_select2.widgets.Select2Multiple`
     - :py:class:`~dal_alight.widgets.ModelAlightMultiple` or :py:class:`~dal_alight.widgets.TagAlight`
   * - :py:class:`~dal_select2.widgets.ListSelect2`
     - :py:class:`~dal_alight.widgets.ListAlight`
   * - :py:class:`~dal_select2.widgets.TagSelect2`
     - :py:class:`~dal_alight.widgets.TagAlight`
   * - :py:class:`~dal_select2_taggit.widgets.TaggitSelect2`
     - :py:class:`~dal_alight.widgets.TaggitAlight`
   * - :py:class:`~dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2`
     - :py:class:`~dal_alight_queryset_sequence.widgets.QuerySetSequenceAlight`
   * - :py:class:`~dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2Multiple`
     - :py:class:`~dal_alight_queryset_sequence.widgets.QuerySetSequenceAlightMultiple`

.. list-table:: Form fields
   :header-rows: 1

   * - ``dal_select2``
     - ``dal_alight``
   * - :py:class:`~dal_select2.fields.Select2ListChoiceField`
     - :py:class:`~dal_alight.fields.AlightListChoiceField`
   * - :py:class:`~dal_select2.fields.Select2ListCreateChoiceField`
     - :py:class:`~dal_alight.fields.AlightListCreateChoiceField`
   * - :py:class:`~dal_select2_queryset_sequence.fields.Select2GenericForeignKeyModelField`
     - :py:class:`~dal_alight_queryset_sequence.fields.AlightGenericForeignKeyModelField`

Behavioural differences
========================

- **Response format**: Select2 views return JSON; alight views return HTML fragments.
  Override :py:meth:`~dal.views.BaseQuerySetView.get_result_label` instead of
  ``get_result_label`` + ``get_selected_result_label``.
- **Create**: the POST response returns an HTML label fragment, not ``{"id": …, "text": …}`` JSON.
- **Forwarding**: the ``forward`` widget argument and :py:mod:`dal.forward` helpers work identically.
- **Admin registration**: ``ModelAdmin.form`` assignment works identically.
- **Static files**: replace ``dal_select2`` media with ``dal_alight`` media; jQuery is no longer loaded by the widget.

Changes in 5.1
==============

Since 5.1.0 (see ``CHANGELOG``):

- Widget ``attrs`` apply to the visible search ``<input>``, not a hidden
  ``<select>``.
- ``ListAlight`` now requires a ``url``; client-side local filtering of static
  ``choices`` was removed.  Use ``ListAlight`` with ``AlightListView``, or a
  plain ``<select>`` for tiny static lists.
- The ``change`` event fires on ``<autocomplete-select>``, not a ``<select>``.
- ``Alight`` and ``AlightMultiple`` were removed; use the widget mapping table
  above (``Select2`` → ``ListAlight``; ``Select2Multiple`` →
  ``ModelAlightMultiple`` or ``TagAlight``).
