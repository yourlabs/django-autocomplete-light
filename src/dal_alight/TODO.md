# dal_alight: gaps to replace dal_select2

## Python / widget side

### 1. `ModelAlightMultiple` widget
Add a second widget class for ManyToMany fields.
`ModelAlight` wraps `forms.Select`; this one wraps `forms.SelectMultiple`.
No other logic change needed — the web component already handles multiple
selection via the deck.

```python
class ModelAlightMultiple(QuerySetSelectMixin, AlightWidgetMixin, forms.SelectMultiple):
    pass
```

### 2. Initial value rendering
On an edit form, the selected object must appear pre-filled.
`dal_select2` solves this with `Select2InitialRenderMixin`, which temporarily
filters `self.choices.queryset` to only the current pk(s) before rendering.
Without this, the `<select>` renders with no `<option>` and the deck is empty.

Add an equivalent mixin to `AlightWidgetMixin` (or as a separate mixin applied
to both `ModelAlight` and `ModelAlightMultiple`).

### 3. Forward: render the config div
`AlightWidgetMixin.render()` does not call `render_forward_conf()`.
The forward config div (`<div class="dal-forward-conf">…</div>`) is never
emitted, so the JS has nothing to read.

Fix: call `render_forward_conf()` inside `AlightWidgetMixin.render()` and
append it to the output, exactly as `WidgetMixin.render()` does for Select2.

---

## JS side (new file: `dal_alight/static/dal_alight/dal-django.js`)

A thin Django-specific adapter. Loaded via `AlightWidgetMixin.media` alongside
`autocomplete-light.js`.

### 4. Forward: read and append to URL
For each `<autocomplete-select-input>` on the page, read its sibling
`dal-forward-conf` div (same format `autocomplete_light.js` uses for Select2),
collect the current values of the referenced form fields, and monkey-patch or
subclass the component's `url` getter to append `&forward=<json>`.

The forward config JSON format is already defined in `dal/forward.py` and the
existing `autocomplete_light.js` has `yl.getForwards()` as reference for how
to walk the DOM and build the dict.

### 5. Create POST handler
Listen for `autocompleteCreate` events dispatched by the component.
On fire:
1. Read the CSRF token from `document.querySelector('[name=csrfmiddlewaretoken]')?.value`
   or parse `document.cookie` for `csrftoken`.
2. POST to the component's `url` attribute with body `text=<value>&csrfmiddlewaretoken=<token>`.
3. Parse the JSON response `{"id": "…", "text": "…"}`.
4. Build a synthetic `<div data-value="<id>"><text></div>` and call
   `autocompleteSelectEl.choiceSelect(syntheticNode)`.

This is intentionally not in the submodule because CSRF and the JSON response
shape are Django-specific.

---

## Integration / packaging

### 6. Export `ModelAlightMultiple` from `dal/autocomplete.py`
`dal/autocomplete.py` re-exports everything; add `ModelAlightMultiple` there
alongside `ModelAlight`.

### 7. Test app for ManyToMany
Add a `test_project/alight_many_to_many/` app mirroring `alight_foreign_key`
but using a ManyToMany field, to cover `ModelAlightMultiple` and the deck
behaviour.

### 8. Test app for forward/linked fields
Add a `test_project/alight_linked_data/` app mirroring `linked_data`, to cover
the forward feature end-to-end (widget renders config div, JS reads it,
view filters by `self.forwarded`).
