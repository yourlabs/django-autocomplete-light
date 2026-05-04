# autocomplete-light — Feature Specification

This document describes a set of new features required in the `autocomplete-light`
web component to make it production-ready as a general-purpose autocomplete widget.
Each feature is specified with its HTML contract, expected JS behaviour, and CSS
hooks. No framework-specific logic is introduced — all features are designed to be
usable from any server-side stack.

---

## 1. `max-choices` HTML attribute

### Problem

`maxChoices` is currently hardcoded: `1` for non-multiple selects, `0` (unlimited)
for multiple. There is no way to configure it from HTML.

### Required behaviour

`AutocompleteSelect.connectedCallback` must read the attribute and use it:

```js
const attrMax = parseInt(this.getAttribute('max-choices'))
this.maxChoices = isNaN(attrMax) ? 0 : attrMax

if (!this.select.multiple) {
  this.maxChoices = 1  // non-multiple always stays 1
}
```

### HTML contract

```html
<!-- Allow selecting at most 3 values -->
<autocomplete-select max-choices="3">
  <select slot="select" name="tags" multiple></select>
  <div slot="deck"></div>
  <autocomplete-select-input slot="input" url="/autocomplete/">
    <input slot="input" type="text" />
  </autocomplete-select-input>
</autocomplete-select>
```

Omitting `max-choices` on a multiple select means unlimited (current default).

---

## 2. "No results" message

### Problem

When the server returns an empty HTML fragment, the dropdown opens but is completely
blank, giving the user no feedback.

### Required behaviour

At the end of `receive()`, after populating `this.box.innerHTML`, check whether any
selectable choices were inserted:

```js
if (this.box.querySelectorAll(this.choiceSelector).length === 0) {
  const el = document.createElement('div')
  el.className = 'autocomplete-light-no-results'
  el.textContent = this.getAttribute('no-results-text') || 'No results'
  this.box.appendChild(el)
}
```

The injected element must **not** carry `data-value` so it is never treated as a
selectable choice and never receives the `data-bound` idempotence mark.

### HTML contract

```html
<autocomplete-select-input slot="input" url="/autocomplete/"
                           no-results-text="No results found">
  <input slot="input" type="text" />
</autocomplete-select-input>
```

### CSS hook

```css
.autocomplete-light-no-results {
  padding: 6px 12px;
  color: #999;
  font-style: italic;
  cursor: default;
}
```

---

## 3. Loading indicator

### Problem

There is no visual feedback during the XHR. Users cannot tell whether the component
is fetching or idle.

### Required behaviour

- `download()` sets a `loading` attribute on the `<autocomplete-select-input>`
  element before the request starts.
- `receive()` removes it once the response has been processed.

```js
download() {
  this.setAttribute('loading', '')
  // … existing XHR setup …
}

receive(ev) {
  this.removeAttribute('loading')
  // … existing logic …
}
```

### CSS hook

Consumers style the loading state freely. A minimal default should be added to
`autocomplete-light.css`:

```css
autocomplete-select-input[loading] input {
  opacity: 0.6;
  cursor: wait;
}
```

No spinner image is imposed — the attribute alone is the contract.

---

## 4. i18n via HTML attributes

### Problem

All user-visible strings are currently hardcoded in JS (`❌`, future "No results",
"Create" text). This makes localisation impossible without patching the component.

### Required behaviour

Every user-visible string must be read from an HTML attribute with a sensible
English default. The component never hardcodes display text.

| Attribute | Element | Default value | Used in |
|---|---|---|---|
| `clear-text` | `<autocomplete-select>` | `×` | Clear button in `addClear()` |
| `no-results-text` | `<autocomplete-select-input>` | `No results` | No-results div (feature 2) |
| `create-text` | `<autocomplete-select>` | `Create "%(val)s"` | Create option div (feature 5) |

`%(val)s` in `create-text` is a placeholder replaced at runtime with the current
query string.

### Implementation

```js
// in addClear():
clear.textContent = this.closest('autocomplete-select')
  .getAttribute('clear-text') || '×'

// in receive() no-results branch:
el.textContent = this.getAttribute('no-results-text') || 'No results'

// in create option rendering (feature 5):
const tpl = this.getAttribute('create-text') || 'Create "%(val)s"'
el.textContent = tpl.replace('%(val)s', this.input.value)
```

### HTML contract

```html
<autocomplete-select clear-text="Remove" create-text="Add &quot;%(val)s&quot;">
  …
  <autocomplete-select-input slot="input" url="/autocomplete/"
                             no-results-text="Nothing found">
    <input slot="input" type="text" />
  </autocomplete-select-input>
</autocomplete-select>
```

---

## 5. Create option (generic POST)

### Problem

There is no way for the user to create a new value that does not yet exist in the
server's dataset.

### Protocol

This feature is split between server and component. The server signals that a create
option is available by including a special element in the HTML fragment it returns.
The component handles the UI and the POST.

#### 5a. Server-side HTML contract

When a create option should be offered, the server appends this element at the end
of the result fragment:

```html
<div data-create="true">Create "foo"</div>
```

Rules:
- **No `data-value` attribute** — the create div must never be treated as a regular
  selectable choice.
- Its visible text is set by the server (the `create-text` attribute from feature 4
  is the template the server uses to render it, or the component can re-render it
  client-side — either convention is acceptable; pick one and document it).
- It must be the last child of the response.

#### 5b. `choiceSelector` change (prerequisite)

Change the default `choiceSelector` from `[data-value]` to
`[data-value]:not([data-create])` so that create divs and any other special elements
are automatically excluded from keyboard navigation, `choices` lists, and the
`data-bound` idempotence check.

```js
get choiceSelector() {
  return this.getAttribute('choice-selector') || '[data-value]:not([data-create])'
}
```

#### 5c. Component behaviour on create click

When the user clicks (or presses Enter on) a `[data-create]` element:

1. Read `q = this.input.value` (the current search query).
2. POST to `this.getAttribute('url')` with body:
   ```
   text=<q>&csrfmiddlewaretoken=<token>
   ```
3. Read the CSRF token from, in order of preference:
   - The `csrfmiddlewaretoken` attribute on `<autocomplete-select>`.
   - `document.querySelector('[name=csrfmiddlewaretoken]')?.value`.
   - The `csrftoken` cookie (parse `document.cookie`).
4. On HTTP 200, parse the JSON response `{"id": "42", "text": "foo"}`:
   - Build a synthetic choice node: `<div data-value="42">foo</div>`
   - Call `choiceSelect(syntheticNode)` on the parent `AutocompleteSelect`
   - Clear `this.input.value`
   - Close the dropdown box
5. On any other status, log to console and leave the dropdown open.

#### 5d. Binding create items

In `receive()`, after the regular `[data-bound]` idempotence loop, bind create items
separately:

```js
this.box.querySelectorAll('[data-create]').forEach((item) => {
  if (item.getAttribute('data-bound')) return
  item.addEventListener('mouseenter', () => item.classList.add('hilight'))
  item.addEventListener('mouseleave', () => item.classList.remove('hilight'))
  item.addEventListener('mousedown', () => this.handleCreate())
  item.setAttribute('data-bound', 'true')
})
```

`handleCreate()` implements step 5c above.

#### 5e. Keyboard navigation for create items

After all regular choices, if the box contains a `[data-create]` item, it should be
reachable by arrow keys. Modify `move()` to use a wider selector for navigation:

```js
get navigationChoices() {
  return Array.from(this.box.querySelectorAll(
    this.choiceSelector + ', [data-create]'
  ))
}
```

Use `navigationChoices` in `move()` instead of `choices`. Only `choices` (which
excludes `[data-create]`) is used for regular selection.

### CSS hook

```css
[data-create] {
  font-style: italic;
  border-top: 1px solid #eee;
}
```

---

## 6. Keyboard navigation correctness with non-selectable items

### Problem

Group headers and other non-selectable items (items without `data-value`) currently
do not appear in `choices` if `choiceSelector` is correctly set (see feature 5b).
However `move()` must be verified to handle a box that mixes selectable and
non-selectable elements without landing on or skipping over choices incorrectly.

### Required behaviour

With the `choiceSelector` change from feature 5b, `this.choices` automatically
excludes non-selectable items. `move()` already iterates `this.choices`, so no
further changes are needed **as long as** `move()` uses `this.choices` (not a raw
`querySelectorAll` with a different selector). Verify this is the case and fix any
divergence.

Additionally, `navigationChoices` from feature 5e must also skip group headers
(items that are neither `[data-value]` nor `[data-create]`).

---

## 7. Pagination — "load more"

### Problem

One XHR fetches one page of results. When the dataset is large, users cannot access
results beyond the first page.

### Protocol

#### 7a. Server-side HTML contract

When more results exist on subsequent pages, the server appends at the end of the
fragment:

```html
<div data-next-page="2">Load more</div>
```

Rules:
- **No `data-value`** — not a selectable choice.
- `data-next-page` holds the integer page number to fetch next.
- Only one such element per response, always last.

#### 7b. Component behaviour

In `receive()`, after populating the box:

1. Find `this.box.querySelector('[data-next-page]')`.
2. If found, bind a `mousedown` handler on it:
   - Fetch `this.getAttribute('url') + '&page=' + nextPage`
   - On response: **append** the received HTML to `this.box` (do not replace
     `innerHTML`) after removing the old `[data-next-page]` element
   - The new fragment may itself end with a `[data-next-page]` for page 3 — the
     same binding logic applies recursively via the normal `receive()` flow
3. The `[data-next-page]` element is bound with `data-bound` idempotence like all
   other special items.

#### 7c. Keyboard navigation

`[data-next-page]` elements must not appear in `this.choices` or
`this.navigationChoices`. The `choiceSelector` from feature 5b already excludes them
since they carry neither `data-value` nor `data-create`. Verify this.

#### 7d. Page parameter in URL

The component appends `&page=N` to the existing URL. The server is responsible for
reading this parameter and returning the correct slice. The component does not need
to know or manage the total page count.

### CSS hook

```css
[data-next-page] {
  text-align: center;
  color: #666;
  cursor: pointer;
  border-top: 1px solid #eee;
}
[data-next-page]:hover {
  background: #f5f5f5;
}
```

---

## Implementation order recommendation

These features are largely independent. Suggested order:

1. **Feature 5b** — change `choiceSelector` default (zero risk, unlocks everything else)
2. **Feature 1** — `max-choices` attribute (trivial, standalone)
3. **Feature 3** — loading indicator (trivial, standalone)
4. **Feature 4** — i18n attributes (trivial, touches `addClear` and future strings)
5. **Feature 2** — no-results message (depends on 4 for `no-results-text`)
6. **Feature 6** — nav correctness (verify after 5b, no new code if 5b is correct)
7. **Feature 7** — pagination (standalone server/client protocol)
8. **Feature 5** — create option (most complex, depends on 4 and 5b)
