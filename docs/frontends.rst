Frontend Comparison: alight vs select2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both frontends share the same Django-side base classes
(``BaseQuerySetView``, ``ViewMixin``, ``forward.py``).
They differ in what the view returns and which JS component renders it.

Core difference
===============

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - ``dal_alight``
     - ``dal_select2``
   * - Response format
     - HTML fragments ``<div data-value="pk">Label</div>``
     - JSON ``{results:[{id, text, selected_text}], pagination:{more}}``
   * - JS payload
     - ``autocomplete-light`` web component (15 KB) + 11 KB DAL adapter.
       **No jQuery.**
     - Select2 4.x (~170 KB) + jQuery (via Django admin) + 5 KB DAL glue
   * - Browser API
     - Native Custom Elements v1, no framework
     - jQuery plugin, ``data-*`` attribute wiring

Feature matrix
==============

.. list-table::
   :header-rows: 1
   :widths: 30 12 12 46

   * - Feature
     - alight
     - select2
     - Notes
   * - Single FK
     - yes
     - yes
     - ``ModelAlight`` / ``ModelSelect2``
   * - Multiple M2M
     - yes
     - yes
     - ``ModelAlightMultiple`` / ``ModelSelect2Multiple``
   * - Free list
     - yes
     - yes
     - ``ListAlight`` + corresponding views / ``ListSelect2``
   * - Tags / comma-separated
     - yes
     - yes
     - ``TagAlight`` / ``TagSelect2``
   * - django-taggit integration
     - yes
     - yes
     - ``TaggitAlight`` / ``TaggitSelect2``
   * - Grouped results
     - yes
     - yes
     - ``AlightGroupQuerySetView`` / ``Select2GroupQuerySetView``
   * - Grouped free list
     - yes
     - yes
     - ``AlightGroupListView`` / ``Select2GroupListView``
   * - Generic FK via queryset-sequence
     - yes
     - yes
     - ``dal_alight_queryset_sequence`` / ``dal_select2_queryset_sequence``
   * - Create on the fly
     - yes
     - yes
     - alight: ``<div data-create>`` sentinel; select2: JSON flag ``create_id:true``
   * - Infinite scroll / pagination
     - yes
     - yes
     - alight: ``<div data-next-page>`` sentinel; select2: ``pagination.more``
   * - Field forwarding
     - yes
     - yes
     - Both use the same ``forward.py``; alight adapter is vanilla JS
   * - Django admin popup sync
     - yes
     - yes
     - alight patches ``dismissAddRelatedObjectPopup`` in ``dal-django.js``
   * - Minimum input length
     - yes
     - yes
     - alight: ``minimum-characters`` attribute; select2: ``data-minimum-input-length``
   * - Clear / remove selection
     - yes
     - yes
     - alight uses × buttons in the deck
   * - Client-side local filtering
     - **no**
     - yes
     - alight choice widgets require a ``url``; values are submitted via hidden inputs
   * - Max-choices cap with auto-eviction
     - yes
     - **no**
     - alight: ``max-choices`` attribute; oldest selection is evicted when cap is exceeded
   * - i18n of widget UI strings
     - planned
     - yes
     - alight UI strings can be overridden via custom attributes or Django's i18n
       machinery; select2 ships 59 locale files
   * - Distinct selected-item label
     - **no**
     - yes
     - alight deck always shows the same label as the dropdown; select2:
       ``get_selected_result_label()`` / ``data-selected-html``
   * - Token separators for tags
     - **no**
     - yes
     - alight requires click or Enter; select2: ``data-token-separators``
       (e.g. type ``,`` to commit)
   * - Rich HTML result/selection templates
     - partial
     - yes
     - alight renders ``get_result_label()`` as raw HTML but has no separate selection
       template; select2: ``templateResult`` / ``templateSelection`` JS callbacks +
       ``data-html``

When to use ``dal_alight``
===========================

- No jQuery in the stack (modern frontend, HTMX, API-only server-side, etc.).
- Minimising JS payload and eliminating third-party dependencies is a priority.
- You want ``max-choices`` enforcement client-side without extra code.
- You prefer the server to own result rendering (HTML fragments) rather than templating
  in JS — useful when labels contain Django template logic or server-side permissions.
- You are building a web-component or shadow-DOM ecosystem and need a widget that fits
  naturally as a Custom Element.

Known gaps in ``dal_alight``
=============================

.. note:: These are deliberate trade-offs or deferred features, not bugs.

1. **i18n** — the three user-visible strings ("Search…", "No result", "Create …")
   can be overridden via custom HTML attributes on the widget, or rendered server-side
   through Django's i18n machinery.

2. **No** ``selected_text`` — there is no mechanism to show a different label once an
   item is selected.  The deck always shows ``get_result_label()``.  Select2's
   ``get_selected_result_label()`` hook has no alight equivalent yet.

3. **No token separators** — in tag mode the user must click or press Enter to commit a
   tag; typing a separator character does not auto-commit.

When to use ``dal_select2``
============================

Use ``dal_select2`` when you require one of these specific features not yet in
``dal_alight``:

- A distinct label in the "selected chip" versus the dropdown item
  (``get_selected_result_label``).
- Token separators for tag creation (typing ``,`` to commit a tag without
  clicking).
- Results with rich HTML requiring *different* rendering for dropdown vs selection
  display.
- Browsers or CSP policies that disallow Custom Elements.

Class name mapping
==================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - ``dal_alight``
     - ``dal_select2``
     - Kind
   * - :py:class:`~dal_alight.views.AlightQuerySetView`
     - :py:class:`~dal_select2.views.Select2QuerySetView`
     - View
   * - :py:class:`~dal_alight.views.AlightGroupQuerySetView`
     - :py:class:`~dal_select2.views.Select2GroupQuerySetView`
     - View
   * - :py:class:`~dal_alight.views.AlightListView`
     - :py:class:`~dal_select2.views.Select2ListView`
     - View
   * - :py:class:`~dal_alight.views.AlightGroupListView`
     - :py:class:`~dal_select2.views.Select2GroupListView`
     - View
   * - :py:class:`~dal_alight_queryset_sequence.views.AlightQuerySetSequenceView`
     - :py:class:`~dal_select2_queryset_sequence.views.Select2QuerySetSequenceView`
     - View (GFK)
   * - :py:class:`~dal_alight.widgets.ModelAlight`
     - :py:class:`~dal_select2.widgets.ModelSelect2`
     - Widget — FK
   * - :py:class:`~dal_alight.widgets.ModelAlightMultiple`
     - :py:class:`~dal_select2.widgets.ModelSelect2Multiple`
     - Widget — M2M
   * - :py:class:`~dal_alight.widgets.ListAlight`
     - :py:class:`~dal_select2.widgets.ListSelect2`
     - Widget — list-backed
   * - :py:class:`~dal_alight.widgets.TagAlight`
     - :py:class:`~dal_select2.widgets.TagSelect2`
     - Widget — free-text tags
   * - :py:class:`~dal_alight.widgets.TaggitAlight`
     - :py:class:`~dal_select2_taggit.widgets.TaggitSelect2`
     - Widget — django-taggit
   * - :py:class:`~dal_alight_queryset_sequence.widgets.QuerySetSequenceAlight`
     - :py:class:`~dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2`
     - Widget — GFK single
   * - :py:class:`~dal_alight_queryset_sequence.widgets.QuerySetSequenceAlightMultiple`
     - :py:class:`~dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2Multiple`
     - Widget — GFK multiple
   * - :py:class:`~dal_alight.fields.AlightListChoiceField`
     - :py:class:`~dal_select2.fields.Select2ListChoiceField`
     - Form field
   * - :py:class:`~dal_alight.fields.AlightListCreateChoiceField`
     - :py:class:`~dal_select2.fields.Select2ListCreateChoiceField`
     - Form field
   * - :py:class:`~dal_alight_queryset_sequence.fields.AlightGenericForeignKeyModelField`
     - :py:class:`~dal_select2_queryset_sequence.fields.Select2GenericForeignKeyModelField`
     - Form field — GFK auto-view
