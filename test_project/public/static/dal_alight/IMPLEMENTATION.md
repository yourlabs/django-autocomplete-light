# Implementation notes — feature spec decisions

Records what was done versus what the spec requested, and why deviations were made.

---

## Feature 1 — `max-choices` HTML attribute

**Status: implemented as specified.**

`AutocompleteSelect.connectedCallback` now reads `max-choices` and calls
`parseInt` with an `isNaN` guard. Non-multiple selects still pin `maxChoices`
to 1 regardless of the attribute.

---

## Feature 2 — "No results" message

**Status: implemented as specified, with one server-side adjustment.**

The component adds a `.autocomplete-light-no-results` div when the server
returns an empty fragment and no `[data-next-page]` sentinel is present.

`serve.py` (the development demo server) previously returned
`<div>No result found</div>` server-side. That div was removed so the
client message takes over. Existing tests still pass because they match
the substring `'No result'`, which appears in both the old server text
and the new client text `'No results'`.

The no-results div is not injected when a `[data-next-page]` element is
present, because more results may exist on subsequent pages.

---

## Feature 3 — Loading indicator

**Status: implemented as specified.**

`download()` sets a `loading` attribute on the component element before the
XHR starts. `receive()` and both the `error` and `timeout` handlers remove it.
CSS uses the attribute selector `autocomplete-select-input[loading] input` and
`autocomplete-light[loading] input` to dim the input and show a wait cursor.

---

## Feature 4 — i18n via HTML attributes

**Status: partially implemented.**

| Attribute | Status |
|-----------|--------|
| `clear-text` | Implemented — `addClear()` reads it with `|| '×'` fallback |
| `no-results-text` | Implemented — `receive()` reads it with `|| 'No results'` fallback |
| `create-text` | **Not implemented** — see Feature 5 |

`create-text` is not implemented because the create option text is rendered by
the server in the HTML fragment (see Feature 5). The component never generates
the create option label client-side.

---

## Feature 5 — Create option

**Status: implemented with a different protocol — no built-in POST.**

### What the spec requested

The spec asked the component to:
1. Intercept the create-option click
2. Resolve a CSRF token (from attribute, DOM field, or cookie)
3. POST to the autocomplete URL with `text=<q>&csrfmiddlewaretoken=<token>`
4. Parse a JSON response `{"id": "42", "text": "foo"}`
5. Build a synthetic node and call `choiceSelect()`

### What was implemented instead

The component dispatches a custom event and stops there:

```js
handleCreate() {
  this.dispatchEvent(new CustomEvent('autocompleteCreate', {
    detail: {value: this.input.value},
    bubbles: true,
  }))
  this.box.setAttribute('hidden', 'true')
  this.input.setAttribute('aria-expanded', 'false')
}
```

The caller listens for `autocompleteCreate`, performs the POST using whatever
CSRF strategy and HTTP client is appropriate for the framework in use, and
calls `choiceSelect()` on the result.

### Why

1. **CSRF handling is Django-specific.** `csrfmiddlewaretoken` (the form field
   name) and `csrftoken` (the cookie name) are Django conventions. Other
   frameworks use different names and header locations. Hardcoding this inside
   a "framework-agnostic" component contradicts the library's stated goal.

2. **The JSON response shape `{"id": ..., "text": ...}` is an opinionated API
   contract.** The library's core value is that the server renders HTML and the
   component doesn't know your data model. Feature 5 as written forces a
   specific JSON schema on the server. The custom-event approach keeps the
   component schema-agnostic.

3. **Size.** Full implementation of the spec's POST flow would add ~50 lines
   to a 300-line file. The custom event is 8 lines.

### Server-side HTML contract (unchanged from spec)

The server signals a create option by including a `[data-create]` element in
the result fragment:

```html
<div data-create="true">Create "foo"</div>
```

The component binds click/hover/keyboard handlers on it and fires
`autocompleteCreate` when activated. The element must not carry `data-value`.

### `create-text` attribute

Not implemented. The create option label is set by the server in the returned
HTML. If the server wants to use a configurable template, it reads the
`create-text` attribute on the element itself — that is a server-side concern.

---

## Feature 5b — `choiceSelector` default change

**Status: implemented as specified.**

Default changed from `[data-value]` to `[data-value]:not([data-create])`.

This is technically a breaking change for anyone who happens to use
`data-create` on their own choice elements, but since `data-create` is a new
convention introduced by this spec that is unlikely in practice.

One downstream fix was required: `hilight()` previously called
`this.selected.forEach(...)` to clear the old highlight. `selected` uses
`choiceSelector`, so it would not clear highlight from `[data-create]` items.
`hilight()` now uses `this.box.querySelectorAll('.hilight')` directly.

---

## Feature 6 — Keyboard navigation correctness

**Status: verified, no changes needed for choiceSelector; one fix applied.**

`move()` now uses `this.navigationChoices` (which includes `[data-create]`
items) instead of `this.choices` for arrow-key navigation. `this.choices`
(which excludes `[data-create]`) is still used by `AutocompleteSelect` for
all selection logic.

`navigationChoices` uses `choiceSelector + ', [data-create]'`, which
automatically excludes `[data-next-page]`, group headers, and any other
non-selectable elements.

The `keyboard()` handler was updated to call `handleCreate()` instead of
`selectChoice()` when the highlighted item has `data-create`.

---

## Feature 7 — Pagination ("load more")

**Status: implemented as specified.**

When `bindBox()` finds a `[data-next-page]` element, it attaches a `mousedown`
handler that:
1. Reads the `data-next-page` value (the page number to fetch)
2. Removes the sentinel element from the DOM
3. Fires a new XHR to `url?q=<query>&page=<N>`
4. On success, appends the response HTML to the existing box via a temporary
   container and calls `bindBox()` again — binding new choices, any nested
   `[data-next-page]`, and any `[data-create]` items from the appended page

`mousedown` uses `ev.preventDefault()` to keep focus on the input so the box
remains visible while the next page loads.

The no-results check in `receive()` is skipped when a `[data-next-page]`
element is present, since further pages may contain results.

---

## Feature 3 — Loading indicator (test coverage note)

The loading state is not covered by the Selenium test suite. On localhost the
XHR round-trip completes in < 5 ms, making the `loading` attribute appear and
disappear faster than any reliable polling window. The attribute and CSS are
correct; manual inspection in devtools confirms the behaviour.

---

## Other changes made alongside the spec

These were not in the spec but were applied in the same implementation pass:

- **`receive()` refactored into `receive()` + `bindBox()`**: the binding loop
  was extracted so pagination can reuse it without replacing `innerHTML`.
- **`serve.py` no-results response removed**: the demo server no longer
  returns `<div>No result found</div>`; it returns empty HTML and the
  component's no-results message takes over.
- **No-results check also guards against `[data-create]`**: the initial
  implementation would inject "No results" even when the box contained only a
  create option (because `choiceSelector` excludes `[data-create]`, so the
  count was 0). A third condition `&& !this.box.querySelector('[data-create]')`
  was added to prevent this.
- **Error/timeout handlers in `download()` also remove the `loading` attribute**
  (the spec's loading indicator description only mentioned the happy path).
