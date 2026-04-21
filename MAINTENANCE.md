# Plan de maintenance — django-autocomplete-light

> Rédigé le 2026-04-20 — mis à jour après inspection du code source réel.
> Référence fork : [PurpleToti/django-autocomplete-light](https://github.com/PurpleToti/django-autocomplete-light) — 24 commits en avance sur yourlabs/master, 0 en retard.

---

## État actuel

### Ce qui a déjà été fait (fork PurpleToti, PR #1407)

| Tâche | Statut |
|---|---|
| Drop Python < 3.11 / Django < 5.2 | ✅ Fait |
| Suppression packages morts (`dal_genericm2m`, `dal_gm2m`, `dal_select2_tagging`, `dal_legacy_static`) | ✅ Fait |
| Migration `setup.py` → `pyproject.toml` (PEP 517/518) | ✅ Fait |
| Migration linter `flake8` → `ruff` | ✅ Fait |
| CI GitHub Actions (checkqa + docs + matrice tests Firefox headless) | ✅ Fait |
| Docs mises à jour Django 5.2+ / Sphinx 9.x | ✅ Fait |
| `Select2InitialRenderMixin` — fix valeurs initiales absentes (#1076/#1292) | ✅ Fait (`src/dal_select2/widgets.py` lignes 112–140) |
| Build system : `python -m build` + publication sdist + wheel (#1383) | ✅ Fait |
| Matrice CI : `py{311,312,313,314}-dj52` + `py{312,313,314}-dj{60,main}` | ✅ Fait |

---

## Phase 1 — Merge et nettoyage des PRs (priorité immédiate)

### 1.1 Merger PR #1407 dans yourlabs/master

La PR est prête : CI verte, tests OK, changelog complet.

**Action :** Merger `PurpleToti:master` → `yourlabs:master` via PR #1407.

### 1.2 Corriger la version dans `pyproject.toml` avant release

**Fichier :** `pyproject.toml` ligne 7

```toml
# Actuellement :
version = "3.12.1"
# À changer en (breaking change : drop Python < 3.11 / Django < 5.2) :
version = "4.0.0"
```

Note : `package.json` est aussi désynchronisé (ligne 3 dit `"version": "3.5.1"`) mais ce fichier est uniquement utilisé pour le build JS (npm), pas pour PyPI.

### 1.3 Fermer les PRs Snyk obsolètes (~26 PRs)

Toutes ces PRs ciblent Django 3.2.x / anciens deps, désormais hors scope.

PRs à fermer comme obsolètes :
`#1405, #1403, #1402, #1401, #1399, #1397, #1391, #1390, #1389, #1387, #1384, #1379, #1377, #1376, #1375, #1374, #1372, #1371, #1369, #1367, #1366, #1365, #1364, #1363, #1362, #1361`

**Message de fermeture suggéré :**
> Closing as obsolete: this PR targets Django 3.2.x / old dependencies. The project now requires Django ≥ 5.2 (see PR #1407). Thank you for the contribution.

### 1.4 Fermer PR #1385 (`super(..)` → `super()`)

Déjà couvert par le ruff pass de #1407.

---

## Phase 2 — Release (après merge de #1407)

### 2.1 Checklist release

- [ ] Bumper `pyproject.toml` → `version = "4.0.0"` (breaking change confirmé)
- [ ] Mettre à jour `CHANGELOG.md` avec les notes de la v4.0.0
- [ ] `python -m build` → vérifie que sdist + wheel sont générés
- [ ] `twine upload dist/*` → PyPI
- [ ] Créer le tag git `v4.0.0` + release GitHub

---

## Phase 3 — Triage des issues ouvertes (50 issues)

### 3.1 Issues actives prioritaires (par nb de commentaires / impact)

| # | Comments | Date | Titre | Action recommandée |
|---|---|---|---|---|
| **#1311** | 10 | 2022-09 | JS non initialisé avec HTMX | **Haute priorité** — voir Phase 4 |
| **#1318** | 18 | 2023-01 | Select simple pas beau avec django-bootstrap5 | Moyenne — CSS override, documenter le workaround |
| **#1283** | 16 | 2022-02 | Focus sur input ne fonctionne pas au clic | Moyenne — regression UX fréquente |
| **#1398** | — | 2025-10 | Bug `allowClear` avec select2 | **Haute** — confirmé dans le code, voir Phase 4 |
| **#1396** | — | 2025-08 | `AttributeError` à l'installation | **Haute** — à reproduire, voir Phase 4 |
| **#1400** | — | 2025-11 | Incompatibilité `django-formset` (Forwarding cassé) | Haute — régression de compatibilité |
| **#1334** | — | 2023-08 | `WidgetMixin.__init__` crash si `attrs=None` | **Moyenne** — confirmé dans le code, voir Phase 4 |
| **#1333** | — | 2023-07 | Widget protocol Django non implémenté | **Moyenne** — confirmé dans le code, voir Phase 4 |
| **#1352** | 8 | 2024-01 | Clonage formulaire autocomplete dynamiquement | Faible — cas d'usage avancé, documenter |
| **#1357** | 2 | 2024-03 | `ModelSelect2Multiple` réordonne les items | **Haute** — confirmé dans le code, voir Phase 4 |

### 3.2 Issues à fermer comme obsolètes / hors scope

| # | Titre | Raison |
|---|---|---|
| #1267 | DAL 3.9.0 will break your project? | Vieux, Django 3.x |
| #1285 | Release date v4.0.0rc0? | v4 est prête |
| #1296 | Migrer CI vers GitHub Actions | Fait dans #1407 |
| #100 | Django 1.7 compatibility | Très obsolète |
| #97 | Deprecated `is_authenticated()` Django 2.0 | Obsolète, Python 3.11+ only |

### 3.3 Issues à documenter (pas de code à changer)

| # | Titre | Action |
|---|---|---|
| #1319 | Charger JS/CSS dans une BSModal | Documenter la bonne façon dans les docs |
| #1345 | Forward fields outside Admin | Ajouter exemple dans docs |
| #1346 | Forward ForeignKey("self") | Ajouter exemple dans docs |
| #1406 | Template tag pour inclure les médias globalement | Documenter dans `install.rst` |

---

## Phase 4 — Bugs à corriger (code)

### Priorité haute

---

#### #1311 — JS non initialisé avec HTMX

**Analyse :** Le JS principal (`autocomplete_light.js`) est wrappé dans `window.addEventListener("load", ...)` (ligne 30). Un `MutationObserver` (lignes 199–216) est enregistré à l'intérieur de ce callback, il surveille les insertions DOM. En théorie, les swaps HTMX devraient être captés par le MutationObserver. Le vrai problème est que `window.addEventListener("load", ...)` est différent de `DOMContentLoaded` : si le script se charge après le `load` event (cas fréquent avec HTMX qui injecte des `<script>` tags), l'init ne se déclenche pas.

**Fichier :** `src/dal/static/autocomplete_light/autocomplete_light.js` ligne 30

```js
// Actuellement :
window.addEventListener("load", function () {
    // ...tout le code d'init...
});

// Problème : avec HTMX, les fragments chargés dynamiquement contiennent
// souvent des <script> tags ré-exécutés APRÈS l'événement "load".
// Le MutationObserver (ligne 199) est bien là pour capter les nouveaux nœuds,
// mais il n'est enregistré qu'à l'intérieur du callback "load".
```

**Fix suggéré :** Écouter également `htmx:afterSettle` au niveau `document` pour re-scanner les nouveaux widgets :

```js
// À ajouter APRÈS la fermeture du window.addEventListener("load", ...) existant :
document.addEventListener('htmx:afterSettle', function(e) {
    if (window.__dal__initialize && window.django && django.jQuery) {
        django.jQuery('[data-autocomplete-light-function]', e.detail.elt)
            .excludeTemplateForms()
            .each(window.__dal__initialize);
    }
});
```

**Complexité réelle :** Faible (5 lignes JS). Régénérer aussi `autocomplete_light.min.js` avec `npm run minify-autocomplete`.

---

#### #1398 — Bug `allowClear` avec select2

**Analyse :** Select2 4.x exige un `placeholder` non vide quand `allowClear: true`. Dans le code actuel, `allowClear` est activé pour tous les champs non-required mais le placeholder par défaut est `''` (chaîne vide).

**Fichier :** `src/dal_select2/static/autocomplete_light/select2.js` lignes 96–99

```js
// Actuellement :
$element.select2({
    placeholder: $element.attr('data-placeholder') || '',
    allowClear: !$element.is('[required]'),
    // ...
});
```

**Fix suggéré :** N'activer `allowClear` que si un placeholder est effectivement défini, conformément au contrat de select2 :

```js
var placeholderText = $element.attr('data-placeholder') || '';
$element.select2({
    placeholder: placeholderText,
    allowClear: !$element.is('[required]') && placeholderText !== '',
    // ...
});
```

**Complexité réelle :** Triviale (1 ligne JS). Régénérer aussi `select2.min.js` avec `npm run minify-select2`.

---

#### #1357 — `ModelSelect2Multiple` réordonne les items

**Analyse :** `ModelSelect2Multiple` n'a pas de `value_from_datadict()` propre. Il hérite de `forms.SelectMultiple` via `QuerySetSelectMixin` → `WidgetMixin` → `forms.SelectMultiple`. La méthode `SelectMultiple.value_from_datadict()` de Django appelle `data.getlist(name)` qui retourne les valeurs dans l'ordre du POST, mais `filter_choices_to_render()` (`src/dal/widgets.py` lignes 63–66 et 151–158) filtre ensuite sur `self.choices.queryset` avec un `pk__in=[...]` — or un filtre `pk__in` dans Django ORM ne préserve pas l'ordre des PKs transmis, il suit l'ordre de la base.

**Fichier :** `src/dal/widgets.py` lignes 151–158 (`QuerySetSelectMixin.filter_choices_to_render`)

```python
# Actuellement :
def filter_choices_to_render(self, selected_choices):
    try:
        self.choices.queryset = self.choices.queryset.filter(
            pk__in=[c for c in selected_choices if c]
        )
    except ValueError:
        pass
```

**Fix suggéré :** Ajouter `value_from_datadict()` dans `ModelSelect2Multiple` (ou `QuerySetSelectMixin`) pour préserver l'ordre des PKs tel que soumis par select2 :

```python
# À ajouter dans src/dal_select2/widgets.py, classe ModelSelect2Multiple :
def value_from_datadict(self, data, files, name):
    """Return values preserving the order submitted by Select2."""
    return data.getlist(name)
    # Note: filter_choices_to_render est appelé à l'affichage (render),
    # pas lors de la soumission. Le vrai fix est dans le ModelField qui
    # reçoit la liste de PKs et doit les traiter dans l'ordre.
    # Alternativement, utiliser Case/When pour préserver l'ordre en DB :
    # from django.db.models import Case, When
    # preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)])
    # qs.filter(pk__in=pks).order_by(preserved)
```

**Complexité réelle :** Moyenne. Le bug est en deux parties : (1) le widget retourne bien les PKs dans l'ordre POST mais (2) `filter_choices_to_render` réordonne les choices selon le queryset DB. Il faut ajouter `Case/When` dans `filter_choices_to_render` pour les `ModelSelect2Multiple`.

---

### Priorité moyenne

---

#### #1334 — `WidgetMixin.__init__` crash si `attrs=None`

**Analyse :** Confirmé. Si l'appelant passe explicitement `attrs=None` (ce que Django fait dans certains cas internes), `kwargs.get("attrs", {})` retourne `None` (la valeur explicite), et `None.get("data-placeholder")` lève `AttributeError`.

**Fichier :** `src/dal/widgets.py` ligne 47

```python
# Actuellement (ligne 47) :
self.placeholder = kwargs.get("attrs", {}).get("data-placeholder")

# Fix :
self.placeholder = (kwargs.get("attrs") or {}).get("data-placeholder")
```

**Complexité réelle :** Triviale (1 caractère de diff).

---

#### #1333 — Widget protocol Django non implémenté

**Analyse :** `WidgetMixin` (classe de base pour tous les widgets DAL) n'implémente aucune des méthodes du protocole Widget Django introduites en Django 2.x et renforcées en Django 4.x+ :
- `use_required_attribute(initial_value)` — contrôle l'attribut HTML `required`
- `subwidgets(name, value, attrs)` — pour les widgets composés
- `id_for_label(id_)` — retourne l'`id` à utiliser dans le `<label>`

Ces méthodes existent sur `forms.Select` (classe parente réelle via MRO), donc elles ne crashent pas, mais `WidgetMixin` ne les surcharge pas pour tenir compte de son URL/forward config.

**Fichier :** `src/dal/widgets.py` — `class WidgetMixin` (lignes 13–137)

**Fix suggéré :** Vérifier le comportement de `use_required_attribute()` avec les widgets DAL non-required mais avec `allowClear`. Probablement ajouter :

```python
def use_required_attribute(self, initial_value):
    # Les widgets DAL avec allowClear ne doivent pas forcer required
    return super().use_required_attribute(initial_value)
```

**Complexité réelle :** Faible à moyenne — nécessite d'abord de comprendre l'impact réel sur les formulaires Django 5.2+.

---

#### #1396 — AttributeError à l'installation

**Analyse :** Impossible à reproduire depuis le code seul. Le code d'import de `src/dal/autocomplete.py` est propre (blocs `_installed()` bien gardés). Cependant, deux dead codes Python 2 identifiés pourraient être liés à des erreurs d'import sur des environnements propres :

**Fichier 1 :** `src/dal_select2/widgets.py` lignes 3–10 et 56–62

```python
# Dead code Python 2 — peut lever des warnings ou confusions à l'import :
try:
    from functools import lru_cache
except ImportError:  # py2
    try:
        from backports.functools_lru_cache import lru_cache
    except ImportError:
        lru_cache = None
# ...
if lru_cache:
    get_i18n_name = lru_cache()(get_i18n_name)
else:
    import warnings
    warnings.warn('Python2: no cache on ...')
```

**Fichier 2 :** `src/dal_select2/views.py` lignes 3–6

```python
# Dead code Python 2 — collections.Sequence supprimé en Python 3.10 :
try:
    from collections.abc import Sequence
except ImportError:  # py < 3.10
    from collections import Sequence
```

**Fix :** Puisque Python ≥ 3.11 est désormais requis, simplifier directement :

```python
# src/dal_select2/widgets.py — remplacer lignes 3–10 par :
from functools import lru_cache

# ...supprimer le bloc if lru_cache / else aux lignes 56–62, garder uniquement :
get_i18n_name = lru_cache()(get_i18n_name)

# src/dal_select2/views.py — remplacer lignes 3–6 par :
from collections.abc import Sequence
```

**Complexité réelle :** Triviale. Ces cleanups réduisent aussi la surface de `#1396`.

---

#### #1400 — Incompatibilité avec `django-formset`

**Analyse :** Non reproductible depuis le code seul. Le Forwarding DAL utilise l'événement `change` jQuery (via `yl.getForwards()` dans `autocomplete_light.js`). `django-formset` intercepte les événements de formulaire avec sa propre logique. Le conflit probable est dans la propagation des événements `change` sur les champs forwardés.

**Fichier concerné :** `src/dal/static/autocomplete_light/autocomplete_light.js` — fonctions `yl.getForwards` et `yl.getFieldRelativeTo` (lignes 419–480)

**Action :** Reproduire avec un projet minimal `django-formset` + DAL, puis diagnostiquer si le sélecteur `[name=prefix+field]` est compatible avec la structure DOM générée par `django-formset`.

**Complexité réelle :** Inconnue sans reproduction. Suspicion : moyenne.

---

### Nettoyage de code (non lié à des issues)

#### Dead code Python 2 dans `dal_select2`

Identifié lors de l'inspection, non tracké dans les issues :

| Fichier | Lignes | Problème |
|---|---|---|
| `src/dal_select2/widgets.py` | 3–10 | `try/except ImportError` pour `lru_cache` Python 2 |
| `src/dal_select2/widgets.py` | 56–62 | Branch `if lru_cache` + warning Python 2 |
| `src/dal_select2/views.py` | 3–6 | `try/except ImportError` pour `collections.Sequence` Python 2 |

Fix dans le cadre du nettoyage post-merge #1407.

#### `dal_contenttypes` non exposé dans `autocomplete.py`

**Fichier :** `src/dal/autocomplete.py`

Le docstring (lignes 11–12) mentionne l'import conditionnel de `dal_contenttypes`, mais le bloc correspondant est absent du code. Le package `src/dal_contenttypes/` existe bien mais n'est jamais importé via `autocomplete.py`.

```python
# Manquant dans src/dal/autocomplete.py :
if _installed('dal_select2') and _installed('django.contrib.contenttypes'):
    from dal_contenttypes.fields import (...)  # à vérifier selon l'API publique
```

**Complexité réelle :** Faible à moyenne — vérifier d'abord si `dal_contenttypes` expose une API publique à re-exporter.

---

## Phase 5 — Améliorations (features)

| # | Titre | Effort | Valeur |
|---|---|---|---|
| #1406 | Template tag pour médias globaux | Faible | Haute — demandé régulièrement |
| #1264 | Free text dans `Select2ListView` | Moyenne | Moyenne |
| #1323 | Autoriser sélection dupliquée | Faible | Moyenne |
| #1288 | Labels custom dans `Select2ListView` | Moyenne | Haute |
| #1313 | `class Formset(Forward)` | Moyenne | Moyenne |

---

## Résumé des actions par ordre de priorité

```
1. [ ] Merger PR #1407 dans yourlabs/master
2. [ ] Bumper version pyproject.toml → 4.0.0
3. [ ] Fermer les ~26 PRs Snyk obsolètes
4. [ ] Fermer PR #1385
5. [ ] Fix #1334 : src/dal/widgets.py:47 — (kwargs.get("attrs") or {}).get(...)
6. [ ] Fix #1398 : src/dal_select2/static/.../select2.js:99 — allowClear conditionnel
7. [ ] Fix dead code Python 2 : dal_select2/widgets.py:3-10,56-62 + views.py:3-6
8. [ ] Fix #1311 : autocomplete_light.js — ajouter listener htmx:afterSettle
9. [ ] Fix #1357 : ModelSelect2Multiple — préserver ordre PKs (Case/When)
10. [ ] Fix #1396 : reproduire AttributeError + nettoyer dead imports
11. [ ] Fix #1333 : vérifier protocole Widget Django 5.2+ sur WidgetMixin
12. [ ] Fix #1400 : reproduire + diagnostiquer incompatibilité django-formset
13. [ ] Fix dal_contenttypes absent de autocomplete.py
14. [ ] Publier release v4.0.0 sur PyPI
15. [ ] Docs : #1406, #1345, #1346, #1319
16. [ ] Fermer issues obsolètes (#1267, #1285, #1296, #100, #97)
17. [ ] Évaluer features : #1264, #1288, #1323
```
