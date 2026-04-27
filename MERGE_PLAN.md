# Merge Plan — PR #1358 "Clone forwards"

Source: https://github.com/yourlabs/django-autocomplete-light/pull/1358
Priority: HIGH
Conflict risk: LOW

---

## What it does

Fixes a bug where the `forward` list on `WidgetMixin` is shared across all form
instances that inherit from a common base class. Because Django deep-copies widget
instances from class-level field definitions rather than re-instantiating them, every
form subclass that appends to `widget.forward` in `__init__` silently mutates the
same list object — polluting sibling and subsequent forms.

Two changes in the PR:

- `src/dal/widgets.py` — `WidgetMixin.__init__`: copy the forward list defensively
  instead of assigning the caller's list by reference; add `__deepcopy__` so that
  widget clones also get their own copy of `.forward`.
- `test_project/tests/test_widgets.py` — new test `test_forwards_are_cloned` that
  instantiates two subclasses of a shared base form (each appending a different
  `forward.Const`) and asserts each form sees only its own entry.

---

## How to merge it

### Step 1 — `src/dal/widgets.py`

Location: `WidgetMixin.__init__`, currently around line 46.

Current code:
```python
self.forward = forward or []
```

Replace with a guarded copy so the list is never shared by reference:
```python
self.forward = list(forward) if forward else []
```

Note: the PR writes `list(forward).copy()` — the `.copy()` call is redundant since
`list()` already copies. Use `list(forward)` only.

Then insert a `__deepcopy__` method immediately after `__init__` (before
`build_attrs`):
```python
def __deepcopy__(self, memo):
    obj = super().__deepcopy__(memo)
    obj.forward = self.forward[:]
    return obj
```

Caveat: `Widget.__deepcopy__` exists in Django 4.x+ but not all versions define it.
Test against Django 4.2 and 5.x. If `super().__deepcopy__()` raises `AttributeError`,
fall back to:
```python
import copy
obj = copy.copy(self)
obj.forward = self.forward[:]
return obj
```

No merge conflict expected here.

### Step 2 — `test_project/tests/test_widgets.py`

Three imports need to be added near the top of the file:
```python
from django.contrib.auth import get_user_model
from dal import forward
from dal_select2.widgets import ModelSelect2
```

Check that none are already present before adding. The import block may have been
reorganised by the ruff linting commit (e2f5d2fd) — add them manually rather than
applying the raw diff hunk.

Then add the new test at the bottom of `WidgetMixinTest` (or as a standalone
`TestCase` subclass):
```python
def test_forwards_are_cloned(self):
    User = get_user_model()

    class BaseForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username']
            widgets = {
                'username': ModelSelect2(url='autocomplete')
            }

    class FormA(BaseForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.forward.append(forward.Const('a', 'key'))

    class FormB(BaseForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.forward.append(forward.Const('b', 'key'))

    form_a = FormA()
    form_b = FormB()
    self.assertEqual(len(form_a.fields['username'].widget.forward), 1)
    self.assertEqual(len(form_b.fields['username'].widget.forward), 1)
    self.assertEqual(form_a.fields['username'].widget.forward[0].val, 'a')
    self.assertEqual(form_b.fields['username'].widget.forward[0].val, 'b')
```

### Step 3 — Cherry-pick strategy

The PR is a single commit (`cc3f7f5`). Try:
```bash
git cherry-pick cc3f7f5
```

A conflict is expected only in the import section of `test_widgets.py`. Resolve as
described in Step 2, then `git cherry-pick --continue`.

---

## Consequences

- **Regression risk: LOW.** The fix only affects the copy/clone path. Single-
  instantiation usage is completely unaffected.
- **`__deepcopy__` compatibility**: must be verified against Django 4.2 and 5.x
  before merging. See the fallback pattern in Step 1.
- **Breaking change: none.** The `forward` list contract is unchanged — mutation
  still works, it just no longer leaks across form instances.
- **Unlikely breakage**: any project that intentionally relies on the leaking
  behaviour (sharing a mutable forward list across form subclasses by mutating the
  base widget at runtime) would break. This is clearly a bug, not a feature.
- **Test infrastructure**: the new test uses `get_user_model()` and `ModelSelect2`,
  so it requires a configured `AUTH_USER_MODEL` and DB access — consistent with the
  existing `TestCase` subclasses in the file. No extra fixtures needed.
