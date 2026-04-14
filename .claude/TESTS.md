# Django Autocomplete Light — Structure des tests

---

## 1. Vue d'ensemble

Les tests sont organisés en deux niveaux :

- **Infrastructure de test** (`src/dal/test/`, `src/dal_select2/test.py`) : classes de base, scénarios réutilisables, sélecteurs CSS
- **Projet de test** (`test_project/`) : 17 applications Django, chacune couvrant un cas d'usage précis

**Deux types de tests coexistent :**

| Type | Outil | Ce que ça teste |
|---|---|---|
| Tests unitaires | `pytest` + `django.test.TestCase` | Logique des vues, formulaires, widgets, champs |
| Tests fonctionnels | `pytest` + Selenium via Splinter | Comportement complet dans le navigateur |

---

## 2. Configuration de l'exécution

### `test_project/conftest.py`

```python
@pytest.fixture(scope='session')
def splinter_webdriver():
    return os.environ.get('BROWSER', 'firefox')
```

Naviguateur Selenium configurable via la variable d'environnement `BROWSER`. Par défaut : Firefox.

### `test_project/pytest.ini`

```ini
addopts = --nomigrations --create-db --reuse-db
DJANGO_SETTINGS_MODULE = settings.base
django_debug_mode = true
```

- Les migrations sont ignorées (base créée directement depuis les modèles)
- La base est réutilisée entre les runs pour accélérer les tests

### `tox.ini`

Matrice de tests couvrant Python 3.6–3.13 + PyPy × Django 3.2–5.1 + branche main.

Commande : `pytest -v --cov --liveserver 127.0.0.1:9999`

### Lancement

```bash
cd test_project/

# Tous les tests
pytest -v --liveserver 127.0.0.1:9999

# Une app spécifique
pytest select2_foreign_key/ -v

# Un test précis
pytest select2_foreign_key/test_functional.py::AdminForeignKeyTestCase::test_can_select_option

# Headless
BROWSER=firefox MOZ_HEADLESS=1 pytest -v

# Avec couverture
pytest --cov --cov-report=html
```

---

## 3. Infrastructure de test

### 3.1 `src/dal/test/case.py` — Classes de base

#### `AutocompleteTestCase(StaticLiveServerTestCase)`

Classe de base pour tous les tests fonctionnels Selenium.

| Méthode | Rôle |
|---|---|
| `get(url)` | Ouvre l'URL sur le serveur live ; gère la connexion admin automatiquement |
| `click(selector)` | Clique sur un élément CSS |
| `enter_text(selector, text)` | Saisit du texte dans un champ |
| `assert_visible(selector)` | Vérifie qu'un élément est visible |
| `assert_not_visible(selector)` | Vérifie qu'un élément est absent |
| `wait_script()` | Appelé après navigation (surchargé dans Select2Story) |

Décorée avec `@pytest.mark.usefixtures('cls_browser')` — le navigateur est partagé à l'échelle de la classe.

#### `AdminMixin`

Fournit les helpers pour naviguer dans l'admin Django.

| Méthode | Rôle |
|---|---|
| `get_modeladmin_url(action, **kwargs)` | Construit l'URL d'une action admin (add, change, delete…) |
| `fill_name()` | Remplit le champ `name` avec une valeur unique |

#### `OptionMixin`

Crée des instances de test avec des noms uniques (UUID).

| Méthode | Rôle |
|---|---|
| `create_option()` | Crée une instance via `get_or_create`, retourne `(option, created)` |

#### `ContentTypeOptionMixin(OptionMixin)`

Variante pour les modèles avec `GenericForeignKey`.

| Méthode | Rôle |
|---|---|
| `create_option()` | Retourne `(option, ContentType)` |

---

### 3.2 `src/dal/test/stories.py` — Scénarios réutilisables

Les *stories* encapsulent des scénarios d'interaction complets, réutilisables par toutes les apps de test.

#### `BaseStory`

Classe de base. Prend en paramètre : `case`, `field_name`, et des sélecteurs CSS (avec valeurs par défaut issues de `case`).

| Méthode | Rôle |
|---|---|
| `find_option(text)` | Trouve une option dans le dropdown (retry 3s via tenacity) |
| `get_label()` / `assert_label(text)` | Lit et vérifie le label sélectionné |
| `get_value()` / `assert_value(value)` | Lit et vérifie la valeur du champ |
| `assert_selection(value, label)` | Vérifie valeur + label en même temps |
| `assert_selection_persists(value, label)` | Vérifie, soumet le formulaire, vérifie à nouveau |
| `assert_suggestion_labels_are(expected)` | Vérifie la liste de suggestions affichées |
| `toggle_autocomplete()` | Ouvre/ferme le dropdown |
| `get_suggestions()` | Retourne `[(value, text), ...]` pour les suggestions visibles |
| `submit()` | Soumet le formulaire et attend le rechargement |
| `switch_to_popup()` / `switch_to_main()` | Gère les fenêtres popup (add-another) |

#### Scénarios concrets (héritent de `BaseStory`)

| Classe | Scénario couvert |
|---|---|
| `SelectOption` | Sélectionner une option existante, effacer la sélection |
| `InlineSelectOption(SelectOption)` | Même chose dans un inline model admin (gère le numéro de ligne) |
| `RenameOption(SelectOption)` | Ouvrir le popup de renommage, modifier, sauvegarder |
| `AddAnotherOption` | Créer une option via le popup "add another" |
| `CreateOption(SelectOption)` | Créer une option à la volée depuis le champ |
| `MultipleMixin` | Sélection multiple : `get_labels()`, `get_values()`, `assert_labels()`, `assert_values()` |
| `SelectOptionMultiple` | `SelectOption` + `MultipleMixin` |
| `InlineSelectOptionMultiple` | `InlineSelectOption` + `MultipleMixin` |
| `CreateOptionMultiple` | `CreateOption` + `MultipleMixin` |

---

### 3.3 `src/dal/test/utils.py` — Fixtures de données

#### `Fixtures`

Peuple la base avec 49 objets nommés `"test N"` via le signal `post_migrate`.

#### `OwnedFixtures(Fixtures)`

Idem, mais crée deux utilisateurs (`test` et `other`) et associe les objets à leur propriétaire respectif. Utilisé pour tester le forwarding et le filtrage par owner.

---

### 3.4 `src/dal_select2/test.py` — Sélecteurs Select2

#### `Select2Story`

Mixin fournissant les sélecteurs CSS de Select2 à utiliser dans les tests.

| Attribut | Sélecteur |
|---|---|
| `clear_selector` | `.select2-selection__clear` |
| `dropdown_selector` | `.select2-dropdown` |
| `input_selector` | `.select2-search__field` |
| `label_selector` | `.select2-selection__rendered` |
| `labels_selector` | `.select2-selection__rendered .select2-selection__choice` |
| `option_selector` | `.select2-results__option[aria-selected]` |
| `widget_selector` | `.select2-selection` |

| Méthode | Rôle |
|---|---|
| `wait_script()` | Attend que `yl.registerFunction` soit disponible (100 essais, 15s max) |
| `clean_label(label)` | Supprime le caractère `×` (bouton de suppression Select2) du label |

---

## 4. Héritage des classes de test fonctionnel

Toutes les classes de tests fonctionnels suivent ce schéma d'héritage multiple :

```
Select2Story          → sélecteurs CSS Select2
AdminMixin            → URLs admin, fill_name()
OptionMixin           → create_option() (ou ContentTypeOptionMixin)
AutocompleteTestCase  → navigateur Selenium, assertions, get/click/enter_text
        ↑
AdminForeignKeyTestCase  (définie dans chaque app)
```

---

## 5. Applications de test (17 apps)

### 5.1 `select2_foreign_key` — ForeignKey simple

**Modèle** : `TModel` avec champ `test` (ForeignKey vers lui-même) et `for_inline` (ForeignKey vers lui-même)

**Formulaire** : `TForm` avec `ModelSelect2(url='select2_fk')`

**Admin** : `TestAdmin` avec inline `TestInline` (TabularInline)

**Tests fonctionnels** (`test_functional.py`) :

| Méthode | Ce qui est testé |
|---|---|
| `test_can_select_option` | Sélectionner une option et vérifier qu'elle persiste après soumission |
| `test_can_select_option_in_first_inline` | Même chose dans le premier inline (ligne 0) |
| `test_can_select_option_in_first_extra_inline` | Même chose dans une ligne d'inline ajoutée dynamiquement (ligne 3) |
| `test_can_change_selected_option` | Sélectionner, renommer via popup, vérifier la mise à jour |
| `test_can_add_another_option` | Créer une option via popup "add another" |
| `test_can_unselect_option` | Sélectionner puis effacer la sélection |

---

### 5.2 `select2_many_to_many` — ManyToMany

**Modèle** : `TModel` avec champ `test` (ManyToManyField vers lui-même)

**Formulaire** : `TForm` avec `ModelSelect2Multiple`

**Tests fonctionnels** :

| Méthode | Ce qui est testé |
|---|---|
| `test_can_create_option_on_the_fly_and_select_existing_option` | Créer une nouvelle option ET sélectionner une option existante, vérifier les deux présentes |

---

### 5.3 `select2_one_to_one` — OneToOne

**Modèle** : `TModel` avec `name` soumis à `validate_slug`, champ `test` (OneToOneField)

**Tests fonctionnels** :

| Méthode | Ce qui est testé |
|---|---|
| `test_can_create_option_on_the_fly` | Créer une option (slug valide), vérifier persistance |
| `test_create_option_validation` | Saisir un nom invalide (slug), vérifier l'erreur de validation, corriger et valider |

---

### 5.4 `select2_generic_foreign_key` — GenericForeignKey

**Modèles** : `TModel` (avec deux GFK : `test` et `test2`) + `TProxyModel` (proxy de TModel)

**Formulaire** : `TForm(FutureModelForm)` avec `Select2GenericForeignKeyModelField`

**Tests unitaires** (`test_forms.py`) :

| Méthode | Ce qui est testé |
|---|---|
| `test_model_name` | Génération du nom de modèle pour proxy et modèle concret |
| `test_model_name_index_error` | Nom de modèle avec liste de parents vide |
| `test_save` | Sauvegarde d'un formulaire avec GFK |
| `test_validate` | Validation échoue si l'objet est retiré du queryset |
| `test_initial` | Rendu du widget avec valeur initiale |

**Tests fonctionnels** (`test_functional.py`) :

| Méthode | Ce qui est testé |
|---|---|
| `test_can_select_option` | Sélection d'une option GFK, valeur au format `ctype-pk-option_id` |
| `test_can_select_option_in_first_inline` | Version inline |
| `test_can_select_option_in_first_extra_inline` | Version inline dynamique |

---

### 5.5 `select2_generic_m2m` — Generic ManyToMany (django-generic-m2m)

**Modèle** : `TModel` avec `test` (`RelatedObjectsDescriptor` de genericm2m)

**Formulaire** : `TForm(FutureModelForm)` avec `GenericM2MQuerySetSequenceField` sur `QuerySetSequence(Group, TModel)`

**Tests unitaires** (`test_forms.py`) :

| Méthode | Ce qui est testé |
|---|---|
| `test_save` | Sauvegarde de deux objets de types différents (TModel + Group) |
| `test_validate` | Validation échoue si queryset restreint |
| `test_initial` | Rendu du widget avec valeurs initiales |

**Tests fonctionnels** : sélection de deux options de types différents, valeurs au format `ctype-pk`.

---

### 5.6 `select2_gm2m` — Generic ManyToMany (django-gm2m)

Identique à `select2_generic_m2m` mais utilise `GM2MField` de django-gm2m.

---

### 5.7 `linked_data` — Forwarding / dépendances entre champs

**Modèle** : `TModel` avec `owner` (FK vers User) et `test` (FK vers lui-même)

**Vue** : `LinkedDataView` filtre `TModel` selon `self.forwarded['owner']`

**Formulaire** : widget `test` avec `forward=('owner',)` + `clean_test()` qui valide la cohérence owner/test

**Tests unitaires** (`test_forms.py`) :

| Méthode | Ce qui est testé |
|---|---|
| `test_save` | Formulaire valide : fixture et form ont le même owner |
| `test_validate` | Formulaire invalide : owner du champ ≠ owner de l'objet sélectionné |

**Tests unitaires** (`test_views.py`) :

| Méthode | Ce qui est testé |
|---|---|
| `test_no_data` | GET sans paramètre `forward` |
| `test_not_dict` | `forward='[]'` (liste au lieu d'objet) → 400 |
| `test_invalid_json` | JSON malformé → 400 |
| `test_invalid_method` | PUT → 405 |

**Tests fonctionnels** :

| Méthode | Ce qui est testé |
|---|---|
| `test_filter_options` | Changer l'owner filtre les options du champ test |
| `test_filter_option_in_first_inline` | Même chose en inline |
| `test_can_select_option_in_first_extra_inline` | Version inline dynamique |

---

### 5.8 `secure_data` — Filtrage par propriétaire

Similaire à `linked_data` mais centré sur la sécurité : les utilisateurs ne voient que leurs propres objets.

**Tests fonctionnels** :

| Méthode | Ce qui est testé |
|---|---|
| `test_filtered_options` | Les options retournées appartiennent uniquement à l'utilisateur connecté |

---

### 5.9 `select2_list` — Listes statiques (sans QuerySet)

**Modèle** : `TModel` avec `test` (CharField, nullable)

**Tests unitaires** (`test_fields.py`) :

| Classe / Méthode | Ce qui est testé |
|---|---|
| `Select2ListChoiceFieldTest` | Initialisation avec liste, tuple, callable |
| `Select2ListCreateChoiceFieldTest` | Validation : autorise les valeurs non présentes dans la liste |

**Tests unitaires** (`test_views.py`) :

| Classe / Méthode | Ce qui est testé |
|---|---|
| `Select2ListViewTest` | Vue vide, POST échoue, résultats case-insensitive |
| `Select2ProvidedValueListViewTest` | Paires valeur/texte distinctes |
| `Select2GroupListViewTest` | Résultats groupés |

**Tests fonctionnels** : sélection, changement, création d'options pour un champ liste.

---

### 5.10 `select2_taggit` — Tags (django-taggit)

**Modèle** : `TModel` avec `test` (`TaggableManager`)

**Tests unitaires** (`test_forms.py`) :

| Méthode | Ce qui est testé |
|---|---|
| `test_save` | Sauvegarde d'un tag existant + nouveau tag |
| `test_multi_words_tag` | Tag avec plusieurs mots |
| `test_initial` | Rendu du widget avec tags initiaux |

**Tests fonctionnels** :

| Méthode | Ce qui est testé |
|---|---|
| `test_can_select_options` | Sélectionner plusieurs tags dont un nouveau |
| `test_can_select_option_in_first_inline` | Version inline |

---

### 5.11 `select2_tagging` — Tags (django-tagging)

Identique à `select2_taggit` mais utilise `TagField` de django-tagging. Limité à Django < 2.0.

---

### 5.12 `custom_select2` — Widget/vue custom

App de démonstration d'une implémentation personnalisée. Réutilise l'infrastructure de `select2_foreign_key`. Pas de tests métier propres.

---

### 5.13 `rename_forward` — Renommage de champ forwardé

**Modèle** : `TModel` avec `owner` (FK vers User) et relation nommée (`related_name='related_test_models_rf'`)

**Tests fonctionnels** : hérite directement de `AdminLinkedDataTest` de `linked_data`, teste le même comportement avec un `related_name` explicite.

---

### 5.14 `select2_nestedadmin` — Inline imbriqué (django-nested-admin)

**Modèles** :
- `TModelOne` : niveau 1 (`level_one`)
- `TModelTwo` : niveau 2 (`level_two`, FK vers TModelOne)
- `TModelThree` : niveau 3 (`test`, FK vers lui-même, FK vers TModelTwo)

**Tests fonctionnels** :

| Méthode | Ce qui est testé |
|---|---|
| `test_linked_value_is_forwarded_for_nested_admin` | Intercept XHR pour vérifier que les paramètres `forward` transmis contiennent bien `level_one` et `level_two` |

---

### 5.15 `select2_djhacker_formfield` — Intégration djhacker

Réutilise intégralement les tests de `select2_foreign_key` via héritage direct de sa classe de test.

---

### 5.16 `select2_outside_admin` — Utilisation hors admin

Pas de tests automatisés. Contient une `UpdateView` Django générique avec formset, servant de démo pour l'utilisation en dehors de l'interface admin.

---

### 5.17 `tests` — Tests unitaires du noyau

App centralisée pour les tests unitaires des composants de base.

**`test_widgets.py`** :

| Classe | Méthode | Ce qui est testé |
|---|---|---|
| `SelectTest` | `test_widget_renders_only_selected_with_url` | Seul le choix sélectionné est rendu si une URL est fournie |
| `Select2Test` | `test_widget_renders_empty_option_with_placeholder_without_url` | Option vide rendue si placeholder défini |
| `Select2Test` | `test_widget_no_empty_option_without_placeholder_without_url` | Pas d'option vide sans placeholder |
| `Select2Test` | `test_widget_finds_correct_language` | Langue correctement détectée (i18n) |
| `Select2Test` | `test_widget_does_not_find_incorrect_language` | Code langue invalide ignoré |
| `WidgetMixinTest` | `test_widget_renders_without_attrs` | Config forward sérialisée correctement en JSON avec/sans `id` |

---

## 6. Synthèse de la couverture

| Cas d'usage | App de test | Type de tests |
|---|---|---|
| ForeignKey | `select2_foreign_key` | Unitaire + Fonctionnel |
| ManyToMany | `select2_many_to_many` | Fonctionnel |
| OneToOne | `select2_one_to_one` | Fonctionnel |
| GenericForeignKey | `select2_generic_foreign_key` | Unitaire + Fonctionnel |
| Generic M2M (genericm2m) | `select2_generic_m2m` | Unitaire + Fonctionnel |
| Generic M2M (gm2m) | `select2_gm2m` | Unitaire + Fonctionnel |
| Forwarding / filtrage conditionnel | `linked_data`, `rename_forward` | Unitaire + Fonctionnel |
| Sécurité / filtrage par owner | `secure_data` | Fonctionnel |
| Listes statiques | `select2_list` | Unitaire + Fonctionnel |
| Tags (taggit) | `select2_taggit` | Unitaire + Fonctionnel |
| Tags (tagging) | `select2_tagging` | Unitaire + Fonctionnel |
| Inline imbriqué | `select2_nestedadmin` | Fonctionnel |
| Widget custom | `custom_select2` | Fonctionnel |
| Hors admin Django | `select2_outside_admin` | — (démo) |
| Widgets / sélecteurs / i18n | `tests` | Unitaire |
| Robustesse des vues (JSON invalide, méthodes) | `linked_data/test_views.py` | Unitaire |
