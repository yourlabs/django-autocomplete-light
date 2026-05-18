# DONE — alight-cleanup

## Add outside-admin view for dal_alight

Completed the `alight_outside_admin` app to match parity with `select2_outside_admin`.

- `views.py`: switched from `alight_foreign_key` to `alight_many_to_many` models/forms to showcase M2M autocomplete (data fixtures already provided by `select2_many_to_many`'s AppConfig)
- `templates/base.html`: added nav link `{% url 'alight_outside_admin' %}` alongside the select2 link
- `alight_outside_admin/test_functional.py`: added 3 Selenium tests — page loads with `<autocomplete-select>`, option selection, form submission

## Dark mode

Added dark mode support to `dal_alight` via CSS custom properties and an optional JS toggle.

- Refactored `autocomplete-light.css` to use CSS custom properties in `:root` for all hardcoded colors
- Added `@media (prefers-color-scheme: dark)` block with dark values
- Added `html.alight-dark-mode` class-based override for JS toggle
- Added `AutocompleteLightDarkMode` JS object to `dal-django.js` with `toggle()`, `initialize()`, localStorage persistence, and system preference listener

**Deviation from plan:** CSS changes were kept in the main repo only (`src/dal_alight/static/dal_alight/autocomplete-light.css`). The submodule copy was intentionally not modified — dark mode changes in the submodule were reverted to keep the submodule at upstream HEAD.

Commits: `3f37f365`, `1124cac7`, `3265172c`

## Admin global search bar

Added a global search bar to the Django admin topbar that searches across all admin-registered models and navigates to the selected object's change page.

- `AdminGlobalSearchView` in `test_project/views.py` — searches all admin-registered models; auto-detects first `CharField`/`TextField` as fallback when no `search_fields` defined; respects staff permission; returns HTML fragments with `data-url` pointing to each object's change page
- URL registered at `/admin-search/` as `admin-global-search`
- `test_project/templates/admin/base_site.html` — overrides admin header to embed `<autocomplete-light>` in the topbar; CSS `order` trick places it visually between branding (left) and user-tools (right)
- On `autocompleteChoiceSelected` event, JS navigates to `choice.dataset.url`

Commit: (this session)

## List behavior: fix tag loss on update

Fixed selected tags reappearing in the dropdown after a list refresh.

- `AutocompleteSelectInput.receive()`: filters already-selected items from server HTML before rendering the dropdown
- `AutocompleteSelect.reconcileState()`: extracted deck↔select sync logic from `connectedCallback()` into a reusable method
- `AutocompleteSelect.connectedCallback()`: early-return with `reconcileState()` when `data-bound` is set (handles form re-render / reconnect)
- Added `test_tags_survive_list_refresh` and `test_tags_dont_appear_in_dropdown_after_selection` to `alight_tag` test suite

Commit: `3d22ad94`

## Untrack db.sqlite3

Removed `test_project/db.sqlite3` from git tracking and prevented future sqlite files from being committed.

- Ran `git rm --cached test_project/db.sqlite3`
- Added wildcard patterns to `.gitignore`: `*.sqlite3`, `*.sqlite`, `*.db`

Commit: `5312239f`

## Verify taggit integration

Verified `TaggitAlight` / `AlightQuerySetView` integration is production-ready (5/5 tests green, parity with `dal_select2_taggit`). Closed the three remaining gaps:

- Added `AlightTagAutocompleteView` convenience base class to `src/dal_alight/views.py` — overrides `get_result_value()` to return `result.name`; exported from `dal.autocomplete`
- Added `test_project/alight_taggit/test_edge_cases.py` — 4 new form-level tests: unicode tag names, HTML special-char tag names, 99-char tag names, tag removal
- Extended `docs/taggit.rst` with Alight view and form examples (using `AlightTagAutocompleteView` and `TaggitAlight`)

## Static files management

Followed the STATICFILES_DIRS / collectstatic pattern.

- `test_project/settings/base.py`: added `STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'static')]`
- Created `test_project/static/js/` and moved three scattered per-app JS files into it: `js_handlers.js`, `linked_data.js`, `t_select2.js`
- Updated references in `select2_forward_different_fields/forms.py`, `alight_forward_different_fields/forms.py`, `select2_linked_data/forms.py`, `custom_select2/widgets.py` to use `js/` prefix
- Deleted old per-app `static/` JS files (4 files removed from git)
- Added `test_project/public/` to `.gitignore` (collectstatic output — not a source artifact)
- Ran `git rm --cached -r test_project/public/` to untrack 239 previously-committed build files
- Verified `python manage.py collectstatic --noinput` completes cleanly (246 files, no errors)

**Note:** `select2_rename_forward/static/linked_data.js` was intentionally left in place — it has subtly different content from `select2_linked_data`'s copy and was not listed in the TODO.
