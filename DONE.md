# DONE — alight-cleanup

## Dark mode

Added dark mode support to `dal_alight` via CSS custom properties and an optional JS toggle.

- Refactored `autocomplete-light.css` to use CSS custom properties in `:root` for all hardcoded colors
- Added `@media (prefers-color-scheme: dark)` block with dark values
- Added `html.alight-dark-mode` class-based override for JS toggle
- Added `AutocompleteLightDarkMode` JS object to `dal-django.js` with `toggle()`, `initialize()`, localStorage persistence, and system preference listener

**Deviation from plan:** CSS changes were kept in the main repo only (`src/dal_alight/static/dal_alight/autocomplete-light.css`). The submodule copy was intentionally not modified — dark mode changes in the submodule were reverted to keep the submodule at upstream HEAD.

Commits: `3f37f365`, `1124cac7`, `3265172c`

## Untrack db.sqlite3

Removed `test_project/db.sqlite3` from git tracking and prevented future sqlite files from being committed.

- Ran `git rm --cached test_project/db.sqlite3`
- Added wildcard patterns to `.gitignore`: `*.sqlite3`, `*.sqlite`, `*.db`

Commit: `5312239f`
