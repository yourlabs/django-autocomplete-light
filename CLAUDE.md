# Django Autocomplete Light

Django autocomplete library based on Select2.

## Structure
- `src/dal/` — core: `views.py`, `widgets.py`, `forms.py`, `forward.py`
- `src/dal_select2/` — Select2 integration: main view `Select2QuerySetView`
- `test_project/` — 17 test apps (unit + Selenium/Splinter)

## Request flow
`GET ?q=…&forward={…}` → `ViewMixin.dispatch()` → `BaseQuerySetView.get_queryset()` → Select2 JSON

## Common customisation
Override `get_queryset()`. Configure `search_fields`, `create_field`, `paginate_by`.
Forwarding: `forward=['country']` on the widget → `self.forwarded.get('country')` in the view.

## Tests
```bash
cd test_project/
tox -e py314-dj52 -- --ignore-glob='**/test_functional.py'           # unit (-n auto)
tox -e py314-dj52 -- --ignore-glob='**/test_units.py' --ignore-glob='**/test_views.py' --ignore-glob='**/test_forms.py'  # browser (-n auto)
BROWSER=firefox tox -e py314-dj52 -- --ignore-glob='**/test_units.py' --ignore-glob='**/test_views.py' --ignore-glob='**/test_forms.py' --splinter-headless
```
