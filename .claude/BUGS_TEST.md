# Analyse des échecs de tests — py311-dj52

**Résultat** : 11 failed / 45 passed / 28 warnings

---

## Problème 1 — `ElementClickInterceptedException` (11 tests, bloquant)

### Tests concernés

Tous les tests `test_can_select_option_in_first_inline` et `test_can_select_option_in_first_extra_inline` dans :
- `select2_foreign_key`, `select2_generic_foreign_key`, `select2_list`
- `select2_taggit`, `select2_djhacker_formfield`, `rename_forward`

### Message d'erreur

```
ElementClickInterceptedException: Element <span class="select2-selection"> is not
clickable at point (505,620) because another element
<a class="TemplatesPanel" href="#"> obscures it
```

Les overlapping elements sont des onglets de la **Django Debug Toolbar** : `TemplatesPanel`, `SQLPanel`, `StaticFilesPanel`.

### Cause racine

La chaîne est la suivante :

1. `tox.ini` définit `setenv = DEBUG=1`
2. `settings/base.py` lit `DEBUG = os.environ.get('DEBUG', False)` → `DEBUG = True`
3. Le bloc conditionnel dans settings active debug_toolbar :
   ```python
   if DEBUG:
       import debug_toolbar
       INSTALLED_APPS.append('debug_toolbar')
       MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
   ```
4. La toolbar injecte ses onglets dans chaque page admin avec une position CSS fixe sur le côté droit de l'écran
5. Les formulaires inline ajoutent des lignes qui descendent dans la page et se retrouvent **sous les onglets de la toolbar**
6. Selenium essaie de cliquer sur le widget Select2 dans l'inline, mais la toolbar est par-dessus → exception

Les tests qui passent (`test_can_select_option`, inline numéro 0 sur des pages courtes) ne sont pas affectés car le widget est plus haut dans la page, hors de la zone couverte par la toolbar.

### Fix

Supprimer `django-debug-toolbar` de `test_project/requirements.txt`. Il n'a aucune utilité dans un contexte de tests automatisés headless.

```diff
- django-debug-toolbar
```

Et nettoyer le bloc conditionnel dans `settings/base.py` qui ne sert plus à rien :

```diff
- if DEBUG:
-     try:
-         import debug_toolbar
-     except ImportError:
-         pass
-     else:
-         INSTALLED_APPS.append('debug_toolbar')
-         MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
```

---

## Problème 2 — `UnorderedObjectListWarning` (non-bloquant, mais à corriger)

### Message

```
UnorderedObjectListWarning: Pagination may yield inconsistent results with an
unordered object_list: <class 'select2_foreign_key.models.TModel'> QuerySet.
```

Apparu sur quasiment tous les tests fonctionnels.

### Cause racine

Django 4.1+ émet cet avertissement quand un `ListView` (dont hérite `BaseQuerySetView`) pagine un QuerySet sans `ORDER BY`. Les résultats peuvent changer d'ordre entre deux pages, ce qui peut produire des doublons ou des omissions.

Les `TModel` de toutes les apps n'ont pas de `ordering` dans leur `Meta`, et les vues ne forcent pas d'ordre non plus.

### Fix

Deux options :

**Option A** (recommandée) — ajouter `ordering` sur chaque `TModel` dans les apps de test :
```python
class TModel(models.Model):
    name = models.CharField(max_length=200)
    class Meta:
        ordering = ['name']
```

**Option B** — surcharger `get_queryset()` dans `BaseQuerySetView` pour ajouter un `.order_by('pk')` par défaut quand aucun ordering n'est défini. C'est un fix dans le code source de la lib, plus robuste.

---

## Problème 3 — `DatabaseWrapper` thread sharing (warning, non-bloquant)

### Message

```
DatabaseError: DatabaseWrapper objects created in a thread can only be used in
that same thread. The object with alias 'default' was created in thread id X
and this is thread id Y.
```

Apparu uniquement sur `test_can_unselect_option` de `select2_djhacker_formfield`.

### Cause racine

`StaticLiveServerTestCase` démarre un vrai serveur HTTP dans un thread séparé. Django 4.1+ avec SQLite enforces strictement le thread-local des connexions DB. Lors du teardown du test, le serveur live ferme des connexions depuis le mauvais thread.

C'est un problème connu de `pytest-splinter` / `StaticLiveServerTestCase` avec SQLite. Il n'entraîne pas d'échec de test — c'est un warning émis pendant le teardown.

### Fix

Filtrer l'avertissement dans `pytest.ini` pour éviter le bruit :

```ini
filterwarnings =
    ignore::pytest.PytestUnhandledThreadExceptionWarning
```

Ou, solution plus propre, passer à `--reuse-db` (déjà actif) et s'assurer que `CONN_MAX_AGE = 0` est bien la valeur par défaut (ce qui est le cas).

---

## Récapitulatif

| # | Type | Impact | Fix |
|---|---|---|---|
| 1 | `ElementClickInterceptedException` (debug toolbar) | **11 tests échouent** | Supprimer `django-debug-toolbar` de requirements.txt et settings |
| 2 | `UnorderedObjectListWarning` | Warning, pas d'échec | Ajouter `ordering` aux modèles de test ou à `BaseQuerySetView` |
| 3 | `DatabaseWrapper` thread sharing | Warning, pas d'échec | Filtrer dans `pytest.ini` ou ignorer |

Le problème 1 est la priorité absolue. Les problèmes 2 et 3 sont du bruit.
