# Changelog modernisation — branche `modernize`

Mise à niveau complète du projet pour Python 3.11–3.14 et Django 5.2–6.0+.
**105 fichiers modifiés, 196 insertions, 477 suppressions.**

---

## Commits antérieurs à la modernisation

| Hash | Message |
|---|---|
| `d829891` | Release 3.12.1 |

---

## Commit 1 — Documentation interne (`9721d99`)

Création des fichiers de référence dans `.claude/` :

- `ANALYSE.md` — architecture technique complète (flux requête, classes clés, JS)
- `TESTS.md` — structure et documentation des 17 apps de test
- `OVERVIEW.md` — référence architecture étendue
- `PLAN_MODERNISATION.md` — plan en 8 étapes
- `PLAN_TESTS.md` — plan de nettoyage de la suite de tests
- `CLAUDE.md` (racine) — résumé ~20 lignes chargé automatiquement par Claude Code

---

## Commit 2 — Matrice tox + dépendances (`d152ef0`, `c85a50e`)

### `tox.ini`
- Nouvelle matrice : `py{311,312,313,314}-dj52` · `py{312,313,314}-dj60` · `py{312,313,314}-djmain`
- Suppression des envs obsolètes : `dj32`, `dj40`, `dj41`, `dj42`, `dj50`, `dj51` et Python 3.6–3.10
- `dj60` restreint à `py312+` (Django 6.0 requiert Python ≥ 3.12)
- `djmain` restreint à `py312+` (Django main requiert Python ≥ 3.12)

### `test_project/requirements.txt`
- Suppression de `django-generic-m2m` (mort, plus sur PyPI)
- Suppression de `django-gm2m` (mort, plus sur PyPI)
- Suppression de `django-tagging` (incompatible Django 5.2+)
- Suppression de `mock` (stdlib `unittest.mock` depuis Python 3.3)
- Suppression de `django-debug-toolbar` (interfère avec Selenium en mode headless)

---

## Commit 3 — Nettoyage codebase (`608d500`)

### Code source (`src/`)

| Fichier | Changement |
|---|---|
| `dal/views.py` | Suppression guards `VERSION < (2,)` et `VERSION < (4,)` ; import direct de `lookup_spawns_duplicates` ; simplification de `has_add_permission()` |
| `dal_select2/__init__.py` | Suppression de `default_app_config` (obsolète depuis Django 3.2) |
| `dal/test/case.py` | Suppression guard `VERSION < (1, 10)` ; import mort `urlresolvers` → `django.urls` ; `super(Class, self)` → `super()` |
| `dal/test/stories.py` | Suppression `from __future__ import unicode_literals` ; 2 `bare except` → `except Exception` ; `super()` modernisé |
| `dal_select2/test.py` | `bare except` → `except Exception` |
| `dal_genericm2m/` | **Supprimé** (2 fichiers) |
| `dal_gm2m/` | **Supprimé** (2 fichiers) |
| `dal_select2_tagging/` | **Supprimé** (2 fichiers) |

### Projet de test (`test_project/`)

| Fichier | Changement |
|---|---|
| `settings/base.py` | Suppression blocs `OPENSHIFT_*`, `MIDDLEWARE_CLASSES`, `SessionAuthenticationMiddleware`, guards `VERSION`, `USE_L10N`, bloc `debug_toolbar` |
| `linked_data/test_views.py` | `force_text` → `force_str` ; import `urlresolvers` → `django.urls` |
| `select2_generic_foreign_key/test_forms.py` | Suppression bloc `try/except ImportError` pour `reverse` |
| `select2_tagging/` | **Supprimé** (7 fichiers) — dépendait de `django-tagging` |
| `select2_gm2m/` | **Supprimé** (9 fichiers) — dépendait de `django-gm2m` |
| `select2_generic_m2m/` | **Supprimé** (9 fichiers) — dépendait de `django-generic-m2m` |

---

## Changements en attente de commit — Sessions 1 & 2

### Fix infrastructure de test

**Problème : `ElementClickInterceptedException` (debug toolbar)**
- Cause : la Django Debug Toolbar injectait des onglets CSS fixes qui couvraient les widgets Select2 dans les inlines
- Fix : suppression de `django-debug-toolbar` de `requirements.txt` et du bloc conditionnel dans `settings/base.py`

**Problème : `UnorderedObjectListWarning` (13 apps)**
- Cause : Django 4.1+ avertit quand un `ListView` pagine un QuerySet sans `ORDER BY`
- Fix : ajout de `class Meta: ordering = ['name']` sur tous les modèles de test (13 apps, 15 modèles)
- Fix complémentaire : `Tag.objects.all()` → `Tag.objects.order_by('name')` dans `select2_taggit/urls.py`

**Problème : `ElementClickInterceptedException` résiduel (`rename_forward`)**
- Cause : l'inline n°3 du formulaire `rename_forward` (champ `owner` supplémentaire) dépassait du viewport
- Fix : `src/dal/test/case.py` — ajout de `scrollIntoView({block: "center"})` avant chaque `click()`

**Problème : `DatabaseWrapper` thread sharing (warning pytest)**
- Cause : `StaticLiveServerTestCase` + SQLite + Django 4.1+ enforce strictement les connexions thread-local
- Fix : `pytest.ini` — `ignore::pytest.PytestUnhandledThreadExceptionWarning`

**Problème : `DeprecationWarning` pytest-splinter**
- Cause : `pytest_splinter/plugin.py` appelle `set_timeout()` déprécié dans `RemoteConnection`
- Fix : `pytest.ini` — filtre ciblé sur le module `pytest_splinter`

### Packaging — migration `pyproject.toml`

`setup.py` **supprimé**, remplacé par `pyproject.toml` (PEP 517/518) :

```
[build-system]   setuptools.build_meta
[project]        métadonnées complètes
[project.optional-dependencies]  nested / tags / gfk
[tool.setuptools.packages.find]  where = ["src"]
[tool.ruff.*]    configuration linter
```

Mises à jour des métadonnées :
- `python_requires = ">=3.11"`
- `install_requires` : `django>=3.2` → `django>=5.2`
- Extra `genericm2m` supprimé (`django-generic-m2m` est mort)
- Classifiers Django : 3.2/4.x/5.0–5.1 → **5.2 / 6.0**
- Classifiers Python : ajout **3.11 / 3.12 / 3.13 / 3.14**

### Linter — migration `flake8` → `ruff`

`tox.ini [testenv:checkqa]` :
- Avant : 4 invocations `flake8` + 7 dépendances (`flake8`, `flake8-debugger`, `flake8-docstrings`, `flake8-import-order`, `mccabe`, `pep8-naming`, `pydocstyle<4`)
- Après : `ruff check src test_project` + 1 dépendance (`ruff`)

Configuration dans `pyproject.toml [tool.ruff.lint]` :
- Règles activées : `E`, `W`, `F`, `C90`, `I`, `N`, `T10`
- Complexité cyclomatique max : 8
- `per-file-ignores` ciblés : migrations (`E501`), `settings/__init__.py` (`F403`), `djhacker/urls.py` (`E402`), `autocomplete.py` (`F401`, `I001`)

Corrections de code déclenchées par ruff :
- `src/dal_select2/views.py` : variable ambiguë `l` → `items` (règle E741, 2 occurrences)
- `src/dal/views.py` : ligne trop longue extraite en variable (règle E501)
- 88 fichiers : imports réordonnés via `ruff check --fix` (règle I001)

### Documentation

- **Supprimés** : `docs/genericm2m.rst`, `docs/gm2m.rst`, `docs/tagging.rst`
- `docs/index.rst` : toctree "External app support" → `gfk` + `taggit` uniquement
- `docs/install.rst` : section "Django versions earlier than 2.0" supprimée
- `docs/conf.py` : version 3.11 → 3.12.1 ; intersphinx Python 2.7 → 3

---

## Résultat final

| Environnement | Résultat |
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
| `checkqa` (ruff) | ✅ 0 erreur |

**Avant modernisation** : installation impossible (`django-generic-m2m` mort sur PyPI)
