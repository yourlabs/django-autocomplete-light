"""Test helpers for dal_alight — mirrors dal_select2.test without select2."""

import time


class AlightStory:
    """CSS selectors and wait logic for the autocomplete-light web component.

    Drop-in replacement for ``Select2Story``.  Mix into
    ``AutocompleteTestCase`` subclasses instead of ``Select2Story``.

    HTML structure produced by ``AlightWidgetMixin``::

        <autocomplete-select>
          <select slot="select" id="id_{field}">…</select>
          <div slot="deck">
            <div data-value="1">Label<span class="clear">×</span></div>
          </div>
          <autocomplete-select-input slot="input" url="…">
            <input name="{field}-input" slot="input" class="vTextField" />
          </autocomplete-select-input>
        </autocomplete-select>

    The dropdown box is appended to ``<body>`` by the component::

        <div class="autocomplete-light-box">
          <div data-value="1">Label</div>
          <div data-create data-value="foo">Create "foo"</div>
        </div>
    """

    # The text input lives inside the widget, not in a global dropdown.
    # This lets InlineSelectOption scope enter_text to the field container.
    input_in_field_container = True

    # Text input embedded inside the web component.
    input_selector = 'autocomplete-select-input input'
    # Floating dropdown box appended to body.
    dropdown_selector = '.autocomplete-light-box'
    # Selectable result items (excludes create / group headers).
    option_selector = '.autocomplete-light-box [data-value]:not([data-create])'
    # Create-on-the-fly entry only (has data-create attribute).
    create_option_selector = '.autocomplete-light-box [data-create]'
    # Currently selected value label in the deck (single-select).
    label_selector = 'autocomplete-select [slot=deck] [data-value]'
    # Deck items (multiple-select).
    labels_selector = 'autocomplete-select [slot=deck] [data-value]'
    # Clear (×) button inside a deck item.
    clear_selector = '.clear'
    # Clicking this opens the dropdown (same as input_selector for alight).
    widget_selector = 'autocomplete-select-input input'
    # The outer web component element.
    container_selector = 'autocomplete-select'

    def get_create_option_selector(self, name):
        """Return a selector for the create option that matches ``name`` exactly.

        Using ``[data-value="name"]`` prevents clicking a stale create option
        left over from a previous query before the new XHR has returned.
        """
        escaped = name.replace('"', '\\"')
        return f'.autocomplete-light-box [data-create][data-value="{escaped}"]'

    def wait_script(self):
        """Wait until the autocomplete-select custom element is registered and all
        autocomplete-select-input instances have completed connectedCallback."""
        tries = 100
        while tries:
            try:
                result = self.browser.evaluate_script(
                    "customElements.get('autocomplete-select') !== undefined"
                    " && !document.querySelector('autocomplete-select-input:not([data-bound])') "
                )
                if result:
                    return result
            except Exception:
                pass
            time.sleep(0.15)
            tries -= 1
        raise Exception(
            'autocomplete-select custom element was not defined after 15 seconds.'
        )

    def toggle_autocomplete_widget(self, selector):
        """Open the autocomplete, ensuring focus fires even if already focused.

        For alight, ``focus`` on the text input is what triggers the XHR.
        When the input already has focus (e.g. after a previous call in
        ``refresh_autocomplete``), a plain Selenium click does not re-fire
        ``focus``.  Blurring first resets the focus state so the subsequent
        click fires a real ``focus`` event and starts a fresh XHR.
        """
        self.browser.execute_script(
            """
            var el = document.querySelector(arguments[0]);
            if (el && document.activeElement === el) { el.blur(); }
            """,
            selector,
        )
        self.click(selector)

    def clean_label(self, label):
        """Remove the × clear button text from a label string."""
        return label.replace('×', '').strip()
