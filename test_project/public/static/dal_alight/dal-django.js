/**
 * Django-specific adapter for autocomplete-light web components.
 *
 * Responsibilities:
 *  1. Forward: read the dal-forward-conf div emitted by AlightWidgetMixin and
 *     append &forward=<json> to every autocomplete URL request.
 *  2. Create: listen for autocompleteCreate events, POST to the view with the
 *     CSRF token, then feed the returned {id, text} into choiceSelect().
 */

(function () {
  'use strict'

  // --- Forward helpers ------------------------------------------------------

  function getCsrfToken() {
    var el = document.querySelector('[name=csrfmiddlewaretoken]')
    if (el) return el.value
    var match = document.cookie.match(/csrftoken=([^;]+)/)
    return match ? match[1] : ''
  }

  /** Return the <form> ancestor of an element, or document as fallback. */
  function getForm(el) {
    return el.closest('form') || document
  }

  /**
   * Read values from a named field relative to the form that contains `el`.
   * Handles text inputs, selects, checkboxes, radios, and multi-selects.
   */
  function getFieldValue(form, name) {
    var fields = Array.from(form.querySelectorAll('[name="' + name + '"]'))
    if (!fields.length) return undefined

    // Multiple checkboxes with value → list of checked values
    if (fields.every(function (f) { return f.type === 'checkbox' && f.getAttribute('value') !== null })) {
      var checked = fields.filter(function (f) { return f.checked }).map(function (f) { return f.value })
      return checked.length ? checked : undefined
    }

    var f = fields[0]
    if (f.type === 'checkbox') return f.checked
    if (f.multiple) return Array.from(f.selectedOptions).map(function (o) { return o.value })
    return f.value || undefined
  }

  /**
   * Parse the dal-forward-conf script tag inside an autocomplete-select and
   * return a JSON-encoded forward dict, or null if nothing to forward.
   */
  function buildForward(autocompleteSelectEl) {
    var confDiv = autocompleteSelectEl.querySelector('.dal-forward-conf')
    if (!confDiv) return null

    var script = confDiv.querySelector('script[type="text/dal-forward-conf"]')
    if (!script) return null

    var list
    try {
      list = JSON.parse(script.textContent)
    } catch (e) {
      return null
    }
    if (!Array.isArray(list) || !list.length) return null

    var form = getForm(autocompleteSelectEl)
    var select = autocompleteSelectEl.querySelector('select')
    var data = {}

    list.forEach(function (field) {
      if (field.type === 'const') {
        data[field.dst] = field.val
      } else if (field.type === 'field') {
        var val = getFieldValue(form, field.src)
        if (val !== undefined) data[field.dst || field.src] = val
      } else if (field.type === 'self') {
        var dst = field.dst || 'self'
        if (select) data[dst] = select.value || undefined
      }
    })

    return Object.keys(data).length ? JSON.stringify(data) : null
  }

  // --- Patch AutocompleteSelectInput.url ------------------------------------

  /**
   * Wait until the custom element is defined, then override the url getter on
   * its prototype so that every request automatically appends forward data.
   */
  customElements.whenDefined('autocomplete-select-input').then(function () {
    var proto = customElements.get('autocomplete-select-input').prototype
    var originalDescriptor = Object.getOwnPropertyDescriptor(proto, 'url')
    if (!originalDescriptor) return

    Object.defineProperty(proto, 'url', {
      get: function () {
        var base = originalDescriptor.get.call(this)
        if (!base) return base

        var autocompleteSelectEl = this.closest('autocomplete-select')
        if (!autocompleteSelectEl) return base

        var forward = buildForward(autocompleteSelectEl)
        if (forward) base += '&forward=' + encodeURIComponent(forward)
        return base
      },
      configurable: true,
    })
  })

  // --- Create POST handler --------------------------------------------------

  document.addEventListener('autocompleteCreate', function (ev) {
    var inputEl = ev.target  // autocomplete-select-input
    var autocompleteSelectEl = inputEl.closest('autocomplete-select')
    if (!autocompleteSelectEl) return

    var urlAttr = inputEl.getAttribute('url')
    if (!urlAttr) return

    var text = ev.detail.value
    var csrf = getCsrfToken()
    var forward = buildForward(autocompleteSelectEl)

    var body = 'text=' + encodeURIComponent(text) + '&csrfmiddlewaretoken=' + encodeURIComponent(csrf)
    if (forward) body += '&forward=' + encodeURIComponent(forward)

    var xhr = new XMLHttpRequest()
    xhr.open('POST', urlAttr)
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    xhr.setRequestHeader('X-CSRFToken', csrf)
    xhr.addEventListener('load', function () {
      if (!(xhr.status >= 200 && xhr.status < 300)) return
      var result
      try {
        result = JSON.parse(xhr.responseText)
      } catch (e) { return }
      if (!result.id) return

      var choice = document.createElement('div')
      choice.setAttribute('data-value', result.id)
      choice.textContent = result.text || result.id

      autocompleteSelectEl.choiceSelect(choice)
    })
    xhr.send(body)
  })
})()
