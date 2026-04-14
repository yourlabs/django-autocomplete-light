# Plan d'upgrade des tests

---

## Vue d'ensemble des problèmes identifiés

| Catégorie | Problèmes |
|---|---|
| Code mort Python 2 | `from __future__ import unicode_literals`, `super(Cls, self)`, `try/except ImportError` pour `django.urls` |
| API Django supprimée | `force_text` (supprimé Django 5.0), `MIDDLEWARE_CLASSES`, `SessionAuthenticationMiddleware`, `USE_L10N`, `django.core.urlresolvers` |
| Gardes de version mortes | `VERSION < (1, 10)`, `VERSION < (2, 0, 0)`, `VERSION < (4, 0)` dans settings |
| Bare except | `except:` sans type dans stories.py et test.py |
| Apps/deps obsolètes | `select2_tagging`, `select2_gm2m`, `select2_generic_m2m`, `mock` |
| OpenShift | Références à `OPENSHIFT_*` dans settings (projet mort) |

---

## Étape 1 — `src/dal/test/case.py`

**Problèmes :**
- L. 11–12 : `try/except ImportError` pour `django.urls.reverse` → `django.core.urlresolvers` supprimé depuis Django 2.0
- L. 88–91 : garde `VERSION < (1, 10)` dans `OptionMixin.create_option()` → branche morte
- L. 103 : `super(ContentTypeOptionMixin, self)` → vieux style

**Corrections :**
```python
# Avant
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

# Après
from django.urls import reverse
```
```python
# Avant
if VERSION < (1, 10):
    unique_name = unique_name.replace('-', '')
option, created = self.model.objects.get_or_create(name=unique_name)

# Après
option, created = self.model.objects.get_or_create(name=unique_name)
```
```python
# Avant
super(ContentTypeOptionMixin, self).create_option()
# Après
super().create_option()
```

Supprimer aussi l'import `from django import VERSION` devenu inutile.

---

## Étape 2 — `src/dal/test/stories.py`

**Problèmes :**
- L. 1 : `from __future__ import unicode_literals` → Python 2, inutile
- L. 159 et 267 : `except:` bare → mauvaise pratique, masque toute erreur
- Tous les `super(ClassName, self).__init__(...)` → vieux style

**Corrections :**
```python
# Supprimer
from __future__ import unicode_literals
```
```python
# Avant (submit, l. 159)
except:
    break
# Après
except Exception:
    break
```
```python
# Avant (InlineSelectOption.__init__, l. 267)
except:
    continue
# Après
except Exception:
    continue
```
```python
# Avant
super(InlineSelectOption, self).__init__(case, **kwargs)
# Après
super().__init__(case, **kwargs)
```
Idem pour `InlineSelectOptionMultiple`.

---

## Étape 3 — `src/dal_select2/test.py`

**Problème :**
- L. 26 : `except:` bare dans `wait_script()`

**Correction :**
```python
# Avant
except:
    time.sleep(.15)
# Après
except Exception:
    time.sleep(.15)
```

---

## Étape 4 — `test_project/settings/base.py`

C'est le fichier le plus chargé en dette technique.

**Supprimer entièrement :**
- Tout le bloc `OPENSHIFT_*` (infrastructure morte)
- `MIDDLEWARE_CLASSES` (supprimé Django 2.0, seul `MIDDLEWARE` subsiste)
- `SessionAuthenticationMiddleware` (supprimé Django 2.0, intégré dans `AuthenticationMiddleware`)
- `MIDDLEWARE_CLASSES` dans les blocs `if DEBUG`
- Le bloc `if django.VERSION < (2, 0, 0)` (apps gm2m/tagging) → les apps sont supprimées
- Le bloc `if django.VERSION < (4, 0): USE_L10N = True` → `USE_L10N` supprimé en Django 5.0

**Simplifier :**
```python
# Avant
if django.VERSION < (4, 0):
    USE_L10N = True
USE_TZ = True

# Après
USE_TZ = True
```

**Nettoyer `INSTALLED_APPS` :** retirer `select2_tagging`, `select2_gm2m`, `select2_generic_m2m`, `tagging`, `gm2m`, `genericm2m`.

---

## Étape 5 — `test_project/linked_data/test_views.py`

**Problèmes :**
- L. 9–11 : `try/except ImportError` pour `django.urls.reverse` → mort
- `force_text` de `django.utils.encoding` → renommé `force_str` en Django 4.0, **supprimé en Django 5.0**

**Corrections :**
```python
# Avant
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.utils.encoding import force_text

# Après
from django.urls import reverse
from django.utils.encoding import force_str
```
```python
# Avant
self.assertJSONEqual(force_text(response.content), ...)
self.assertEqual(force_text(response.content), 'Not a JSON object')

# Après
self.assertJSONEqual(force_str(response.content), ...)
self.assertEqual(force_str(response.content), 'Not a JSON object')
```

---

## Étape 6 — `test_project/select2_generic_foreign_key/test_forms.py`

**Problème :**
- L. 8–11 : `try/except ImportError` pour `django.urls.reverse` → mort

**Correction :**
```python
# Avant
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
# Après
from django.urls import reverse
```

---

## Étape 7 — `test_project/select2_generic_m2m/test_forms.py`

Même correction que l'étape 6 (même `try/except ImportError`).

À noter : ce fichier sera **supprimé entièrement** (étape 9) avec l'app `select2_generic_m2m`. Pas besoin de le corriger si la suppression est faite en premier.

---

## Étape 8 — `test_project/select2_tagging/test_forms.py`

Même `try/except ImportError`. Ce fichier sera **supprimé entièrement** avec l'app `select2_tagging` (étape 9).

---

## Étape 9 — Suppression des apps et fichiers obsolètes

Apps à supprimer dans `test_project/` :
- `select2_tagging/` (dépend de django-tagging, incompatible Django ≥ 2.0)
- `select2_gm2m/` (dépend de django-gm2m, idem)
- `select2_generic_m2m/` (dépend de django-generic-m2m, idem)

Fichiers de test dans `src/` associés (packages source) :
- `src/dal_genericm2m/` → supprimer
- `src/dal_gm2m/` → supprimer
- `src/dal_select2_tagging/` → supprimer

Dans `test_project/urls.py` : retirer les includes des 3 apps.
Dans `test_project/settings/base.py` : déjà traité à l'étape 4.

---

## Étape 10 — `test_project/requirements.txt`

```diff
- mock                    # built-in unittest.mock depuis Python 3.3
- django-tagging          # incompatible Django moderne
- django-gm2m             # incompatible Django moderne
- django-generic-m2m      # incompatible Django moderne
```

Vérifier les versions minimales des dépendances restantes compatibles Django 5.2+ :
- `django-querysetsequence` : vérifier support Django 5.2
- `django-nested-admin` : vérifier support Django 5.2
- `djhacker` : vérifier support Django 5.2
- `pytest-splinter` : vérifier compatibilité Selenium 4+

---

## Étape 11 — `test_project/select2_taggit/test_forms.py` (vérification)

Ce fichier utilise `FutureModelForm` et `TaggableManager`. Aucun problème de version identifié, mais vérifier que `django-taggit` est compatible avec Django 5.2+ avant de valider.

---

## Récapitulatif par fichier

| Fichier | Actions |
|---|---|
| `src/dal/test/case.py` | Supprimer import mort, garde VERSION, vieux super |
| `src/dal/test/stories.py` | Supprimer `__future__`, corriger bare except × 2, vieux super × 2 |
| `src/dal_select2/test.py` | Corriger bare except |
| `test_project/settings/base.py` | Supprimer OPENSHIFT, MIDDLEWARE_CLASSES, gardes VERSION, apps obsolètes |
| `test_project/linked_data/test_views.py` | `force_text` → `force_str`, import mort |
| `test_project/select2_generic_foreign_key/test_forms.py` | Import mort |
| `test_project/select2_generic_m2m/test_forms.py` | Supprimé avec l'app |
| `test_project/select2_tagging/test_forms.py` | Supprimé avec l'app |
| `test_project/select2_tagging/` | Supprimer le dossier |
| `test_project/select2_gm2m/` | Supprimer le dossier |
| `test_project/select2_generic_m2m/` | Supprimer le dossier |
| `src/dal_genericm2m/` | Supprimer |
| `src/dal_gm2m/` | Supprimer |
| `src/dal_select2_tagging/` | Supprimer |
| `test_project/requirements.txt` | Supprimer mock, tagging, gm2m, generic-m2m |

---

## Ce qui ne change pas

Les fichiers de test suivants sont propres et n'ont pas besoin de modification :

- `src/dal/test/utils.py` — pas de dette technique identifiée
- `test_project/select2_foreign_key/test_functional.py` — propre
- `test_project/select2_many_to_many/test_functional.py` — propre
- `test_project/select2_one_to_one/test_functional.py` — propre
- `test_project/select2_generic_foreign_key/test_functional.py` — propre
- `test_project/select2_list/test_fields.py` — propre
- `test_project/select2_list/test_views.py` — propre
- `test_project/select2_list/test_functional.py` — propre
- `test_project/select2_nestedadmin/test_functional.py` — propre
- `test_project/secure_data/test_functional.py` — propre
- `test_project/linked_data/test_forms.py` — propre
- `test_project/linked_data/test_functional.py` — propre
- `test_project/select2_generic_foreign_key/test_views.py` — propre
- `test_project/rename_forward/test_functional.py` — propre
- `test_project/custom_select2/test_functional.py` — propre
- `test_project/select2_djhacker_formfield/test_functional.py` — propre
- `test_project/select2_taggit/test_forms.py` — propre (sous réserve compatibilité taggit)
- `conftest.py` (racine) — propre
