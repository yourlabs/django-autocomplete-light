# TODO — suite de la modernisation

## Priorité 1 — Compléter la matrice tox

`py311-dj52` passe. Il reste à valider les 10 autres envs :

```
py312-dj52, py313-dj52, py314-dj52
py312-dj60, py313-dj60, py314-dj60
py311-djmain, py312-djmain, py313-djmain, py314-djmain
```

Lancer `tox` complet et traiter les échecs éventuels (Django 6.0 et main peuvent avoir des API différentes).

---

## Priorité 2 — Warning résiduel `UnorderedObjectListWarning` (taggit)

La sortie montre encore :
```
UnorderedObjectListWarning: Pagination may yield inconsistent results with an
unordered object_list: <class 'taggit.models.Tag'> QuerySet.
```

Ce warning vient du modèle `Tag` de la lib `django-taggit` — on ne contrôle pas ce modèle. Options :

- **Option A** : surcharger `get_queryset()` dans la vue `select2_taggit` pour ajouter `.order_by('name')`
- **Option B** : filtrer ce warning spécifiquement dans `pytest.ini` :
  ```ini
  filterwarnings =
      ignore::pytest.PytestUnhandledThreadExceptionWarning
      ignore::django.core.paginator.UnorderedObjectListWarning
  ```

---

## Priorité 3 — Warning `DeprecationWarning` pytest-splinter

```
DeprecationWarning: set_timeout() in RemoteConnection is deprecated,
set timeout in client_config instead
```

Vient de `pytest-splinter` lui-même (`plugin.py:599`). Ce n'est pas notre code.
Options :
- Ouvrir un ticket / PR upstream sur pytest-splinter
- Filtrer dans `pytest.ini` en attendant un fix upstream

---

## Priorité 4 — `setup.py` / `pyproject.toml`

Mettre à jour les métadonnées du package :
- `python_requires = ">=3.11"` dans `setup.py`
- Classifiers : supprimer Python 3.6–3.10 et Django 3.2–5.1
- `install_requires` : vérifier que les contraintes de version sont à jour
- Envisager migration vers `pyproject.toml` (PEP 517/518)

---

## Priorité 5 — Commit des changements en cours

Tous les fixes de la session sont non commités. Un commit propre à faire :

```
Fix test suite for Python 3.11+ / Django 5.2+

- Remove django-debug-toolbar (breaks Selenium inline tests)
- Add Meta.ordering to all test models (UnorderedObjectListWarning)
- Add scrollIntoView in click() helper (viewport clipping in Firefox)
- Filter PytestUnhandledThreadExceptionWarning in pytest.ini
```

---

## Priorité 6 — Documentation utilisateur

- Mettre à jour `CHANGELOG` et `README` pour mentionner le drop des vieilles versions
- Mettre à jour la doc readthedocs si elle référence des versions Python/Django obsolètes
