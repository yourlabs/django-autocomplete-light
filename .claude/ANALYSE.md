# Django Autocomplete Light (DAL) — Analyse technique

> Généré à partir de l'exploration du code source (`src/`) et de la structure du projet.

---

## 1. Fonction du module

**Django Autocomplete Light** est une bibliothèque Django qui permet d'ajouter des champs d'autocomplétion dans les formulaires (admin ou frontend custom). Elle repose sur la bibliothèque JavaScript **Select2** pour l'interface côté client et fournit un ensemble de vues, widgets et formulaires côté serveur.

**Cas d'usage principaux :**
- Autocomplétion sur des champs `ForeignKey`, `ManyToManyField`, `OneToOneField`
- Autocomplétion sur des relations génériques (`GenericForeignKey`, `GenericManyToMany`)
- Autocomplétion sur des listes de valeurs statiques ou dynamiques
- Création à la volée d'une nouvelle option depuis le champ de saisie
- Filtrage conditionnel (forwarding) : la valeur d'un champ influence les options d'un autre

---

## 2. Architecture générale

Le projet est découpé en plusieurs sous-packages indépendants dans `src/` :

| Package | Rôle |
|---|---|
| `dal` | Noyau : vues, widgets, formulaires, forward |
| `dal_select2` | Intégration Select2 (widgets, vues, champs) |
| `dal_queryset_sequence` | Support de multiples QuerySets hétérogènes |
| `dal_select2_queryset_sequence` | Select2 + QuerySetSequence combinés |
| `dal_contenttypes` | Support du framework ContentType de Django |
| `dal_genericm2m` | Intégration django-generic-m2m |
| `dal_gm2m` | Intégration django-gm2m |
| `dal_select2_taggit` | Intégration django-taggit |
| `dal_select2_tagging` | Intégration django-tagging |
| `dal_legacy_static` | Fichiers statiques Select2 embarqués (rétrocompat) |

---

## 3. Structure des fichiers

```
src/
├── dal/                            # Noyau de la bibliothèque
│   ├── __init__.py
│   ├── autocomplete.py             # Point d'entrée public (façade d'imports)
│   ├── views.py                    # Vues de base (ViewMixin, BaseQuerySetView)
│   ├── widgets.py                  # Widgets de base (WidgetMixin, QuerySetSelectMixin)
│   ├── forms.py                    # FutureModelForm (gestion avancée des relations)
│   ├── forward.py                  # Déclarations de forwarding (Field, Const, JavaScript, Self)
│   ├── urls.py                     # URL patterns utilitaires
│   ├── apps.py                     # AppConfig
│   ├── static/
│   │   └── autocomplete_light/
│   │       └── autocomplete_light.js   # Librairie JS core (yl namespace)
│   └── test/
│       ├── case.py                 # Classes de test Selenium (AutocompleteTestCase)
│       ├── stories.py              # Scénarios de test réutilisables
│       └── utils.py                # Utilitaires de test
│
├── dal_select2/                    # Intégration Select2
│   ├── views.py                    # Select2ViewMixin, Select2QuerySetView, ...
│   ├── widgets.py                  # Select2WidgetMixin, ModelSelect2, TagSelect2, ...
│   ├── fields.py                   # Select2ListChoiceField, Select2ListCreateChoiceField
│   ├── test.py                     # Select2Story pour tests fonctionnels
│   └── static/
│       └── autocomplete_light/
│           └── select2.js          # Initialisation et config Select2
│
├── dal_queryset_sequence/
│   ├── views.py                    # BaseQuerySetSequenceView
│   └── widgets.py                  # QuerySetSequenceSelectMixin
│
├── dal_select2_queryset_sequence/
│   ├── views.py                    # Select2QuerySetSequenceView
│   └── widgets.py                  # ModelSelect2 multi-queryset
│
├── dal_contenttypes/
│   ├── fields.py                   # ContentTypeField
│   └── widgets.py                  # ContentTypeWidget
│
├── dal_genericm2m/
│   └── fields.py                   # Champs pour generic-m2m
│
├── dal_gm2m/
│   └── fields.py                   # Champs pour gm2m
│
├── dal_select2_taggit/
│   └── widgets.py                  # TaggitSelect2 widget
│
├── dal_select2_tagging/
│   └── widgets.py                  # TaggingSelect2 widget
│
└── dal_legacy_static/
    └── static/                     # Select2 CSS/JS embarqués

test_project/                       # Projet Django de test complet
├── settings.py
├── urls.py
├── select2_foreign_key/            # Tests ForeignKey
├── select2_many_to_many/           # Tests ManyToMany
├── select2_one_to_one/             # Tests OneToOne
├── select2_generic_foreign_key/    # Tests GenericForeignKey
├── select2_generic_m2m/            # Tests Generic M2M
├── linked_data/                    # Tests forwarding (dépendances entre champs)
├── custom_select2/                 # Implémentation custom
├── select2_tagging/                # Tests tagging
├── select2_taggit/                 # Tests taggit
└── select2_outside_admin/          # Tests hors Django admin
```

---

## 4. Implémentation — Flux complet

### 4.1 Côté serveur (Python)

#### Hiérarchie des vues

```
ViewMixin
└── BaseQuerySetView  (dal.views)
    ├── Select2QuerySetView          (dal_select2.views) ← vue principale
    └── Select2GroupQuerySetView     (dal_select2.views)

View + Select2ViewMixin
└── Select2ListView                  (dal_select2.views)
    └── Select2GroupListView
```

#### Hiérarchie des widgets

```
WidgetMixin  (dal.widgets)
├── Select          (+ forms.Select)
├── SelectMultiple  (+ forms.SelectMultiple)
└── QuerySetSelectMixin
    ├── ModelSelect2          (+ Select2WidgetMixin)
    └── ModelSelect2Multiple  (+ Select2WidgetMixin)

Select2WidgetMixin  (dal_select2.widgets)
├── Select2
├── Select2Multiple
├── ListSelect2
└── TagSelect2
```

#### Classes clés

**`dal/views.py` — `ViewMixin`**
- `dispatch()` : parse le JSON `forward` → `self.forwarded` dict, extrait `q` → `self.q`

**`dal/views.py` — `BaseQuerySetView`**
- `get_queryset()` : filtre le QuerySet selon le terme de recherche
- `get_search_results(qs, q)` : implémente la logique de recherche avec préfixes :
  - `^field` → `startswith`
  - `=field` → `exact`
  - `@field` → `search` (full-text)
  - (aucun) → `icontains`
- `post()` : crée un nouvel objet si `create_field` est défini
- `has_add_permission()` : vérifie les droits de création

**`dal_select2/views.py` — `Select2ViewMixin`**
- `render_to_response()` : retourne du JSON au format Select2 `{results, pagination}`
- `get_results()` : formate en `[{id, text, selected_text}, ...]`
- `get_create_option()` : génère l'option "Créer..."

**`dal/widgets.py` — `WidgetMixin`**
- `build_attrs()` : injecte `data-autocomplete-light-url`, `data-autocomplete-light-function`
- `render_forward_conf()` : sérialise la config de forwarding en JSON embarqué dans le HTML

**`dal/forward.py` — Déclarations de forwarding**
- `Field(src, dst=None)` : transmet la valeur d'un autre champ du formulaire
- `Const(val, dst)` : transmet une valeur constante
- `JavaScript(handler, dst=None)` : exécute un handler JS et transmet le résultat
- `Self(dst=None)` : transmet la propre valeur du champ

**`dal/forms.py` — `FutureModelForm`**
- Étend `ModelForm` pour les champs avec relations complexes
- Appelle `field.value_from_object(instance, name)` pour la valeur initiale
- Appelle `field.save_object_data(instance, name, value)` avant sauvegarde
- Appelle `field.save_relation_data(instance, name, value)` après sauvegarde (PK disponible)

---

### 4.2 Côté client (JavaScript)

#### `autocomplete_light.js` (noyau JS)

- Fournit le namespace global `yl`
- `yl.registerFunction(name, fn)` : enregistre une fonction d'initialisation
- `yl.registerForwardHandler(name, fn)` : enregistre un handler de forwarding custom
- `yl.getFormPrefix()` / `yl.getFormPrefixes()` : gestion des préfixes de formsets Django
- Initialise tous les éléments portant `data-autocomplete-light-function` au chargement
- Utilise un `MutationObserver` pour détecter les éléments ajoutés dynamiquement (formsets inline)
- Gère les templates Django formset (`__prefix__`) pour ne pas initialiser les gabarits

#### `select2.js` (intégration Select2)

- Enregistre la fonction `'select2'` via `yl.registerFunction`
- Configure Select2 en mode AJAX :
  - URL : `data-autocomplete-light-url`
  - Paramètres envoyés : `q` (terme), `page` (pagination), `forward` (JSON des valeurs transmises)
  - Réponse attendue : `{results: [{id, text, selected_text}], pagination: {more}}`
- Délai de 250 ms avant requête (throttling)
- Support du mode tags (`data-tags`)
- Support HTML riche dans les résultats (`data-html`)
- Gère la création via POST sur sélection de l'option "Create..."
- Support i18n via `data-autocomplete-light-language`

---

### 4.3 Flux d'une requête d'autocomplétion

```
[Utilisateur tape dans le champ]
        │
        ▼
[Select2] envoie GET ?q=terme&page=1&forward={"field":"value"}
        │
        ▼
[ViewMixin.dispatch()]
   → parse forward JSON → self.forwarded
   → extrait q → self.q
        │
        ▼
[BaseQuerySetView.get_queryset()]
   → filtre selon search_fields et self.q
   → filtre éventuellement selon self.forwarded
        │
        ▼
[Select2ViewMixin.render_to_response()]
   → formate en JSON Select2
   → retourne {results: [...], pagination: {more: bool}}
        │
        ▼
[Select2] affiche les options dans le dropdown
```

---

### 4.4 Flux de création d'un nouvel objet

```
[Utilisateur sélectionne "Créer X"]
        │
        ▼
[select2.js] envoie POST avec le texte saisi
        │
        ▼
[BaseQuerySetView.post()]
   → vérifie has_add_permission()
   → appelle create_object(text)
   → retourne {id, text}
        │
        ▼
[Select2] ajoute la nouvelle option et la sélectionne
```

---

## 5. Comment utiliser DAL (usage type)

### Étape 1 — Créer la vue d'autocomplétion

```python
# urls.py / views.py
from dal import autocomplete

class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Country.objects.none()
        qs = Country.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
```

### Étape 2 — Enregistrer l'URL

```python
# urls.py
path('country-autocomplete/', CountryAutocomplete.as_view(), name='country-autocomplete'),
```

### Étape 3 — Wirer le widget dans le formulaire

```python
from dal import autocomplete
from django import forms

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['country']
        widgets = {
            'country': autocomplete.ModelSelect2(url='country-autocomplete')
        }
```

### Étape 4 — Forwarding (filtrage conditionnel)

```python
widgets = {
    'city': autocomplete.ModelSelect2(
        url='city-autocomplete',
        forward=['country']  # transmet la valeur du champ 'country' au backend
    )
}
```

Côté vue :
```python
def get_queryset(self):
    country_id = self.forwarded.get('country', None)
    qs = City.objects.filter(country_id=country_id)
    ...
```

---

## 6. Tests

### Structure

- **Tests unitaires** : `test_forms.py`, `test_views.py` dans chaque app du `test_project`
- **Tests fonctionnels** (Selenium/Splinter) : `test_functional.py`
- **Classes de base** : `dal.test.case.AutocompleteTestCase` avec `AdminMixin`, `OptionMixin`
- **Scénarios réutilisables** : `dal.test.stories` (`SelectOption`, `InlineSelectOption`, `RenameOption`, `AddAnotherOption`)
- **Support Select2** : `dal_select2.test.Select2Story` avec sélecteurs CSS pour Select2

### Apps de test couvertes

| App | Scénario testé |
|---|---|
| `select2_foreign_key` | ForeignKey simple |
| `select2_many_to_many` | ManyToMany |
| `select2_one_to_one` | OneToOne |
| `select2_generic_foreign_key` | GenericForeignKey |
| `select2_generic_m2m` | Generic M2M |
| `linked_data` | Forwarding / dépendances entre champs |
| `custom_select2` | Widget/vue custom |
| `select2_tagging` / `select2_taggit` | Création de tags |
| `select2_outside_admin` | Utilisation hors Django admin |

---

## 7. Points d'extension notables

- **Surcharger `get_queryset()`** : filtrage custom, permissions, contexte
- **Surcharger `get_result_label()`** : affichage custom dans la liste
- **Surcharger `get_result_value()`** : valeur custom soumise dans le formulaire
- **`create_field`** : nom du champ à utiliser pour créer un objet à la volée
- **`search_fields`** : liste des champs Django ORM à chercher (avec préfixes `^=@`)
- **`split_words`** : découpage du terme de recherche mot par mot
- **`paginate_by`** : taille de page pour la pagination des résultats
- **`yl.registerForwardHandler()`** : handler JS custom pour le forwarding
- **`FutureModelForm`** : pour les champs avec cycle de vie de sauvegarde complexe (tags, generic M2M)
