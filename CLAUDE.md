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
pytest -v --liveserver 127.0.0.1:9999
BROWSER=firefox MOZ_HEADLESS=1 pytest -v   # headless
```
