# Merge Plan — PR #1332 "New dal_alight backend"

Source: https://github.com/yourlabs/django-autocomplete-light/pull/1332
Priority: LOWER
Conflict risk: HIGH — treat as a port, not a clean merge

---

## What it does

Introduces a new optional autocomplete backend `dal_alight` built on the
`autocomplete-light` web component library (no Select2 JS/CSS dependency). Users
opt in by adding `'dal_alight'` to `INSTALLED_APPS` and using `autocomplete.ModelAlight`
as their widget.

**User-facing changes:**
- New widget `ModelAlight` renders a `<autocomplete-select>` web component with an
  `<autocomplete-select-input>` inner element — zero Select2 dependency.
- New view `AlightQuerySetView` returns HTML fragments (not JSON) to populate the
  dropdown.

**Internal changes:**
- New package `src/dal_alight/`: `views.py`, `widgets.py`, `apps.py`, `admin.py`,
  `models.py`, `migrations/`, `tests.py`.
- `src/dal/widgets.py` `WidgetMixin.render()`: adds a `component` wrapping hook —
  if `self.component` is set, the rendered HTML is wrapped in
  `<component>...</component>` tags.
- `src/dal/autocomplete.py`: conditional `if _installed('dal_alight'):` import block
  exports `ModelAlight` and `AlightQuerySetView`.
- New test app `test_project/alight_foreign_key/` with self-referential `TModel`,
  `TForm`, admin, and URL config.
- External git submodule at `src/dal_alight/static/dal_alight` pointing to
  `yourlabs.io/oss/autocomplete-light` (commit `bd9d8ba4`).

---

## How to merge it

**Important:** The PR was authored against v3.9.7. Current master is v4.0.0 with
`pyproject.toml` replacing `setup.py`, Django 5.2+ only, and significant restructuring.
Do NOT apply version bumps, CI workflow, or CHANGELOG hunks.

### Step 1 — Skip entirely

These hunks from the PR must be discarded:
- Any change to `setup.py` (file no longer exists).
- `package.json` / `package-lock.json` version bumps to `3.9.8rc25`.
- `.github/workflows/release.yml` (check if master already has one; if so, do not
  overwrite; if not, evaluate separately).
- `CHANGELOG` hunk (master has a 4.0.0 entry at the top; hunk won't apply cleanly).
- `release.sh` `-eux` fix (minor; evaluate independently).

### Step 2 — `src/dal/widgets.py`

In `WidgetMixin.render()` (currently around line 115–125), find the final
`return mark_safe(widget + conf)` line and replace with:

```python
result = mark_safe(widget + conf)
component = getattr(self, 'component', None)
if component:
    result = mark_safe(f'<{component}>{result}</{component}>')
return result
```

This is isolated and backward-compatible (`component` is not set on any existing
widget). No conflicts expected.

### Step 3 — `src/dal/autocomplete.py`

Before the `if _installed('dal_select2'):` block (currently around line 34), insert:

```python
if _installed('dal_alight'):
    from dal_alight.views import AlightQuerySetView
    from dal_alight.widgets import ModelAlight
```

Verify the `_installed` helper is still present in the file before applying.
No conflicts expected.

### Step 4 — Add `src/dal_alight/` package

Copy all files from the PR branch manually:
- `src/dal_alight/__init__.py`
- `src/dal_alight/apps.py`
- `src/dal_alight/admin.py`
- `src/dal_alight/models.py`
- `src/dal_alight/migrations/`
- `src/dal_alight/tests.py`
- `src/dal_alight/views.py`
- `src/dal_alight/widgets.py`

Then register the git submodule:
```bash
git submodule add https://yourlabs.io/oss/autocomplete-light.git \
    src/dal_alight/static/dal_alight
cd src/dal_alight/static/dal_alight && git checkout bd9d8ba4 && cd -
```

### Step 5 — `test_project/settings/base.py`

Add to `INSTALLED_APPS`:
```python
'dal_alight',
'alight_foreign_key',
```

Verify the current list manually before patching — the structure has changed since
the PR was authored (e.g., `dal_select2_taggit` and `taggit` have been removed).

### Step 6 — `test_project/urls.py`

Add:
```python
path('alight_foreign_key/', include('alight_foreign_key.urls')),
```

`include` is already imported. No conflicts expected.

### Step 7 — Add `test_project/alight_foreign_key/`

Copy the entire directory from the PR branch:
- `models.py` (self-referential `TModel`)
- `forms.py` (`TForm` using `ModelAlight`)
- `admin.py`
- `urls.py`
- `views.py`
- `migrations/`

### Step 8 — `pyproject.toml` (REQUIRED MANUAL FIXUP)

The PR predates `pyproject.toml`. Add `dal_alight` to the package list so it ships
in the wheel. Under `[tool.setuptools.packages.find]` or equivalent, ensure
`src/dal_alight` is included. Also check `MANIFEST.in` if still used.

Example addition to `pyproject.toml`:
```toml
[tool.setuptools.packages.find]
where = ["src"]
```
(If `where = ["src"]` is already set, all packages under `src/` are auto-discovered
and no explicit addition is needed — verify.)

---

## Consequences

- **Conflict risk: HIGH.** Must be treated as a manual port, not a cherry-pick or
  clean merge. Each section above must be applied individually.
- **Regression risk on `WidgetMixin.render()`**: LOW. The `component` guard uses
  `getattr(self, 'component', None)` so all existing widgets are unaffected. Confirm
  with an existing unit test that the base render path is unchanged.
- **Test coverage needed:**
  - `AlightQuerySetView`: at minimum a unit test verifying `200` response and correct
    HTML fragment structure.
  - `ModelAlight.render()`: render test with and without a forwarded value.
  - `WidgetMixin.render()`: confirm `component=None` leaves output unchanged.
- **Known issue — `AlightQuerySetView.render_to_response()`**: returns
  `HttpResponse(html)` where `html` is a list of strings. Django accepts iterables
  but the content-type will be `text/html` with no charset declaration. Normalise to
  `HttpResponse(''.join(html), content_type='text/html; charset=utf-8')`.
- **Known issue — `AlightWidgetMixin.render()`**: sets
  `self.choices.field.empty_label = None` directly on the field object. This may
  conflict with the `Select2InitialRenderMixin` pattern added in recent commits.
  Audit before merging.
- **Django 5.2 compatibility**: the web component approach is untested against
  Django 5.2+ — run the full test suite after porting.
- **Git submodule reliability**: the external submodule on `yourlabs.io` is a CI
  reliability concern. Consider vendoring the built JS/CSS instead (as is done for
  Select2) if the host is not guaranteed stable.
- **Breaking change: none** for existing users. `dal_alight` is fully opt-in via
  `INSTALLED_APPS`.
