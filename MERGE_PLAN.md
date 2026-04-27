# Merge Plan — PR #1332 "New dal_alight backend"

Source: https://github.com/yourlabs/django-autocomplete-light/pull/1332
Priority: LOWER
Treatment: manual port — do NOT cherry-pick, do NOT apply the diff directly.
The PR was authored against v3.9.7; current master is v4.0.0.

---

## Overview

Introduces `dal_alight`, a new optional autocomplete backend built on the
`autocomplete-light` web component (no Select2 dependency). Users opt in via
`INSTALLED_APPS`. All existing Select2 code is untouched.

The implementation works through standard Django web component slots:
- A `<autocomplete-select>` outer web component wraps the inner `<select>` widget.
- Slots `select`, `deck`, and `input` are filled by the widget render output.
- The autocomplete view returns HTML fragments (not JSON).

Render call stack (MRO: ModelAlight → QuerySetSelectMixin → WidgetMixin →
AlightWidgetMixin → forms.Select):
1. `WidgetMixin.render()` is called first (first in MRO with a `render` method).
2. It calls `super().render()` → `AlightWidgetMixin.render()`.
3. `AlightWidgetMixin.render()` sets `attrs['slot'] = 'select'`, calls `super().render()`
   → `forms.Select.render()` → returns `<select slot="select">…</select>`.
4. `AlightWidgetMixin.render()` appends `<div slot="deck">` and `<autocomplete-select-input>`,
   returns all three concatenated.
5. Back in `WidgetMixin.render()`: appends forward conf, then wraps everything in
   `<autocomplete-select>…</autocomplete-select>` via the new `component` attribute.

Final HTML structure (correct for web component slots):
```html
<autocomplete-select>
  <select slot="select">…</select>
  <div slot="deck"></div>
  <autocomplete-select-input slot="input" url="…">
    <input name="…-input" slot="input" class="vTextField" />
  </autocomplete-select-input>
  [forward conf script tag]
</autocomplete-select>
```

---

## What to skip entirely

- `.github/workflows/release.yml` — references deleted `setup.py` and a
  `yourlabs/python` Docker image; current project uses `pyproject.toml` and a
  different release process. Discard completely.
- `setup.py` bump — file no longer exists.
- `package.json` / `package-lock.json` version bumps to `3.9.8rc25` — current
  master is 4.0.0. Discard.
- `CHANGELOG` hunk — removes blank lines from a 3.9.x entry; master's CHANGELOG
  has a 4.0.0/4.0.1 header at the top. Discard.
- `release.sh` `-eux` change — trivial, unrelated, evaluate separately.

---

## Step-by-step implementation

### Step 1 — `src/dal/widgets.py`: add `component` wrapping in `render()`

Current code (around line 154, after our PR #1358 changes):
```python
        conf = self.render_forward_conf(field_id)
        return mark_safe(widget + conf)
```

Replace with:
```python
        conf = self.render_forward_conf(field_id)
        html = widget + conf
        if getattr(self, 'component', None):
            html = f'<{self.component}>{html}</{self.component}>'
        return mark_safe(html)
```

No conflict expected. Backward-compatible: existing widgets don't define `component`,
so `getattr` returns `None` and nothing changes for them.

---

### Step 2 — `src/dal/autocomplete.py`: add `dal_alight` conditional imports

Before the `if _installed('dal_select2'):` block (currently line 33), insert:
```python
if _installed('dal_alight'):
    from dal_alight.widgets import ModelAlight
    from dal_alight.views import AlightQuerySetView
```

`_installed` is already defined above. No conflict expected.

---

### Step 3 — Create `src/dal_alight/` package

Create each file exactly as in the PR, with the fixes noted below.

**`src/dal_alight/__init__.py`** — empty file.

**`src/dal_alight/apps.py`** — verbatim from PR:
```python
from django.apps import AppConfig

class DalAlightConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dal_alight"
```

**`src/dal_alight/admin.py`** — verbatim (empty placeholder).

**`src/dal_alight/models.py`** — verbatim (empty placeholder).

**`src/dal_alight/migrations/__init__.py`** — empty file.

**`src/dal_alight/tests.py`** — verbatim (empty placeholder).

**`src/dal_alight/views.py`** — port from PR with two fixes:

Fix 1: The comment says "Return a JSON response in Select2 format" — wrong copy-paste.
Fix 2: `HttpResponse(html)` where `html` is a list emits no charset; normalise with
an explicit `content_type` and join the list first.

```python
from django import http
from dal.views import BaseQuerySetView


class AlightQuerySetView(BaseQuerySetView):
    def render_to_response(self, context):
        """Return an HTML fragment response for autocomplete-light."""
        html = []
        for result in context['object_list']:
            html.append(
                f'<div data-value="{self.get_result_value(result)}">'
                f'{self.get_result_label(result)}'
                f'</div>'
            )
        return http.HttpResponse(
            ''.join(html),
            content_type='text/html; charset=utf-8',
        )
```

**`src/dal_alight/widgets.py`** — port from PR, cleaned up formatting:
```python
from django import forms
from dal.widgets import QuerySetSelectMixin


class AlightWidgetMixin:
    component = 'autocomplete-select'

    @property
    def media(self):
        return forms.Media(
            css=dict(all=['dal_alight/autocomplete-light.css']),
            js=['dal_alight/autocomplete-light.js'],
        )

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        self.choices.field.empty_label = None
        attrs = attrs or {}
        attrs.setdefault('slot', 'select')
        widget = super().render(name, value, attrs=attrs, renderer=renderer, **kwargs)
        deck = '<div slot="deck"></div>'
        input = (
            f'<autocomplete-select-input slot="input" url="{self.url}">'
            f'<input name="{name}-input" slot="input" class="vTextField" />'
            f'</autocomplete-select-input>'
        )
        return widget + deck + input


class ModelAlight(QuerySetSelectMixin, AlightWidgetMixin, forms.Select):
    pass
```

Note: `AlightWidgetMixin.render()` sets `self.choices.field.empty_label = None` on
every render call. This mutates the field object at render time. Fine in normal
usage (one form instance, one render); mirrors how Select2 handles this elsewhere.

---

### Step 4 — Git submodule for static files

The JS/CSS for the web component lives in an external git repo. Register it as a
submodule:

```bash
git submodule add https://yourlabs.io/oss/autocomplete-light.git \
    src/dal_alight/static/dal_alight
cd src/dal_alight/static/dal_alight && git checkout bd9d8ba4 && cd -
git add .gitmodules src/dal_alight/static/dal_alight
```

**CI impact — REQUIRED fix**: `ci.yml` uses `actions/checkout@v6` without
`submodules: true`. The submodule won't clone in CI, so static files will be
missing. Add `submodules: true` to all three checkout steps in `ci.yml`:

```yaml
- uses: actions/checkout@v6
  with:
    submodules: true
```

---

### Step 5 — `test_project/alight_foreign_key/` test app

Create all files verbatim from the PR:

- `models.py` — `TModel` with self-referential FKs `test` and `for_inline`.
- `forms.py` — `TForm(ModelForm)` using `autocomplete.ModelAlight(url='alight_fk')`.
- `admin.py` — `TestAdmin` with `TestInline`.
- `urls.py` — one URL routing to `AlightQuerySetView.as_view(model=TModel)`.
- `migrations/__init__.py` — empty.
- `migrations/0001_initial.py` — DO NOT use the PR's version (generated against
  Django 4.2.1). After registering the app in settings, run:
  ```bash
  python manage.py makemigrations alight_foreign_key
  ```
  to get a clean Django 5.2+ migration.

---

### Step 6 — `test_project/settings/base.py`

Add to `INSTALLED_APPS` in two places:

Under `# test apps` (before `'select2_foreign_key'`):
```python
'alight_foreign_key',
```

Under `# Enable plugins` (before `'dal_select2'`):
```python
'dal_alight',
```

The current `base.py` still has `taggit`/`select2_taggit`/`nested_admin` entries —
the list structure is unchanged from what the PR expected, so no manual reconciliation
needed beyond the two insertions above.

---

### Step 7 — `test_project/urls.py`

Add before the `select2_foreign_key` URL:
```python
url(r'^alight_foreign_key/', include('alight_foreign_key.urls')),
```

`include` is already imported. No conflicts.

---

### Step 8 — `tox.ini`: add `alight_foreign_key` to test run

The tox `commands` line explicitly enumerates test apps. Add `alight_foreign_key`
to the list so its view is exercised by CI:

```
pytest -v --cov --liveserver 127.0.0.1:9999 {posargs} alight_foreign_key \
    secure_data rename_forward select2_foreign_key ...
```

---

### Step 9 — `pyproject.toml`: no changes needed

`[tool.setuptools.packages.find]` uses `where = ["src"]`, auto-discovering all
packages under `src/`. `dal_alight` will be picked up automatically.

---

### Step 10 — `CHANGELOG`

Add an entry under 4.0.1 (bump to 4.0.2 if 4.0.1 is already released):
```
    - #1332   Add dal_alight: new autocomplete backend based on the
              autocomplete-light web component (no Select2 dependency).
              Opt-in via INSTALLED_APPS = [..., 'dal_alight'].
```

---

## Known issues / risks

| Issue | Severity | Resolution |
|---|---|---|
| CI checkout doesn't init submodule | HIGH | Add `submodules: true` to `ci.yml` (Step 4) |
| `AlightQuerySetView` comment says "JSON/Select2" | LOW | Fixed in Step 3 |
| `AlightQuerySetView` returns list not joined string | LOW | Fixed in Step 3 |
| Migration generated against Django 4.2.1 | LOW | Regenerate in Step 5 |
| `alight_foreign_key` missing from tox commands | MEDIUM | Add in Step 8 |
| No unit tests for `AlightQuerySetView` or `ModelAlight` | MEDIUM | Add after port |
| External submodule on `yourlabs.io` — CI reliability risk | MEDIUM | Monitor; vendor if unstable |
