# TODO — alight-cleanup

- [ ] Dark mode
  - Files to modify:
    - `src/dal_alight/static/dal_alight/autocomplete-light.css` (main)
    - `src/dal_alight/static/dal_alight/component/autocomplete_light/static/autocomplete_light/autocomplete-light.css` (keep in sync)
    - `src/dal_alight/static/dal_alight/dal-django.js` (optional JS toggle)
  - Step 1: Refactor CSS — introduce CSS custom properties in `:root` for all hardcoded colors:
    ```css
    :root {
      --autocomplete-light-bg: white;
      --autocomplete-light-border: #d4d4d4;
      --autocomplete-light-border-light: #eee;
      --autocomplete-light-highlight-bg: #f5f5f5;
      --autocomplete-light-text: rgba(0,0,0,.87);
      --autocomplete-light-text-muted: #999;
      --autocomplete-light-text-secondary: #666;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --autocomplete-light-bg: #1e1e1e;
        --autocomplete-light-border: #444;
        --autocomplete-light-border-light: #333;
        --autocomplete-light-highlight-bg: #333;
        --autocomplete-light-text: rgba(255,255,255,.87);
        --autocomplete-light-text-muted: #b0b0b0;
        --autocomplete-light-text-secondary: #999;
      }
    }
    /* Class-based override for JS toggle */
    html.alight-dark-mode { /* same dark values */ }
    ```
  - Step 2: Replace all hardcoded color values in both CSS files with the new variables
  - Step 3 (optional): Add `AutocompleteLightDarkMode` JS object to `dal-django.js` with `toggle()`, `initialize()`, localStorage persistence, and system preference listener
  - Step 4: Test with DevTools → Rendering → Emulate `prefers-color-scheme: dark/light`; test JS toggle via console
  - Verify WCAG AA contrast (4.5:1) for text on background in both modes
- [ ] Untrack db.sqlite3 from git
  - Current state: `test_project/db.sqlite3` is tracked (binary, ~9512 bytes, modified); .gitignore has no sqlite entries
  - Step 1: `git rm --cached test_project/db.sqlite3`
  - Step 2: Add to `.gitignore` (recommended: wildcard pattern)
    ```
    # SQLite databases
    *.sqlite3
    *.sqlite
    *.db
    ```
  - Step 3: `git add .gitignore && git commit -m "chore: untrack db.sqlite3 and add sqlite to .gitignore"`
  - Step 4: Verify with `git ls-files | grep sqlite3` (should return nothing)
- [ ] Search bar: fix object display
  - Root cause: dropdown result HTML (`choice.innerHTML`) is reused as-is for the selected deck; no separate path for deck vs dropdown display; initial render (widget) and search results (view) use different code paths
  - Files to modify:
    - `src/dal_alight/views.py` — `AlightQuerySetView.render_to_response()` result HTML generation
    - `src/dal_alight/static/dal_alight/autocomplete-light.js` — `choiceSelect()` line 438 (`option.innerHTML = choice.innerHTML`)
    - `src/dal/views.py` — `BaseQuerySetView.get_result_label()` base hook
    - `src/dal_alight/widgets.py` — `AlightInitialRenderMixin` initial deck render
  - Step 1: Add `get_selected_result_label()` hook to `BaseQuerySetView` (defaults to `get_result_label()`) — lets views return a compact label for the deck separately from the dropdown HTML
  - Step 2: In `AlightQuerySetView.render_to_response()`, add a `data-label` attribute to each result `<div>` containing the deck label:
    ```python
    format_html('<div data-value="{}" data-label="{}">{}</div>', pk, deck_label, dropdown_html)
    ```
  - Step 3: In `autocomplete-light.js` `choiceSelect()`, use `choice.dataset.label` (if present) for `option.innerHTML` instead of `choice.innerHTML`
  - Step 4: Unify initial render — `AlightInitialRenderMixin` should produce options whose text matches `get_selected_result_label()` output
  - Step 5: Test with edit forms (initial render), new selections, and multi-select deck
- [ ] List behavior: fix tag loss on update
  - Root cause: `AutocompleteLight.receive()` replaces `this.box.innerHTML` on every list refresh; no re-sync between hidden `<select>` and visible deck after refresh; already-selected tags can reappear in dropdown
  - Files to modify: `src/dal_alight/static/dal_alight/autocomplete-light.js`
  - Fix 1 — Filter already-selected items from server results: override `receive()` in `AutocompleteSelectInput`, parse response HTML, remove `[data-value]` divs whose value is already in `option[selected]`, then call `super.receive(ev)`
  - Fix 2 — Add `reconcileState()` method to `AutocompleteSelect`:
    - Ensure every `option[selected]` has a deck item (add missing ones)
    - Ensure every deck item has a corresponding `option[selected]`
    - Call after each `receive()` and after `choiceUnselect()`
  - Fix 3 — Handle form re-render: in `connectedCallback()`, detect if component was already bound (`data-bound` attribute) and call `reconcileState()` instead of full re-init
  - Key vulnerable lines: `receive()` line 204 (`this.box.innerHTML = ev.target.response`), `connectedCallback()` lines 350-373, `download()` lines 307-324
  - Tests to add in `test_project/alight_tag/test_functional.py`:
    - `test_tags_survive_list_refresh` — select a tag, type to refresh list, verify tag still in deck
    - `test_tags_dont_appear_in_dropdown_after_selection` — verify selected tags are filtered from results
    - `test_tags_persist_on_form_validation_error` — submit with error, verify deck intact after re-render
- [ ] Verify taggit integration
  - Current state: `TaggitAlight` widget exists in `src/dal_alight/widgets.py` (lines 205-216), exported via `dal.autocomplete`; `test_project/alight_taggit/` has 5 tests (3 form + 2 functional) — **all passing**; feature parity with `dal_select2_taggit` confirmed
  - Verdict: core integration is production-ready, no critical fixes needed
  - Remaining gaps (optional):
    1. `docs/taggit.rst` still shows only select2 examples — add alight equivalent (view with `get_result_value()`, form with `TaggitAlight`)
    2. No edge-case tests: unicode tag names, tags with HTML special chars, very long tags, tag removal — add `test_project/alight_taggit/test_edge_cases.py`
    3. No `AlightTagAutocompleteView` convenience base class (optional symmetry with select2)
  - Verification steps to run:
    ```bash
    cd test_project && pytest alight_taggit/ -v   # should be 5/5 green
    pytest select2_taggit/ -v                     # compare parity
    ```
- [ ] Add outside-admin view for dal_alight
  - Current state: `test_project/alight_outside_admin/` already exists (urls, views, template, apps.py) and is registered in settings/urls — but is incomplete
  - Gaps vs `select2_outside_admin`:
    1. `apps.py` missing `post_migrate` fixtures signal → no test data on fresh migrate
    2. Template may use wrong formset IDs and doesn't add a nav link in `base.html`
    3. No functional tests
  - Step 1: `alight_outside_admin/apps.py` — add `post_migrate.connect(fixtures, sender=self)` in `ready()` (match select2_outside_admin pattern)
  - Step 2: Verify `views.py` — currently uses `alight_foreign_key` models/forms; consider switching to `alight_many_to_many` to better showcase M2M autocomplete
  - Step 3: Fix template `alight_outside_admin.html` — update formset management JS IDs to match `alight_foreign_key_tmodel_set-*`, add descriptive headings, ensure `{{ form.media }}` is in footer (Alpine.js loads automatically via widget media)
  - Step 4: `templates/base.html` — add nav link `{% url 'alight_outside_admin' %}` alongside the select2_outside_admin link
  - Step 5 (optional): Add `test_project/alight_outside_admin/test_functional.py` — test page loads, widget renders `<autocomplete-select>`, form submission saves data
  - Note: No special Alpine.js init needed — `{{ form.media }}` handles it via dal_alight web components
- [ ] Static files management: follow STATICFILES_DIRS / collectstatic pattern (ref: yourlabs.org/posts/2012-08-28-surviving-djangocontribstaticfiles-or-how-to-manage-static-files-with-django/)
  - Current gaps: `STATICFILES_DIRS` not set in `test_project/settings/base.py`; test-app JS files scattered across app `static/` dirs; `STATIC_ROOT` (`test_project/public/static/`) contains manually committed non-asset files (md, py, json from the dal_alight component)
  - Templates already use `{% static %}` — no changes needed there
  - Step 1: `test_project/settings/base.py` — add after `STATIC_ROOT`:
    ```python
    STATICFILES_DIRS = [
        os.path.join(PROJECT_ROOT, 'static'),
    ]
    ```
  - Step 2: Create `test_project/static/js/` and move scattered test JS into it:
    - `select2_forward_different_fields/static/js_handlers.js` → `test_project/static/js/`
    - `select2_linked_data/static/linked_data.js` → `test_project/static/js/`
    - `custom_select2/static/t_select2.js` → `test_project/static/js/`
  - Step 3: Clean `STATIC_ROOT` — remove non-asset files (*.md, *.py, package.json, etc.) that leaked in from the dal_alight component; add `test_project/public/` to `.gitignore`
  - Step 4: Verify `python manage.py collectstatic --noinput` runs clean and all pages load
  - Note: `MANIFEST.in` already includes `src/**/*.css/js` — no change needed
