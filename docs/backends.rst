Backend Comparison: select2 vs alight
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both backends share the same Django-side base classes
(``BaseQuerySetView``, ``ViewMixin``, ``forward.py``).
They differ in what the view returns and which JS component renders it.

Core difference
===============

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - ``dal_select2``
     - ``dal_alight``
   * - Response format
     - JSON ``{results:[{id, text, selected_text}], pagination:{more}}``
     - HTML fragments ``<div data-value="pk">Label</div>``
   * - JS payload
     - Select2 4.x (~170 KB) + jQuery (via Django admin) + 5 KB DAL glue
     - ``autocomplete-light`` web component (15 KB) + 11 KB DAL adapter.
       **No jQuery.**
   * - Browser API
     - jQuery plugin, ``data-*`` attribute wiring
     - Native Custom Elements v1, no framework

Feature matrix
==============

.. list-table::
   :header-rows: 1
   :widths: 30 12 12 46

   * - Feature
     - select2
     - alight
     - Notes
   * - Single FK
     - yes
     - yes
     - ``ModelSelect2`` / ``ModelAlight``
   * - Multiple M2M
     - yes
     - yes
     - ``ModelSelect2Multiple`` / ``ModelAlightMultiple``
   * - Free list
     - yes
     - yes
     - ``ListSelect2`` / ``ListAlight`` + corresponding views
   * - Tags / comma-separated
     - yes
     - yes
     - ``TagSelect2`` / ``TagAlight``
   * - django-taggit integration
     - yes
     - yes
     - ``TaggitSelect2`` / ``TaggitAlight``
   * - Grouped results
     - yes
     - yes
     - ``Select2GroupQuerySetView`` / ``AlightGroupQuerySetView``
   * - Grouped free list
     - yes
     - yes
     - ``Select2GroupListView`` / ``AlightGroupListView``
   * - Generic FK via queryset-sequence
     - yes
     - yes
     - ``dal_select2_queryset_sequence`` / ``dal_alight_queryset_sequence``
   * - Create on the fly
     - yes
     - yes
     - select2: JSON flag ``create_id:true``; alight: ``<div data-create>`` sentinel
   * - Infinite scroll / pagination
     - yes
     - yes
     - select2: ``pagination.more``; alight: ``<div data-next-page>`` sentinel
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
     - select2: ``data-minimum-input-length``; alight: ``minimum-characters`` attribute
   * - Clear / remove selection
     - yes
     - yes
     - alight uses × buttons in the deck
   * - Client-side local filtering
     - **no**
     - yes
     - alight: ``Alight`` / ``AlightMultiple`` without a ``url`` filter ``<option>``
       elements locally — no server round-trip
   * - Max-choices cap with auto-eviction
     - **no**
     - yes
     - alight: ``max-choices`` attribute; oldest selection is evicted when cap is exceeded
   * - i18n of widget UI strings
     - yes
     - **no**
     - select2 ships 59 locale files; alight hardcodes "Search…", "No result",
       "Create …" in English
   * - Distinct selected-item label
     - yes
     - **no**
     - select2: ``get_selected_result_label()`` / ``data-selected-html``; alight deck
       always shows the same label as the dropdown
   * - Token separators for tags
     - yes
     - **no**
     - select2: ``data-token-separators`` (e.g. type ``,`` to commit); alight requires
       click or Enter
   * - Rich HTML result/selection templates
     - yes
     - partial
     - select2: ``templateResult`` / ``templateSelection`` JS callbacks + ``data-html``;
       alight renders ``get_result_label()`` as raw HTML but has no separate selection
       template

When to use ``dal_select2``
============================

- The project already loads jQuery (Django admin, Bootstrap 3 era stacks) — Select2
  adds zero new dependencies in that context.
- You need full i18n of widget UI strings (59 locales out of the box).
- You need a distinct label in the "selected chip" versus the dropdown item
  (``get_selected_result_label``).
- You need token separators for tag creation (typing ``,`` to commit a tag without
  clicking).
- Results contain rich HTML and require *different* rendering for dropdown vs selection
  display.
- You target browsers or CSP policies that disallow Custom Elements.

When to use ``dal_alight``
===========================

- No jQuery in the stack (modern frontend, HTMX, API-only backend, etc.).
- Minimising JS payload and eliminating third-party dependencies is a priority.
- You want ``max-choices`` enforcement client-side without extra code.
- Some fields use a small static choice list and local filtering avoids an unnecessary
  server round-trip.
- You prefer the server to own result rendering (HTML fragments) rather than templating
  in JS — useful when labels contain Django template logic or server-side permissions.
- You are building a web-component or shadow-DOM ecosystem and need a widget that fits
  naturally as a Custom Element.

Known gaps in ``dal_alight``
=============================

.. note:: These are deliberate trade-offs or deferred features, not bugs.

1. **No i18n** — the three user-visible strings ("Search…", "No result", "Create …")
   are hardcoded in English inside the web component.  A ``labels`` attribute or a
   ``<slot name="no-results">`` override would be the natural extension point.

2. **No** ``selected_text`` — there is no mechanism to show a different label once an
   item is selected.  The deck always shows ``get_result_label()``.  Select2's
   ``get_selected_result_label()`` hook has no alight equivalent yet.

3. **No token separators** — in tag mode the user must click or press Enter to commit a
   tag; typing a separator character does not auto-commit.

Class name mapping
==================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - ``dal_select2``
     - ``dal_alight``
     - Kind
   * - ``Select2QuerySetView``
     - ``AlightQuerySetView``
     - View
   * - ``Select2GroupQuerySetView``
     - ``AlightGroupQuerySetView``
     - View
   * - ``Select2ListView``
     - ``AlightListView``
     - View
   * - ``Select2GroupListView``
     - ``AlightGroupListView``
     - View
   * - ``Select2QuerySetSequenceView``
     - ``AlightQuerySetSequenceView``
     - View (GFK)
   * - ``ModelSelect2``
     - ``ModelAlight``
     - Widget — FK
   * - ``ModelSelect2Multiple``
     - ``ModelAlightMultiple``
     - Widget — M2M
   * - ``Select2``
     - ``Alight``
     - Widget — arbitrary choices, single
   * - ``Select2Multiple``
     - ``AlightMultiple``
     - Widget — arbitrary choices, multiple
   * - ``ListSelect2``
     - ``ListAlight``
     - Widget — list-backed
   * - ``TagSelect2``
     - ``TagAlight``
     - Widget — free-text tags
   * - ``TaggitSelect2``
     - ``TaggitAlight``
     - Widget — django-taggit
   * - ``QuerySetSequenceSelect2``
     - ``QuerySetSequenceAlight``
     - Widget — GFK single
   * - ``QuerySetSequenceSelect2Multiple``
     - ``QuerySetSequenceAlightMultiple``
     - Widget — GFK multiple
   * - ``Select2ListChoiceField``
     - ``AlightListChoiceField``
     - Form field
   * - ``Select2ListCreateChoiceField``
     - ``AlightListCreateChoiceField``
     - Form field
   * - ``Select2GenericForeignKeyModelField``
     - ``AlightGenericForeignKeyModelField``
     - Form field — GFK auto-view
