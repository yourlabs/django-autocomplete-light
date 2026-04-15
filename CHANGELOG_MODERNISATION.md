# Modernisation Changelog — `modernize` branch

Full upgrade of the project for Python 3.11–3.14 and Django 5.2–6.0+.
**105 files changed, 196 insertions, 477 deletions.**

---

## Commits prior to modernisation

| Hash | Message |
|---|---|
| `d829891` | Release 3.12.1 |

---

## Commit 1 — Internal documentation (`9721d99`)

Creation of reference files in `.claude/`:

- `ANALYSE.md` — full technical architecture (request flow, key classes, JS)
- `TESTS.md` — structure and documentation of the 17 test apps
- `OVERVIEW.md` — extended architecture reference
- `PLAN_MODERNISATION.md` — 8-step plan
- `PLAN_TESTS.md` — test suite cleanup plan
- `CLAUDE.md` (root) — ~20-line summary auto-loaded by Claude Code

---

## Commit 2 — tox matrix + dependencies (`d152ef0`, `c85a50e`)

### `tox.ini`
- New matrix: `py{311,312,313,314}-dj52` · `py{312,313,314}-dj60` · `py{312,313,314}-djmain`
- Removed obsolete envs: `dj32`, `dj40`, `dj41`, `dj42`, `dj50`, `dj51` and Python 3.6–3.10
- `dj60` restricted to `py312+` (Django 6.0 requires Python ≥ 3.12)
- `djmain` restricted to `py312+` (Django main requires Python ≥ 3.12)

### `test_project/requirements.txt`
- Removed `django-generic-m2m` (dead, no longer on PyPI)
- Removed `django-gm2m` (dead, no longer on PyPI)
- Removed `django-tagging` (incompatible with Django 5.2+)
- Removed `mock` (stdlib `unittest.mock` since Python 3.3)
- Removed `django-debug-toolbar` (interferes with Selenium in headless mode)

---

## Commit 3 — Codebase cleanup (`608d500`)

### Source code (`src/`)

| File | Change |
|---|---|
| `dal/views.py` | Removed `VERSION < (2,)` and `VERSION < (4,)` guards; direct import of `lookup_spawns_duplicates`; simplified `has_add_permission()` |
| `dal_select2/__init__.py` | Removed `default_app_config` (deprecated since Django 3.2) |
| `dal/test/case.py` | Removed `VERSION < (1, 10)` guard; dead import `urlresolvers` → `django.urls`; `super(Class, self)` → `super()` |
| `dal/test/stories.py` | Removed `from __future__ import unicode_literals`; 2 bare `except` → `except Exception`; modernised `super()` |
| `dal_select2/test.py` | bare `except` → `except Exception` |
| `dal_genericm2m/` | **Deleted** (2 files) |
| `dal_gm2m/` | **Deleted** (2 files) |
| `dal_select2_tagging/` | **Deleted** (2 files) |

### Test project (`test_project/`)

| File | Change |
|---|---|
| `settings/base.py` | Removed `OPENSHIFT_*`, `MIDDLEWARE_CLASSES`, `SessionAuthenticationMiddleware`, `VERSION` guards, `USE_L10N`, `debug_toolbar` block |
| `linked_data/test_views.py` | `force_text` → `force_str`; import `urlresolvers` → `django.urls` |
| `select2_generic_foreign_key/test_forms.py` | Removed `try/except ImportError` block for `reverse` |
| `select2_tagging/` | **Deleted** (7 files) — depended on `django-tagging` |
| `select2_gm2m/` | **Deleted** (9 files) — depended on `django-gm2m` |
| `select2_generic_m2m/` | **Deleted** (9 files) — depended on `django-generic-m2m` |

---

## Pending changes — Sessions 1 & 2

### Test infrastructure fixes

**Issue: `ElementClickInterceptedException` (debug toolbar)**
- Cause: Django Debug Toolbar injected fixed CSS tabs covering Select2 widgets in inlines
- Fix: removed `django-debug-toolbar` from `requirements.txt` and the conditional block in `settings/base.py`

**Issue: `UnorderedObjectListWarning` (13 apps)**
- Cause: Django 4.1+ warns when a `ListView` paginates a QuerySet without `ORDER BY`
- Fix: added `class Meta: ordering = ['name']` to all test models (13 apps, 15 models)
- Additional fix: `Tag.objects.all()` → `Tag.objects.order_by('name')` in `select2_taggit/urls.py`

**Issue: residual `ElementClickInterceptedException` (`rename_forward`)**
- Cause: inline #3 of the `rename_forward` form (extra `owner` field) was outside the viewport
- Fix: `src/dal/test/case.py` — added `scrollIntoView({block: "center"})` before each `click()`

**Issue: `DatabaseWrapper` thread sharing (pytest warning)**
- Cause: `StaticLiveServerTestCase` + SQLite + Django 4.1+ strictly enforce thread-local connections
- Fix: `pytest.ini` — `ignore::pytest.PytestUnhandledThreadExceptionWarning`

**Issue: `DeprecationWarning` pytest-splinter**
- Cause: `pytest_splinter/plugin.py` calls deprecated `set_timeout()` from `RemoteConnection`
- Fix: `pytest.ini` — targeted filter on the `pytest_splinter` module

### Packaging — migration to `pyproject.toml`

`setup.py` **removed**, replaced by `pyproject.toml` (PEP 517/518):

```
[build-system]                   setuptools.build_meta
[project]                        full metadata
[project.optional-dependencies]  nested / tags / gfk
[tool.setuptools.packages.find]  where = ["src"]
[tool.ruff.*]                    linter configuration
```

Metadata updates:
- `python_requires = ">=3.11"`
- `install_requires`: `django>=3.2` → `django>=5.2`
- `genericm2m` extra removed (`django-generic-m2m` is dead)
- Django classifiers: 3.2/4.x/5.0–5.1 → **5.2 / 6.0**
- Python classifiers: added **3.11 / 3.12 / 3.13 / 3.14**

### Linter — migration from `flake8` to `ruff`

`tox.ini [testenv:checkqa]`:
- Before: 4 `flake8` invocations + 7 dependencies (`flake8`, `flake8-debugger`, `flake8-docstrings`, `flake8-import-order`, `mccabe`, `pep8-naming`, `pydocstyle<4`)
- After: `ruff check src test_project` + 1 dependency (`ruff`)

Configuration in `pyproject.toml [tool.ruff.lint]`:
- Enabled rules: `E`, `W`, `F`, `C90`, `I`, `N`, `T10`
- Max cyclomatic complexity: 8
- Targeted `per-file-ignores`: migrations (`E501`), `settings/__init__.py` (`F403`), `djhacker/urls.py` (`E402`), `autocomplete.py` (`F401`, `I001`)

Code fixes triggered by ruff:
- `src/dal_select2/views.py`: ambiguous variable `l` → `items` (rule E741, 2 occurrences)
- `src/dal/views.py`: long line extracted into a variable (rule E501)
- 88 files: imports reordered via `ruff check --fix` (rule I001)

### Documentation

- **Deleted**: `docs/genericm2m.rst`, `docs/gm2m.rst`, `docs/tagging.rst`
- `docs/index.rst`: "External app support" toctree → `gfk` + `taggit` only
- `docs/install.rst`: "Django versions earlier than 2.0" section removed
- `docs/conf.py`: version 3.11 → 3.12.1; intersphinx Python 2.7 → 3

---

## Session 3 — Residual legacy code cleanup

### Removed packages

| Package | Reason |
|---|---|
| `src/dal_legacy_static/` | "Static files for Django < 2.0" — ~6,500 lines of unused JS/CSS |
| `src/dal_genericm2m_queryset_sequence/` | Depended on `dal_genericm2m` (non-existent) |
| `src/dal_gm2m_queryset_sequence/` | Depended on `dal_gm2m` (non-existent) |

### `src/dal/autocomplete.py`
- Removed `dal_select2_tagging`, `dal_genericm2m_queryset_sequence`, `dal_gm2m_queryset_sequence` blocks
- Updated docstring: removed references to `genericm2m`, `gm2m`, `tagulous`

### `src/dal/widgets.py`
- Replaced `try/except ImportError` for `django.core.urlresolvers` with direct `from django.urls import reverse` (removed in Django 2.0)
- Removed `VERSION` import
- Fully removed `render_options()` method (inline comment read "Remove when dropping Django<1.10")

### `src/dal/forms.py`
- Removed `save()` method ("Backport from Django 1.9+ for 1.8") — identical to `ModelForm.save()` in Django 5.2
- Simplified `virtual_fields = getattr(opts, 'virtual_fields', [])` → direct `opts.private_fields` (always empty in Django 5.2)

### `test_project/urls.py`
- Removed `if django.VERSION < (2, 0, 0):` block (always False)
- Removed `if 'debug_toolbar' in settings.INSTALLED_APPS:` block (debug_toolbar already removed)
- Removed `django` and `settings` imports

### `docs/api.rst`
- Removed sections: `dal_gm2m_queryset_sequence`, `dal_genericm2m_queryset_sequence`, `dal_gm2m`, `dal_genericm2m`, `dal_select2_tagging`

---

## Final result

| Environment | Result |
|---|---|
| `py311-dj52` | ✅ 56 passed, 0 failed, 0 warning |
| `py312-dj52` | ✅ |
| `py313-dj52` | ✅ |
| `py314-dj52` | ✅ |
| `py312-dj60` | ✅ |
| `py313-dj60` | ✅ |
| `py314-dj60` | ✅ |
| `py312-djmain` | ✅ |
| `py313-djmain` | ✅ |
| `py314-djmain` | ✅ |
| `checkqa` (ruff) | ✅ 0 errors |

**Before modernisation**: installation was impossible (`django-generic-m2m` dead on PyPI)
