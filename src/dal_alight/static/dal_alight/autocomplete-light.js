class AutocompleteLight extends HTMLElement {
  box = null
  xhr = null
  timeoutId = null

  connectedCallback(retries = 20) {
    this.input = this.querySelector('[slot=input]')
    if (!this.input) {
      if (retries > 0) setTimeout(() => this.connectedCallback(retries - 1), 100)
      return
    }

    this.input.setAttribute('aria-haspopup', 'listbox')
    this.input.setAttribute('aria-autocomplete', 'list')
    this.input.setAttribute('aria-expanded', 'false')

    this.input.addEventListener(
      'focus',
      () => this.input.value.length >= this.minimumCharacters && this.onInput()
    )
    this.input.addEventListener('keydown', this.keyboard.bind(this))
    this.input.addEventListener('input', this.onInput.bind(this))
    window.addEventListener('resize', () => {
      if (this.box) {
        this.box.setAttribute('hidden', 'true')
        this.input.setAttribute('aria-expanded', 'false')
      }
    })
    this.setAttribute('data-bound', 'true')
  }

  get hidden() {
    return this.input.getAttribute('hidden')
  }

  set hidden(value) {
    if (value) {
      this.input.setAttribute('hidden', 'true')
    } else {
      this.input.removeAttribute('hidden')
    }
  }

  onInput() {
    if (this.input.value.length < this.minimumCharacters) {
      this.box && this.box.setAttribute('hidden', 'true')
      this.input.setAttribute('aria-expanded', 'false')
      return
    }
    // abort any pending or in-flight xhr so stale responses never overwrite the box
    this.xhr && this.xhr.readyState !== 4 && this.xhr.abort()
    // clear any planned xhr
    this.timeoutId && window.clearTimeout(this.timeoutId)
    // debounce: 200ms
    this.timeoutId = window.setTimeout(this.download.bind(this), 200)
  }

  hilight(choice) {
    // Use .hilight directly so [data-create] items also get cleared.
    this.box.querySelectorAll('.hilight').forEach((item) => {
      item.classList.remove('hilight')
      item.setAttribute('aria-selected', 'false')
    })
    choice.classList.add('hilight')
    choice.setAttribute('aria-selected', 'true')
  }

  selectChoice(choice) {
    this.dispatchEvent(new CustomEvent('autocompleteChoiceSelected', {
      detail: {choice},
      bubbles: true,
    }))
    this.box.setAttribute('hidden', 'true')
    this.input.setAttribute('aria-expanded', 'false')
  }

  handleCreate() {
    this.dispatchEvent(new CustomEvent('autocompleteCreate', {
      detail: {value: this.input.value},
      bubbles: true,
    }))
    this.box.setAttribute('hidden', 'true')
    this.input.setAttribute('aria-expanded', 'false')
  }

  get url() {
    return this.getAttribute('url') + '?q=' + this.input.value
  }

  download() {
    this.setAttribute('loading', '')
    this.xhr = new XMLHttpRequest()
    this.xhr.timeout = 5000
    this.xhr.addEventListener('load', this.receive.bind(this))
    this.xhr.addEventListener('error', () => {
      this.removeAttribute('loading')
      this.box && this.box.setAttribute('hidden', 'true')
    })
    this.xhr.addEventListener('timeout', () => {
      this.removeAttribute('loading')
      this.box && this.box.setAttribute('hidden', 'true')
    })
    this.xhr.open('GET', this.url)
    this.xhr.send()
  }

  keyboard(ev) {
    switch(ev.key) {
      // Prevent cursor movement in input on arrow keys.
      case 'ArrowDown':
      case 'ArrowUp':
        ev.preventDefault()
        ev.stopPropagation()
        this.move(ev.key === 'ArrowUp' ? 'up' : 'down')
        break

      case 'Tab':
      case 'Enter':
        if (this.box.getAttribute('hidden')) return

        var choice = this.box.querySelector('.hilight')

        if (!choice) {
          // Don't get in the way, let the browser submit form or focus
          // on next element.
          return
        }

        ev.preventDefault()
        ev.stopPropagation()

        if (choice.getAttribute('data-create')) {
          this.handleCreate()
        } else {
          this.selectChoice(choice)
        }
        break

      case 'Escape':
        this.box.setAttribute('hidden', 'true')
        this.input.setAttribute('aria-expanded', 'false')
        break
    }
  }

  move(way) {
    if (this.input.value.length < this.minimumCharacters) return true

    var current = this.box.querySelector('.hilight')
    var choices = this.navigationChoices

    // First and last choices for wrap-around navigation.
    var first = choices[0]
    var last = choices[choices.length - 1]

    var target

    this.draw()

    if (current) {
      if (way === 'up') {
        var next = choices.indexOf(current) - 1
        target = next < 0 ? last : choices[next]
      } else {
        var next = choices.indexOf(current) + 1
        target = next >= choices.length ? first : choices[next]
      }
    } else {
      target = way === 'up' ? last : first
    }

    target !== undefined && this.hilight(target)
  }

  get choices() {
    return Array.from(this.box.querySelectorAll(this.choiceSelector))
  }

  // Includes [data-create] items for arrow-key navigation; excludes group
  // headers, [data-next-page], and other non-selectable elements.
  get navigationChoices() {
    return Array.from(this.box.querySelectorAll(
      this.choiceSelector + ', [data-create]'
    ))
  }

  get selected() {
    return this.box.querySelectorAll(this.choiceSelector + '.hilight')
  }

  get choiceSelector() {
    return this.getAttribute('choice-selector') || '[data-value]:not([data-create])'
  }

  get minimumCharacters() {
    return this.getAttribute('minimum-characters') || 0
  }

  receive(ev) {
    // ev.target.status is undefined for local (non-XHR) calls; skip check in that case.
    if (ev.target.status && !(ev.target.status >= 200 && ev.target.status < 300)) return
    this.removeAttribute('loading')
    this.draw()
    this.box.innerHTML = ev.target.response
    this.bindBox()

    // Client-side no-results message when server returns an empty fragment
    // and there is no pagination sentinel (which implies more results exist).
    if (this.box.querySelectorAll(this.choiceSelector).length === 0
        && !this.box.querySelector('[data-next-page]')
        && !this.box.querySelector('[data-create]')) {
      const el = document.createElement('div')
      el.className = 'autocomplete-light-no-results'
      el.textContent = this.getAttribute('no-results-text') || 'No results'
      this.box.appendChild(el)
    }
  }

  bindBox() {
    // Regular selectable choices.
    this.box.querySelectorAll(this.choiceSelector).forEach((item) => {
      if (item.getAttribute('data-bound')) return
      item.setAttribute('role', 'option')
      item.setAttribute('aria-selected', 'false')
      item.addEventListener('mouseenter', (ev) => this.hilight(ev.target))
      item.addEventListener('mouseleave', (ev) => {
        ev.target.classList.remove('hilight')
        ev.target.setAttribute('aria-selected', 'false')
      })
      // mousedown fires before blur/focusout, so the box stays visible long
      // enough to register the click before hiding.
      item.addEventListener('mousedown', (ev) => this.selectChoice(ev.target))
      item.setAttribute('data-bound', 'true')
    })

    // Create-option items — dispatches autocompleteCreate event; no built-in POST.
    this.box.querySelectorAll('[data-create]').forEach((item) => {
      if (item.getAttribute('data-bound')) return
      item.addEventListener('mouseenter', () => item.classList.add('hilight'))
      item.addEventListener('mouseleave', () => item.classList.remove('hilight'))
      item.addEventListener('mousedown', () => this.handleCreate())
      item.setAttribute('data-bound', 'true')
    })

    // Pagination sentinel — appends next page into the existing box.
    const nextPageEl = this.box.querySelector('[data-next-page]:not([data-bound])')
    if (nextPageEl) {
      nextPageEl.addEventListener('mousedown', (ev) => {
        // preventDefault keeps focus on the input so the box stays visible
        // while the next page loads.
        ev.preventDefault()
        const page = nextPageEl.getAttribute('data-next-page')
        nextPageEl.remove()
        const xhr = new XMLHttpRequest()
        xhr.timeout = 5000
        xhr.addEventListener('load', (loadEv) => {
          if (!(loadEv.target.status >= 200 && loadEv.target.status < 300)) return
          const tmp = document.createElement('div')
          tmp.innerHTML = loadEv.target.response
          while (tmp.firstChild) this.box.appendChild(tmp.firstChild)
          this.bindBox()
        })
        xhr.open('GET', this.getAttribute('url') + '?q=' + this.input.value + '&page=' + page)
        xhr.send()
      })
      nextPageEl.setAttribute('data-bound', 'true')
    }
  }

  boxBuild() {
    this.box = document.createElement('div')
    this.box.classList.add('autocomplete-light-box')
    this.box.setAttribute('role', 'listbox')
    document.querySelector('body').appendChild(this.box)

    const hideBox = () => {
      this.box.setAttribute('hidden', 'true')
      this.input.setAttribute('aria-expanded', 'false')
    }
    this.input.addEventListener('focusout', hideBox)
    this.input.addEventListener('blur', hideBox)
  }

  draw() {
    if (!this.box) this.boxBuild()
    var rect = this.input.getBoundingClientRect()
    this.box.style.top = rect.bottom + window.scrollY + 'px'
    this.box.style.left = rect.left + 'px'
    // keep some space for the border, avoid overflow on x
    this.box.style.width = rect.width - 2 + 'px'
    this.box.removeAttribute('hidden')
    this.input.setAttribute('aria-expanded', 'true')
  }
}


class AutocompleteSelectInput extends AutocompleteLight {
  get url() {
    if (!this.getAttribute('url')) return
    var url = this.getAttribute('url') + '?q=' + this.input.value
    this.parentNode.querySelectorAll('option[selected]').forEach((option) => {
      url += '&_=' + option.value
    })
    var buildFwd = window.AutocompleteLightBuildForward
    if (buildFwd) {
      var parent = this.closest('autocomplete-select')
      if (parent) {
        var fwd = buildFwd(parent)
        if (fwd) url += '&forward=' + encodeURIComponent(fwd)
      }
    }
    return url
  }

  receive(ev) {
    if (ev.target.status && !(ev.target.status >= 200 && ev.target.status < 300)) return
    const selectedValues = new Set(
      Array.from(this.parentNode.querySelectorAll('option[selected]')).map(o => o.value)
    )
    if (selectedValues.size) {
      const tmp = document.createElement('div')
      tmp.innerHTML = ev.target.response
      tmp.querySelectorAll('[data-value]').forEach(item => {
        if (selectedValues.has(item.getAttribute('data-value'))) item.remove()
      })
      ev = {target: {status: ev.target.status, response: tmp.innerHTML}}
    }
    super.receive(ev)
  }

  download() {
    if (this.url) {
      return super.download()
    }

    // No URL: filter local <option> tags instead of fetching from server.
    this.receive({
      target: {
        response: Array.from(
          this.closest('autocomplete-select').select.options
        ).filter(
          (item) => !item.selected && item.innerText.startsWith(this.input.value)
        ).map(
          (item) => `<div data-value="${item.getAttribute('value')}">${item.innerHTML}</div>`
        ).join('\n'),
      }
    })
  }
}


class AutocompleteSelect extends HTMLElement {
  maxChoices = 0

  connectedCallback(retries = 20) {
    if (!this.select || !this.input.input) {
      // Strip data-bound while waiting for children — it may have been
      // inherited from a cloneNode(true), which would make wait_script()
      // return too early before full init completes in the retry.
      this.removeAttribute('data-bound')
      if (retries > 0) setTimeout(() => this.connectedCallback(retries - 1), 100)
      return
    }

    // Use an instance property (not the attribute) to guard against
    // double-init on legitimate reconnects of already-initialised elements.
    // cloneNode(true) copies attributes but NOT instance properties, so
    // cloned elements always go through the full setup on their first connect.
    if (this._initialized) {
      this.reconcileState()
      return
    }

    const attrMax = parseInt(this.getAttribute('max-choices'))
    this.maxChoices = isNaN(attrMax) ? 0 : attrMax

    if (!this.select.multiple) {
      this.maxChoices = 1
    }

    this.input.addEventListener(
      'autocompleteChoiceSelected',
      (ev) => this.choiceSelect(ev.detail.choice)
    )

    this.reconcileState()
    this._initialized = true
    this.setAttribute('data-bound', 'true')
  }

  reconcileState() {
    // ensure all selected options are in deck
    Array.from(
      this.select.querySelectorAll('option[selected]')
    ).forEach((option) => {
      var exists = this.deck.querySelectorAll(
        '[data-value="' + option.getAttribute('value') + '"]'
      )
      if (exists.length) return
      var cmp = document.createElement('div')
      cmp.setAttribute('selected', 'selected')
      cmp.setAttribute('data-value', option.getAttribute('value'))
      cmp.innerHTML = option['innerHTML']
      this.choiceSelect(cmp, false)
    })

    // ensure all deck values are in select
    Array.from(
      this.deck.querySelectorAll('[data-value]')
    ).forEach((choice) => {
      if (!this.select.querySelector('option[value="' + choice.getAttribute('data-value') + '"]')) {
        this.choiceSelect(choice, false)
      }
      this.addClear(choice)
    })

    this.input.hidden = this.maxChoices && this.selected.length >= this.maxChoices
  }

  get deck() {
    return this.querySelector('[slot=deck]')
  }

  get select() {
    return this.querySelector('[slot=select]')
  }

  get selected() {
    return this.deck.querySelectorAll('[data-value]')
  }

  get input() {
    return this.querySelector('autocomplete-select-input, autocomplete-light')
  }

  onClearClick(ev) {
    this.choiceUnselect(ev.target.parentNode)
    ev.preventDefault()
    ev.stopPropagation()
  }

  choiceUnselect(choice, noShowHide = false) {
    var value = choice.getAttribute('data-value')

    var option = this.select.querySelector('option[value="' + value + '"]')
    if (option) {
      option.removeAttribute('selected')
    }

    var decked = this.deck.querySelector('[data-value="' + value + '"]')
    if (decked) {
      decked.parentNode.removeChild(decked)
    }

    if (!this.selected.length) {
      this.select.value = ''
    }

    if (!noShowHide)
      this.input.hidden = this.maxChoices && this.selected.length >= this.maxChoices

    this.changeTrigger()
  }

  choiceUpdate(value, newLabel) {
    var item = this.deck.querySelector('[data-value="' + value + '"]')
    if (item) {
      var clearSpan = item.querySelector('.clear')
      item.textContent = newLabel
      if (clearSpan) item.appendChild(clearSpan)
    }
    var option = this.select.querySelector('option[value="' + value + '"]')
    if (option) option.textContent = newLabel
  }

  choiceSelect(choice, trigger = true) {
    if (this.maxChoices && this.selected.length >= this.maxChoices) {
      this.choiceUnselect(this.selected[0], true)
    }

    var value = choice.getAttribute('data-value')

    var option = this.select.querySelector('option[value="' + value + '"]')
    if (!option) {
      option = document.createElement('option')
      option.setAttribute('value', value)
      option.innerHTML = choice.innerHTML
      this.select.appendChild(option)
    }
    option.selected = true
    option.setAttribute('selected', 'selected')

    if (!this.select.multiple) {
      this.select.value = value
    }

    if (!this.deck.querySelector('[data-value="' + value + '"]')) {
      choice = choice.cloneNode(true)
      choice.classList.remove('hilight')
      this.addClear(choice)
      this.deck.appendChild(choice)
    }

    this.input.hidden = this.maxChoices && this.selected.length >= this.maxChoices

    trigger && this.changeTrigger()
  }

  changeTrigger() {
    this.select.dispatchEvent(
      new Event('change', {bubbles: true, cancelable: false})
    )
  }

  addClear(choice) {
    if (choice.querySelector('.clear'))
      return
    var clear = document.createElement('span')
    clear.classList.add('clear')
    clear.addEventListener('click', this.onClearClick.bind(this))
    clear.textContent = this.getAttribute('clear-text') || '×'
    choice.appendChild(clear)
  }
}

window.customElements.define('autocomplete-light', AutocompleteLight)
window.customElements.define('autocomplete-select-input', AutocompleteSelectInput)
window.customElements.define('autocomplete-select', AutocompleteSelect)
