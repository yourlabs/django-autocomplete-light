/**
 * Django-specific adapter for autocomplete-light web components.
 *
 * Responsibilities:
 *  1. Forward: read the dal-forward-conf div emitted by AlightWidgetMixin and
 *     append &forward=<json> to every autocomplete URL request.
 *  2. Create: listen for autocompleteCreate events, POST to the view with the
 *     CSRF token, then feed the returned HTML fragment into choiceSelect().
 *  3. Popup sync: when Django admin's "add related" popup creates an object,
 *     sync it into the deck via choiceSelect().
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

    // Multiple hidden inputs with the same name (alight multi-select).
    if (fields.length > 1 && fields.every(function (f) { return f.type === 'hidden' })) {
      var hiddenValues = fields.map(function (f) { return f.value }).filter(function (v) { return v !== '' })
      return hiddenValues.length ? hiddenValues : undefined
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
  function getSearchInput(autocompleteSelectEl) {
    return autocompleteSelectEl.querySelector(
      'autocomplete-select-input [slot=input], autocomplete-light [slot=input]'
    )
  }

  function getFormPrefixes(autocompleteSelectEl, form) {
    var input = getSearchInput(autocompleteSelectEl)
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

  function getSelfValue(autocompleteSelectEl) {
    var inputs = Array.from(autocompleteSelectEl.querySelectorAll('[slot=values]'))
    if (!inputs.length) return undefined
    var values = inputs.map(function (input) { return input.value }).filter(function (v) { return v !== '' })
    if (!values.length) return undefined
    if (autocompleteSelectEl.hasAttribute('data-multiple')) {
      return values
    }
    return values[0]
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
        data[dst] = getSelfValue(autocompleteSelectEl)
      }
    })

    return Object.keys(data).length ? JSON.stringify(data) : null
  }

  // Expose buildForward so AutocompleteSelectInput.url can call it fresh on every request.
  window.AutocompleteLightBuildForward = buildForward

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
      var tmp = document.createElement('div')
      tmp.innerHTML = xhr.responseText.trim()
      var choice = tmp.firstElementChild
      if (!choice || !choice.hasAttribute('data-value')) return

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
    var el = document.getElementById(name)
    if (!el) return null
    if (el.tagName === 'AUTOCOMPLETE-SELECT') return el
    return el.closest('autocomplete-select')
  }

  // --- Related-object link enable/disable ----------------------------------

  /**
   * Django admin's updateRelatedObjectLinks uses nextAll() on the field
   * widget to find .view-related/.change-related buttons.  For our widget the
   * buttons are siblings of <autocomplete-select>, not of the value inputs.
   */
  function updateAlightRelatedLinks(acEl) {
    if (!acEl) return
    var value = getSelfValue(acEl)
    var linkValue = Array.isArray(value) ? value[0] : value
    var buttons = acEl.parentNode
      ? Array.from(acEl.parentNode.querySelectorAll('.view-related, .change-related, .delete-related'))
      : []
    buttons.forEach(function (btn) {
      if (linkValue) {
        var tmpl = btn.getAttribute('data-href-template')
        if (tmpl) btn.setAttribute('href', tmpl.replace('__fk__', linkValue))
        btn.removeAttribute('aria-disabled')
      } else {
        btn.removeAttribute('href')
        btn.setAttribute('aria-disabled', 'true')
      }
    })
  }

  // --- Django admin popup sync -----------------------------------------------

  document.addEventListener('DOMContentLoaded', function () {
    // Initial state for widgets that already have a value (edit forms).
    document.querySelectorAll('autocomplete-select').forEach(function (acEl) {
      updateAlightRelatedLinks(acEl)
      acEl.addEventListener('change', function () {
        updateAlightRelatedLinks(acEl)
      })
    })
    var origAdd = window.dismissAddRelatedObjectPopup
    window.dismissAddRelatedObjectPopup = function (win, newId, newRepr) {
      var el = findAutocompleteSelect(win.name)
      if (el) {
        var choice = document.createElement('div')
        choice.setAttribute('data-value', String(newId))
        choice.textContent = String(newRepr)
        el.choiceSelect(choice)
        win.close()
        return
      }
      if (origAdd) origAdd.call(this, win, newId, newRepr)
    }

    var origChange = window.dismissChangeRelatedObjectPopup
    window.dismissChangeRelatedObjectPopup = function (win, objId, newRepr, newId) {
      var el = findAutocompleteSelect(win.name)
      if (el) {
        el.choiceUpdate(String(objId), String(newRepr), String(newId))
        win.close()
        return
      }
      if (origChange) origChange.call(this, win, objId, newRepr, newId)
    }
  })
})()
