# dal_alight: roadmap toward full select2 parity

## Completed (original batch)

- [x] `ModelAlightMultiple` widget (wraps `forms.SelectMultiple`)
- [x] `AlightInitialRenderMixin` — pre-fills selected values on edit forms
- [x] Forward config div emitted by `WidgetMixin.render()` via MRO
- [x] `dal-django.js` — reads `dal-forward-conf`, appends `&forward=` to URL
- [x] `dal-django.js` — `autocompleteCreate` handler: POST + `choiceSelect()`
- [x] Export `ModelAlightMultiple` from `dal/autocomplete.py`
- [x] Test app `alight_many_to_many` (M2M scaffolding)
- [x] Test app `alight_linked_data` (forward scaffolding)

## Completed (full parity batch)

- [x] `create_field` support in `AlightQuerySetView`
- [x] `AlightListView` — list-based autocomplete (mirrors `Select2ListView`)
- [x] `AlightGroupQuerySetView` — grouped queryset (mirrors `Select2GroupQuerySetView`)
- [x] `AlightGroupListView` — grouped list (mirrors `Select2GroupListView`)
- [x] `Alight` widget — non-queryset single (mirrors `Select2`)
- [x] `AlightMultiple` widget — non-queryset multiple (mirrors `Select2Multiple`)
- [x] `ListAlight` widget — list-backed, used with `AlightListView`
- [x] `TagAlight` widget — free-text tag mode (mirrors `TagSelect2`)
- [x] `AlightListChoiceField` — list choice field (mirrors `Select2ListChoiceField`)
- [x] `AlightListCreateChoiceField` — skip validation (mirrors `Select2ListCreateChoiceField`)
- [x] `dal_alight/test.py` — `AlightStory` with alight-specific CSS selectors
- [x] Unit tests: views, widgets, fields (`dal_alight/tests.py`)
- [x] Functional tests: `alight_foreign_key/test_functional.py`
- [x] Functional tests: `alight_many_to_many/test_functional.py`
- [x] Functional tests: `alight_linked_data/test_functional.py`
- [x] Test app `alight_list` + `test_functional.py`
- [x] Test app `alight_tag` + `test_functional.py`
- [x] Export all new classes from `dal/autocomplete.py`

---

## Pending (gaps vs select2 — see GAPS.md)

### Test apps (no new Python code needed, widget already works)
- [ ] Test app `alight_one_to_one` — `OneToOneField` + `ModelAlight`, functional tests
- [ ] Test app `alight_forward_different_fields` — `Field('src', 'dst')` forwarding, functional tests
- [ ] Test app `alight_rename_forward` — forwarded key renamed on view side, functional tests
- [ ] Test app `alight_secure_data` — auth-gated `AlightQuerySetView`, functional tests covering 403 for anon
- [ ] Test app `alight_outside_admin` — standalone form page with functional tests (currently demo-only)

### New code required
- [ ] `AlightQuerySetSequenceView` — multi-queryset autocomplete (mirrors `Select2QuerySetSequenceView`)
- [ ] `AlightQuerySetSequenceWidget` / mixin — widget for heterogeneous results
- [ ] Test app `alight_generic_foreign_key` — ContentType-based GFK using the above
- [ ] `TaggitAlight` widget — bridges `TagAlight` with `django-taggit` (mirrors `TaggitSelect2`)
- [ ] Test app `alight_taggit` — taggit-backed tag autocomplete, functional tests
- [ ] Nested admin support — verify widget init in dynamically added inline rows, test app `alight_nestedadmin`
- [ ] Test app `alight_djhacker_formfield` — `django-djhacker` formfield override

### Demo pages to add once code exists
- [ ] `/one_to_one/` — one-to-one autocomplete
- [ ] `/generic_fk/` — generic foreign key autocomplete
- [ ] `/taggit/` — taggit tag autocomplete

---

## Feature notes

### create_field HTML fragment
`AlightQuerySetView` appends `<div data-create data-value="{q}">Create "{q}"</div>`
when `create_field` is set and no case-insensitive exact match exists in page 1.
The `dal-django.js` `autocompleteCreate` handler POSTs to the view and feeds
the JSON response into `autocompleteSelectEl.choiceSelect()`.

### Grouping HTML convention
`AlightGroupQuerySetView` and `AlightGroupListView` wrap items in:
```html
<div class="autocomplete-light-group">Group label</div>
<div data-value="1">Item</div>
```
Group header divs have no `data-value` so the component skips them during
keyboard navigation and selection.

### TagAlight storage
Values are stored as comma-separated text (the tag text IS the value, no PK).
`value_from_datadict` joins the multiselect values with `','`.
`optgroups` renders each tag as a pre-selected `<option value="tag">tag</option>`.
Use with `AlightListView` (with `create()`) as the URL source.

### Alight / AlightMultiple (non-queryset)
When no `url` is set the `autocomplete-select-input` component filters
`<option>` tags locally in JS — no server round-trip needed.
When a `url` is set the view is called normally.
