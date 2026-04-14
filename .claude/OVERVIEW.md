# Django Autocomplete Light — Contexte projet

Bibliothèque Django d'autocomplétion basée sur **Select2**. Documentation détaillée dans `.claude/`.

## Architecture

Plusieurs sous-packages dans `src/` :

| Package | Rôle |
|---|---|
| `dal` | Noyau : vues, widgets, formulaires, forward |
| `dal_select2` | Intégration Select2 (vue principale : `Select2QuerySetView`) |
| `dal_queryset_sequence` | QuerySets hétérogènes |
| `dal_contenttypes` | Support ContentType |
| `dal_genericm2m` / `dal_gm2m` | Relations génériques |
| `dal_select2_taggit` / `dal_select2_tagging` | Tags |

## Fichiers clés

```
src/dal/
  autocomplete.py      # Point d'entrée public (imports façade)
  views.py             # ViewMixin, BaseQuerySetView
  widgets.py           # WidgetMixin, QuerySetSelectMixin
  forms.py             # FutureModelForm
  forward.py           # Field, Const, JavaScript, Self

src/dal_select2/
  views.py             # Select2ViewMixin, Select2QuerySetView
  widgets.py           # ModelSelect2, ModelSelect2Multiple, TagSelect2
  fields.py            # Select2ListChoiceField

src/dal/static/autocomplete_light/autocomplete_light.js   # Core JS (namespace yl)
src/dal_select2/static/autocomplete_light/select2.js      # Init Select2 + AJAX
```

## Flux d'une requête

```
Utilisateur tape → Select2 envoie GET ?q=…&forward={…}
  → ViewMixin.dispatch()         parse forward → self.forwarded, self.q
  → BaseQuerySetView.get_queryset()   filtre le QS
  → Select2ViewMixin.render_to_response()  retourne JSON {results, pagination}
```

## Points d'extension courants

- `get_queryset()` — filtrage custom, permissions, contexte
- `get_result_label()` / `get_result_value()` — affichage et valeur custom
- `create_field` — création d'objet à la volée (POST)
- `search_fields` — champs ORM avec préfixes `^` `=` `@`
- `paginate_by` — taille de page
- `forward` sur le widget — transmet des valeurs d'autres champs au backend

## Forwarding

```python
# Widget
widgets = {'city': autocomplete.ModelSelect2(url='city-ac', forward=['country'])}

# Vue
def get_queryset(self):
    return City.objects.filter(country_id=self.forwarded.get('country'))
```

Classes forward disponibles : `Field(src, dst)`, `Const(val, dst)`, `JavaScript(handler, dst)`, `Self(dst)`.

## Tests

Les tests sont dans `test_project/`. Deux types :
- **Unitaires** : `pytest` + `django.test.TestCase` (`test_forms.py`, `test_views.py`)
- **Fonctionnels** : `pytest` + Selenium/Splinter (`test_functional.py`)

### Lancer les tests

```bash
cd test_project/
pytest -v --liveserver 127.0.0.1:9999          # tous
pytest select2_foreign_key/ -v                  # une app
BROWSER=firefox MOZ_HEADLESS=1 pytest -v        # headless
pytest --cov --cov-report=html                  # avec couverture
```

### Infrastructure de test (classes de base)

```
Select2Story          → sélecteurs CSS Select2
AdminMixin            → URLs admin
OptionMixin           → create_option() avec UUID unique
AutocompleteTestCase  → navigateur Selenium, get/click/enter_text/assert_*
```

Scénarios réutilisables (`dal.test.stories`) : `SelectOption`, `CreateOption`, `InlineSelectOption`, `RenameOption`, `AddAnotherOption`, `MultipleMixin`.

### Apps de test (17)

| App | Ce qui est testé |
|---|---|
| `select2_foreign_key` | FK : select, inline, add-another, rename, unselect |
| `select2_many_to_many` | M2M : création + sélection simultanées |
| `select2_one_to_one` | OneToOne + validation (slug) |
| `select2_generic_foreign_key` | GFK, format valeur `ctype-pk-id` |
| `select2_generic_m2m` / `select2_gm2m` | Generic M2M, types mixtes |
| `linked_data` | Forwarding, filtrage conditionnel, robustesse JSON |
| `secure_data` | Filtrage par propriétaire (sécurité) |
| `select2_list` | Listes statiques, vues groupées |
| `select2_taggit` / `select2_tagging` | Tags, multi-mots |
| `select2_nestedadmin` | Inline imbriqué, vérification XHR |
| `tests` | Widgets, i18n, rendu forward |

## FutureModelForm

À utiliser à la place de `ModelForm` pour les champs avec relations complexes (tags, GFK, generic M2M). Gère `value_from_object`, `save_object_data`, `save_relation_data`.
