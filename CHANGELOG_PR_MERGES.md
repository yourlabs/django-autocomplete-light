# PR Merges Changelog

Integration of external contributions into the modernisation branch.
**3 files changed, 4 commits.**

---

## Commit baseline

| Hash | Message |
|---|---|
| `31b9801` | changed to english *(last commit before merges)* |

---

## Commit 1 — Build system (`520e350`)

**Source :** PR #1383 by dimbleby — with corrections.

### `release.sh`
- `python setup.py sdist` → `python -m build` (direct setup.py invocation deprecated since setuptools 58.3)
- `twine upload dist/...tar.gz` → `twine upload dist/...*` — publishes both sdist **and** wheel (the original PR omitted this fix)

---

## Commit 2 — Select2 initial values (`253d2d5`)

**Source :** PR #1393 by musanaeem — rewritten with corrections.

### `src/dal_select2/widgets.py`
- Added `Select2InitialRenderMixin` — injects missing initial values into choices at render time so pre-selected values appear correctly on edit forms (fixes issue #1076)
- Applied mixin to `ListSelect2`, `Select2Multiple`, `ModelSelect2`, `ModelSelect2Multiple`
- Removed `ast.literal_eval` string parsing present in the original PR (not a valid Django form flow, masked an upstream issue)

### `test_project/tests/test_widgets.py`
- Replaced `mock.Mock()` view with `DummyView` (a real `View` subclass)
- `import mock` → `from unittest import mock` (stdlib since Python 3.3)
- Added 2 unit tests for `Select2InitialRenderMixin` (`ListSelect2` single value, `Select2Multiple` multiple values)

---

## Commit 3 — Documentation (`09e0712`)

### `docs/tutorial.rst`
- Added section *"Initial values on edit forms"* after "Set form widgets"
- Explains why values appear blank on edit, and that all DAL Select2 widgets handle it automatically via `Select2InitialRenderMixin`

---

## Commit 4 — Ruff fix (`4fa1ee7`)

### `test_project/tests/test_widgets.py`
- Removed leftover `from unittest import mock` import (unused after `mock.Mock()` was replaced — caught by ruff F401/I001)

---

## PRs closed as obsolete

| # | Title | Reason |
|---|---|---|
| #1385 | super(..) -> super() | Fully covered by the modernisation PR (#1407) |
| #1405, #1403, #1402, #1401, #1399, #1397, #1391, #1390, #1389, #1387, #1384, #1379, #1377, #1376, #1375, #1374, #1372, #1371, #1369, #1367, #1366, #1365, #1364, #1363, #1362, #1361 | [Snyk] various security upgrades | All target Django 3.2.x / old deps superseded by the 5.2+ upgrade |
