# Django Autocomplete Light

Bibliothèque Django d'autocomplétion basée sur Select2. Détails dans `.claude/`.

## Structure
- `src/dal/` — noyau : `views.py`, `widgets.py`, `forms.py`, `forward.py`
- `src/dal_select2/` — intégration Select2 : vue principale `Select2QuerySetView`
- `test_project/` — 17 apps de test (unitaires + Selenium/Splinter)

## Flux d'une requête
`GET ?q=…&forward={…}` → `ViewMixin.dispatch()` → `BaseQuerySetView.get_queryset()` → JSON Select2

## Personnalisation courante
Surcharger `get_queryset()`. Configurer `search_fields`, `create_field`, `paginate_by`.
Forwarding : `forward=['country']` sur le widget → `self.forwarded.get('country')` dans la vue.

## Tests
```bash
cd test_project/
pytest -v --liveserver 127.0.0.1:9999
BROWSER=firefox MOZ_HEADLESS=1 pytest -v   # headless
```
