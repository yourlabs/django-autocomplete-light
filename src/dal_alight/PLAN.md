# dal_alight — Implementation Plan

## Sequencing (order matters)

1. **B1** — `TaggitAlight` widget (unblocks B2)
2. **B3** — `dal_alight_queryset_sequence` package (unblocks B4)
3. **A1–A5** — test apps with no new production code (any order, parallel)
4. **B2** — `alight_taggit` test app (needs B1)
5. **B4** — `alight_generic_foreign_key` test app (needs B3)
6. **B5** — `alight_nestedadmin` test app
7. **B6** — `alight_djhacker_formfield` test app

---

## Group A — Scaffold-only test apps

### A1. `test_project/alight_one_to_one/`
Mirrors `select2_one_to_one/`.

- `models.py`: `TModel(name CharField with validate_slug, test OneToOneField('self'), for_inline ForeignKey('self'))`
- `forms.py`: `TForm` using `autocomplete.ModelAlight(url='alight_one_to_one_autocomplete')`
- `admin.py`: `TestInline(TabularInline, fk_name='for_inline')` + `TestAdmin(inlines=[TestInline])`
- `urls.py`: autocomplete view with `create_field='name', validate_create=True`
- `test_functional.py`: `AdminOneToOneTestCase` — tests `test_can_create_option_on_the_fly` and `test_create_option_validation` (slug-validator triggers `.invalid-feedback` markup)
- Use `autocomplete.FutureModelForm` (needed for `validate_create=True` flow)
- Run `manage.py makemigrations alight_one_to_one` for migration

### A2. `test_project/alight_forward_different_fields/`
Mirrors `forward_different_fields/`.

- `models.py`: `TModel(name CharField)` only
- `forms.py`: swap `Select2ListChoiceField` → `AlightListChoiceField`, `ListSelect2` → `ListAlight`; keep all `forward.JavaScript`/`forward.Self` wiring and `Media.js = ('js_handlers.js',)` unchanged
- `static/js_handlers.js`: copy verbatim from the select2 sibling
- `tests.py`: placeholder (select2 sibling has none)
- No functional tests in the select2 sibling, so none here either

### A3. `test_project/alight_rename_forward/`
Mirrors `rename_forward/`.

- `models.py`: `TModel` with `owner ForeignKey('auth.user')` and `test ForeignKey('self')`. Use `_arf` suffix on related_names to avoid collisions with the select2 sibling
- `forms.py`: widget `ModelAlight(url='alight_linked_data_rf', forward=(Field('owner','possessor'), Const(42,'secret')))`
- `urls.py`: `LinkedDataView` filters by `possessor` + checks `secret == 42`
- `test_functional.py`: `AdminRenameForwardTest` asserts that only the logged-in user's records appear (uses `OwnedFixtures`)

### A4. `test_project/alight_secure_data/`
Mirrors `secure_data/`.

- `models.py`: same shape as rename_forward but `_asd` suffixes on related_names
- `views.py`: `SecureDataView` filters `queryset` by `request.user`
- `admin.py`: `SecureFormMixin` overrides `get_form` to restrict `test` queryset to `request.user`-owned rows
- `apps.py`: `ready()` connects `post_migrate` to `OwnedFixtures()`
- `test_functional.py`: `AdminLinkedDataTest` verifies only owned rows show in the autocomplete

### A5. `test_project/alight_outside_admin/`
Mirrors `select2_outside_admin/`, but uses `alight_foreign_key` (not `alight_many_to_many`) because `alight_foreign_key.models.TModel` has `for_inline` while `alight_many_to_many` does not.

- No models (reuses `alight_foreign_key`)
- `views.py`: `UpdateView` with `inlineformset_factory(TModel, TModel, fk_name='for_inline')`
- `templates/alight_outside_admin.html`: copy from the select2 sibling
- No functional tests (matching select2 sibling)

---

## Group B — New production code + test apps

### B1. `TaggitAlight` widget — append to `src/dal_alight/widgets.py`

```python
class TaggitAlight(TagAlight):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        # trailing comma keeps multi-word single tags intact for taggit's parser
        if value and ',' not in value:
            value = '%s,' % value
        return value

    def option_value(self, value):
        # taggit may yield TaggedItem objects on initial render
        return value.tag.name if hasattr(value, 'tag') else value
```

Then extend `src/dal/autocomplete.py`:
```python
if _installed('dal_alight') and _installed('taggit'):
    from dal_alight.widgets import TaggitAlight
```

No `build_attrs` override needed — the `data-tags` attribute is select2-specific.

### B2. `test_project/alight_taggit/`
Mirrors `select2_taggit/`.

- `models.py`: `TModel(name CharField, test=TaggableManager(), for_inline FK self)`
- `forms.py`: `TForm` with `widget=autocomplete.TaggitAlight('alight_taggit')`
- `urls.py`: `AlightQuerySetView(queryset=Tag.objects.order_by('name'))` named `alight_taggit`
- `test_functional.py`: `TaggitAlightAdminTest` — `test_can_select_options` and `test_can_select_option_in_first_inline`
- `test_forms.py`: port from select2 sibling; replace the `assertHTMLEqual` in `test_initial` with an `assertIn` check for the selected `<option>` value
- Migration depends on `('taggit', '0002_auto_20150616_2121')`

### B3. New package `src/dal_alight_queryset_sequence/`

**`views.py`** — `AlightQuerySetSequenceView(BaseQuerySetSequenceView)`:
- `render_to_response`: groups results by model type, emits grouped HTML fragments same as `AlightGroupQuerySetView`
- `AlightQuerySetSequenceAutoView`: auto-generated view with `get_queryset` that builds filters from `model_choice` + forwarded fields

**`widgets.py`**:
- `QuerySetSequenceAlight(AlightInitialRenderMixin, QuerySetSequenceSelectMixin, AlightWidgetMixin, forms.Select)`
- `QuerySetSequenceAlightMultiple(...)` with `forms.SelectMultiple`

**`fields.py`** — `AlightGenericForeignKeyModelField(QuerySetSequenceModelField)`:
- `as_url(form)` auto-generates the URL pattern and assigns `QuerySetSequenceAlight` as widget

`src/dal/autocomplete.py` additions (guarded by `_installed('dal_alight', 'dal_queryset_sequence')`):
```python
from dal_alight_queryset_sequence.views import AlightQuerySetSequenceView
from dal_alight_queryset_sequence.widgets import QuerySetSequenceAlight, QuerySetSequenceAlightMultiple
from dal_alight_queryset_sequence.fields import AlightGenericForeignKeyModelField
```

`pyproject.toml`: verify `dal_alight_queryset_sequence` is auto-discovered or add it explicitly.

### B4. `test_project/alight_generic_foreign_key/`
Mirrors `select2_generic_foreign_key/`.

- `models.py`: `TModel` with two GFKs (`content_type`+`object_id`+`test`, `content_type2`+`object_id2`+`test2`), `for_inline FK self`; plus `TProxyModel(TModel)` proxy
- `forms.py`: `TForm(FutureModelForm)` with `test = AlightGenericForeignKeyModelField(model_choice=...)` and `test2 = GenericForeignKeyModelField(widget=QuerySetSequenceAlight, view=AlightQuerySetSequenceView)`
- `urls.py`: `urlpatterns = [...update view...]; urlpatterns.extend(TForm.as_urls())`
- `test_functional.py`: `AdminGenericForeignKeyTestCase(AlightStory, case.AdminMixin, case.ContentTypeOptionMixin, case.AutocompleteTestCase)` — three test methods mirroring the select2 sibling
- `test_forms.py`: port save/validate tests; replace `assertHTMLEqual` with `assertIn` for the rendered widget HTML
- `apps.py`: `ready()` connects fixtures for both `TModel` and `auth.Group`

### B5. `test_project/alight_nestedadmin/`
Mirrors `select2_nestedadmin/`.

- `models.py`: `TModelOne(name, level_one='one')`, `TModelTwo(name, level_two='two', parent FK TModelOne)`, `TModelThree(name, parent FK TModelTwo, test FK self)`
- `admin.py`: nested inlines via `nested_admin.NestedStackedInline`/`NestedModelAdmin`
- `forms.py`: `TFormThree` with `ModelAlight(url='nested_alight_linked_data', forward=('level_one','level_two'))`
- `urls.py`: `LinkedDataView` raises an error if `level_one` or `level_two` are missing from forwarded
- `test_functional.py`: XHR override script intercepts the autocomplete request and captures the `forward` query param; asserts `{'level_one': 'one', 'level_two': 'two'}` is present

### B6. `test_project/alight_djhacker_formfield/`
Mirrors `select2_djhacker_formfield/`.

- `models.py`: `TModel(name, test FK self, for_inline FK self)` — use `_adf` related_name suffixes
- `admin.py`: `TestInline(fk_name='for_inline')` + `TestAdmin(inlines=[TestInline])`, no custom form (djhacker replaces it)
- `urls.py`: define URL patterns, then `djhacker.formfield(TModel.test, forms.ModelChoiceField, widget=autocomplete.ModelAlight(url='alight_djhacker_formfield'))` — import after `urlpatterns` (E402 lint exception needed in `pyproject.toml`)
- `test_functional.py`: inherit `alight_foreign_key.test_functional.AdminForeignKeyTestCase`, swap model

---

## Settings / URLs additions

### `test_project/settings/base.py` — add to `INSTALLED_APPS`:
```python
'alight_one_to_one',
'alight_forward_different_fields',
'alight_rename_forward',
'alight_secure_data',
'alight_outside_admin',
'alight_taggit',
'alight_generic_foreign_key',
'alight_nestedadmin',
'alight_djhacker_formfield',
```

### `test_project/urls.py` — add:
```python
url(r'^alight_one_to_one/', include('alight_one_to_one.urls')),
url(r'^alight_forward_different_fields/', include('alight_forward_different_fields.urls')),
url(r'^alight_rename_forward/', include('alight_rename_forward.urls')),
url(r'^alight_secure_data/', include('alight_secure_data.urls')),
url(r'^alight_outside_admin/', include('alight_outside_admin.urls')),
url(r'^alight_taggit/', include('alight_taggit.urls')),
url(r'^alight_generic_foreign_key/', include('alight_generic_foreign_key.urls')),
url(r'^alight_nestedadmin/', include('alight_nestedadmin.urls')),
url(r'^alight_djhacker_formfield/', include('alight_djhacker_formfield.urls')),
```

---

## Cross-cutting gotchas

| Issue | Resolution |
|---|---|
| `related_name` collisions with select2 siblings | Add per-app suffixes: `_adf`, `_arf`, `_asd` |
| `test_initial` HTML equality | Replace `assertHTMLEqual` with `assertIn` for the selected `<option>` and URL |
| `alight_outside_admin` needs `for_inline` | Use `alight_foreign_key`, not `alight_many_to_many` |
| `validate_create` needs `FutureModelForm` | Use `autocomplete.FutureModelForm` in one_to_one and generic_fk forms |
| `djhacker` import after urlpatterns | Add `E402` exception in `pyproject.toml` ruff config |
| `dal_alight_queryset_sequence` package discovery | Verify `pyproject.toml` auto-discovers or add explicitly |
| Multi-word taggit tags | `value_from_datadict` appends trailing comma to single-value result |
| `TaggitAlight` initial render | `option_value` handles `TaggedItem` instances via `.tag.name` |
| `as_urls()` placement in generic_fk | Call `urlpatterns.extend(TForm.as_urls())` after importing `TForm` |
| Nested admin double-registration | Each app registers its own `TModelOne` — no clash |
