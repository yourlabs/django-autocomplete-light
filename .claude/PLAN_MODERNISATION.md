# Plan de modernisation — django-autocomplete-light

**Matrice cible :** Python 3.11 / 3.12 / 3.13 / 3.14 × Django 5.2 / 6.0 / 6.1
**Version actuelle :** 3.12.1

---

## Étape 1 — Nettoyer les gardes de version dans le code source

Deux fichiers contiennent des branches conditionnelles liées à d'anciennes versions, qui deviennent du code mort.

**`src/dal/views.py`**
- Ligne 9–13 : garde `django.VERSION >= (4, 0)` pour `lookup_spawns_duplicates`.
  → Garder uniquement l'import Django ≥ 4.0, supprimer la branche `else`.
- Ligne 171–174 : garde `django.VERSION < (2, 0, 0)` pour `is_authenticated`.
  → Supprimer la branche Django < 2 ; `request.user.is_authenticated` est une propriété depuis Django 1.10.

**`src/dal_select2/__init__.py`**
- Ligne 4–5 : `default_app_config` n'est plus nécessaire depuis Django 3.2.
  → Supprimer entièrement le bloc conditionnel (fichier peut devenir vide).

---

## Étape 2 — Mettre à jour `setup.py`

- `install_requires` : passer `django>=5.2`
- `python_requires` : ajouter `python_requires='>=3.11'`
- `classifiers` : remplacer les entrées Django/Python par :
  ```
  Framework :: Django :: 5.2
  Framework :: Django :: 6.0
  Framework :: Django :: 6.1
  Programming Language :: Python :: 3.11
  Programming Language :: Python :: 3.12
  Programming Language :: Python :: 3.13
  Programming Language :: Python :: 3.14
  ```

---

## Étape 3 — Mettre à jour `tox.ini`

- Supprimer les envs : `dj32`, `dj40`, `dj41`, `dj42`, `dj50`, `dj51`
- Supprimer les versions Python : `py36`, `py37`, `py38`, `py39`, `py310`
- Nouvelle `envlist` :
  ```ini
  py{311,312,313,314}-dj52
  py{311,312,313,314}-dj60
  py{311,312,313,314}-dj61
  py{311,312,313,314}-djmain
  ```
- Mettre à jour les `deps` en conséquence.

---

## Étape 4 — Mettre à jour `test_project/requirements.txt`

- Supprimer `mock` (intégré à `unittest` depuis Python 3.3)
- Supprimer `django-tagging` (incompatible Django moderne, app `select2_tagging` déjà conditionnelle)
- Supprimer `django-gm2m` (idem, app `select2_gm2m` déjà conditionnelle)
- Supprimer `django-generic-m2m` (idem, app `select2_generic_m2m` déjà conditionnelle)
- Épingler les dépendances restantes à des versions compatibles Django 5.2+
- Vérifier la compatibilité de `djhacker`, `django-nested-admin`, `django-querysetsequence`

---

## Étape 5 — Supprimer les apps de test obsolètes

Ces apps de test_project sont conditionnées à `Django < 2.0` et n'ont plus lieu d'être :
- `select2_tagging/` — utilise django-tagging (incompatible)
- `select2_gm2m/` — utilise django-gm2m (incompatible)
- `select2_generic_m2m/` — utilise django-generic-m2m (incompatible)

Actions :
- Supprimer les dossiers
- Retirer les entrées de `test_project/settings/base.py` (`INSTALLED_APPS`)
- Retirer les includes dans `test_project/urls.py`
- Supprimer les sous-packages source correspondants : `dal_genericm2m/`, `dal_gm2m/`, `dal_select2_tagging/`

---

## Étape 6 — Mettre à jour la documentation

- `docs/conf.py` : mettre à jour les versions Python/Django documentées
- Supprimer les pages devenues obsolètes : `genericm2m.rst`, `gm2m.rst`, `tagging.rst`
- Mettre à jour `install.rst` avec les nouvelles exigences minimales

---

## Étape 7 — Remplacer `setup.py` par `pyproject.toml` (optionnel mais recommandé)

`setup.py` est le format legacy. Migration vers `pyproject.toml` avec `[build-system]` (setuptools) et `[project]`. C'est le standard actuel et requis par certains outils modernes.

---

## Étape 8 — Mettre à jour le linter (`checkqa`)

- Remplacer `flake8` + plugins par `ruff` (plus rapide, une seule dépendance, activement maintenu)
- Supprimer : `flake8`, `flake8-debugger`, `flake8-docstrings`, `flake8-import-order`, `mccabe`, `pep8-naming`, `pydocstyle<4`

---

## Ordre d'exécution suggéré

```
1. Code source (étapes 1)         ← sans risque, corrections pures
2. setup.py (étape 2)             ← métadonnées
3. tox.ini (étape 3)              ← matrice de test
4. requirements.txt (étape 4)     ← dépendances de test
5. Suppression apps/packages (5)  ← nettoyage
6. Docs (étape 6)                 ← mise à jour
7. pyproject.toml (étape 7)       ← optionnel, peut être fait séparément
8. Linter (étape 8)               ← optionnel, peut être fait séparément
```
