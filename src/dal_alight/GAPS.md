# dal_alight — gaps vs select2

Features present in `dal_select2` and its test apps that are not yet
implemented or demonstrated in `dal_alight`.

---

## 1. One-to-one field

**select2 app:** `select2_one_to_one`

A `OneToOneField` backed autocomplete. Functionally identical to a FK
autocomplete (`ModelAlight`) — the widget is the same, only the model field
type differs. Needs a test app `alight_one_to_one` to confirm it works and
to cover the uniqueness constraint edge case.

---

## 2. Generic foreign key (ContentType)

**select2 app:** `select2_generic_foreign_key`

Points to any model via `django.contrib.contenttypes`. Requires
`dal_queryset_sequence` (multi-queryset view) and
`dal_contenttypes` (GenericForeignKey field helpers).

Neither `AlightQuerySetSequenceView` nor alight contenttypes field mixins
exist yet.

---

## 3. QuerySet sequence / multi-model autocomplete

**select2 package:** `dal_select2_queryset_sequence`

A single autocomplete URL that searches across multiple models at once,
returning a heterogeneous list. Requires:
- `AlightQuerySetSequenceView`
- `AlightQuerySetSequenceWidget` (or mixin equivalent)

---

## 4. Nested admin

**select2 app:** `select2_nestedadmin`

Autocomplete widgets inside Django admin inlines that are themselves nested
inside other inlines (using `django-nested-admin`). Tests that multiple
widget instances on the same page initialise independently and that
dynamically added inline rows get working autocomplete widgets.

---

## 5. Taggit integration

**select2 app:** `select2_taggit` / widget `TaggitSelect2`

Proper tag management via `django-taggit` (tags stored as related objects,
not a raw CharField). Requires a `TaggitAlight` widget that bridges
`TagAlight` with taggit's `TaggedItemBase` API.

---

## 6. Forward with field renaming

**select2 app:** `forward_different_fields`

Forwarding a field's value under a different name to the view:
```python
forward=[Field('country', 'location')]
```
The view receives `self.forwarded['location']` instead of
`self.forwarded['country']`. This already works at the `dal` / `dal-django.js`
level but has no dedicated alight test app verifying it.

---

## 7. Rename forward

**select2 app:** `rename_forward`

A variant of forwarding where the destination key is renamed on the view
side. No dedicated alight test app.

---

## 8. Secure / permission-gated autocomplete

**select2 app:** `secure_data`

Autocomplete view that requires authentication and returns 403/empty for
anonymous users. `AlightQuerySetView` inherits `has_add_permission` checks
for create but there is no dedicated test covering auth-gated list responses.

---

## 9. djhacker formfield override

**select2 app:** `select2_djhacker_formfield`

Using `django-djhacker` to swap a model's default form field for an
autocomplete widget without touching `ModelAdmin.form`. No alight equivalent.

---

## 10. Outside-admin standalone form (dedicated test app)

**select2 app:** `select2_outside_admin`

A named test app proving the widget works in a plain Django view outside
the admin. The alight demo pages serve this purpose informally but there is
no standalone test app with functional tests confirming it.

---

## Summary table

| Feature                        | select2 | alight |
|-------------------------------|---------|--------|
| Foreign key                    | ✓       | ✓      |
| Many to many                   | ✓       | ✓      |
| One to one                     | ✓       | —      |
| Generic foreign key            | ✓       | —      |
| QuerySet sequence              | ✓       | —      |
| Forward / linked data          | ✓       | ✓      |
| Forward with field renaming    | ✓       | —      |
| List autocomplete              | ✓       | ✓      |
| Tag (raw CharField)            | ✓       | ✓      |
| Taggit integration             | ✓       | —      |
| Nested admin                   | ✓       | —      |
| Secure / permission-gated      | ✓       | —      |
| Outside-admin standalone       | ✓       | ✓ (demo only) |
| djhacker formfield             | ✓       | —      |
