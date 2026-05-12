/**
 * Django-specific adapter for autocomplete-light web components.
 *
 * Responsibilities:
 *  1. Forward: read the dal-forward-conf div emitted by AlightWidgetMixin and
 *     append &forward=<json> to every autocomplete URL request.
 *  2. Create: listen for autocompleteCreate events, POST to the view with the
 *     CSRF token, then feed the returned {id, text} into choiceSelect().
 *  3. Popup sync: when Django admin's "add related" popup creates an object and
 *     adds an option to the native <select>, sync it into the deck via a
 *     change-event listener so the component reflects the new selection.
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
    return f.value !== '' ? f.value : undefined
  }

  /**
   * Return a list of form-field prefixes to try when resolving a forwarded
   * field name, mirroring select2's getFormPrefixes logic.
   *
   * Nested admin inlines use prefixed names like "tmodeltwo_set-0-level_two".
   * We derive candidate prefixes from the autocomplete widget's own input name
   * (e.g. "tmodeltwo_set-0-tmodelthree_set-0-test-input") by stripping the
   * trailing "-input" suffix and the last segment, then trying successively
   * shorter prefix strings (skipping every other segment so we step across
   * formset "name-index" pairs).  The empty prefix (exact match) is always
   * tried last.
   */
  function getFormPrefixes(autocompleteSelectEl, form) {
    var input = autocompleteSelectEl.querySelector('input[name]')
    if (!input) return ['']
    var parts = input.getAttribute('name').replace(/-input$/, '').split('-').slice(0, -1)
    var prefixes = []
    for (var i = 0; i < parts.length; i += 2) {
      var prefix = parts.slice(0, parts.length - i).join('-') + '-'
      if (form.querySelector('[name^="' + prefix + '"]')) {
        prefixes.push(prefix)
      }
    }
    prefixes.push('')
    return prefixes
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
        var prefixes = getFormPrefixes(autocompleteSelectEl, form)
        for (var i = 0; i < prefixes.length; i++) {
          var val = getFieldValue(form, prefixes[i] + field.src)
          if (val !== undefined) {
            data[field.dst || field.src] = val
            break
          }
        }
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

  // --- Popup sync (Django admin "add/change related" popups) ---------------

  /**
   * Django admin's dismissAddRelatedObjectPopup uses jQuery's $(elem).trigger()
   * which does NOT fire native addEventListener handlers — it only fires jQuery-
   * registered handlers.  So we patch the dismiss functions directly.
   *
   * dal-django.js is loaded as form media, which Django admin includes AFTER its
   * own core scripts (RelatedObjectLookups.js), so window.dismissAdd… is already
   * defined by the time this runs.
   */
  function findAutocompleteSelect(winName) {
    // Django admin's removePopupIndex strips "__N" suffix (double underscore + popup index).
    var name = winName.replace(/__\d+$/, '')
    var select = document.getElementById(name)
    if (!select) return null
    return select.closest('autocomplete-select')
  }

  // Defer patching until DOMContentLoaded so that RelatedObjectLookups.js
  // (which loads after dal-django.js in the merged media) has already run
  // and defined window.dismissAddRelatedObjectPopup.
  // --- Related-object link enable/disable ----------------------------------

  /**
   * Django admin's updateRelatedObjectLinks uses nextAll() on the <select>
   * to find .view-related/.change-related buttons.  For our widget the
   * <select> is nested inside <autocomplete-select>, so the buttons are
   * siblings of <autocomplete-select>, not of <select>.  We traverse up
   * first, then look sideways.
   */
  function updateAlightRelatedLinks(select) {
    var acEl = select.closest('autocomplete-select')
    if (!acEl) return
    var value = select.value
    var buttons = acEl.parentNode
      ? Array.from(acEl.parentNode.querySelectorAll('.view-related, .change-related, .delete-related'))
      : []
    buttons.forEach(function (btn) {
      if (value) {
        var tmpl = btn.getAttribute('data-href-template')
        if (tmpl) btn.setAttribute('href', tmpl.replace('__fk__', value))
        btn.removeAttribute('aria-disabled')
      } else {
        btn.removeAttribute('href')
        btn.setAttribute('aria-disabled', 'true')
      }
    })
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Initial state for selects that already have a value (edit forms).
    document.querySelectorAll('autocomplete-select select').forEach(function (select) {
      updateAlightRelatedLinks(select)
      select.addEventListener('change', function () {
        updateAlightRelatedLinks(select)
      })
    })
    var origAdd = window.dismissAddRelatedObjectPopup
    window.dismissAddRelatedObjectPopup = function (win, newId, newRepr) {
      if (origAdd) origAdd.call(this, win, newId, newRepr)
      var el = findAutocompleteSelect(win.name)
      if (!el) return
      var choice = document.createElement('div')
      choice.setAttribute('data-value', String(newId))
      choice.textContent = String(newRepr)
      el.choiceSelect(choice)
    }

    var origChange = window.dismissChangeRelatedObjectPopup
    window.dismissChangeRelatedObjectPopup = function (win, objId, newRepr, newId) {
      if (origChange) origChange.call(this, win, objId, newRepr, newId)
      var el = findAutocompleteSelect(win.name)
      if (!el) return
      var deck = el.querySelector('[slot="deck"]')
      if (!deck) return
      var item = deck.querySelector('[data-value="' + String(objId) + '"]')
      if (!item) return
      var clearSpan = item.querySelector('.clear')
      item.textContent = String(newRepr)
      if (clearSpan) item.appendChild(clearSpan)
    }
  })
})()
