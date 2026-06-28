"""Test helpers for dal_alight — mirrors dal_select2.test without select2."""

import time

from dal.test import stories


class AlightStory:
    """CSS selectors and wait logic for the autocomplete-light web component.

    Drop-in replacement for ``Select2Story``.  Mix into
    ``AutocompleteTestCase`` subclasses instead of ``Select2Story``.

    HTML structure produced by ``AlightWidgetMixin``::

        <autocomplete-select>
          <input type="hidden" name="{field}" value="1" slot="values" data-label="Label">
          <span slot="deck">
            <div data-value="1">Label<span class="clear">×</span></div>
          </span>
          <autocomplete-select-input slot="input" url="…">
            <input id="id_{field}" name="{field}-input" slot="input" class="vTextField" />
          </autocomplete-select-input>
        </autocomplete-select>

    The dropdown box is appended to ``<body>`` by the component::

        <div class="autocomplete-light-box">
          <div data-value="1">Label</div>
          <div data-create data-value="foo">Create "foo"</div>
        </div>
    """

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
        """Wait until all alight web components have finished connectedCallback.

        autocomplete-select.connectedCallback fires before its child
        autocomplete-select-input's callback (parent-first connection order),
        so it schedules a 100 ms retry.  We must wait for BOTH elements to
        have data-bound before interacting: autocomplete-select installs the
        autocompleteChoiceSelected listener only on its own retry, and
        clicking an option before that listener exists silently does nothing.
        """
        tries = 100
        while tries:
            try:
                result = self.browser.evaluate_script(
                    "customElements.get('autocomplete-select') !== undefined"
                    " && !document.querySelector("
                    "'autocomplete-select-input:not([data-bound]),"
                    " autocomplete-select:not([data-bound])') "
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


class AlightSelectOption(stories.SelectOption):
    """Single-select user story for the alight backend."""

    def _values_selector(self):
        """Hidden inputs live in the component; Django's id is on the search input."""
        return 'autocomplete-select:has(%s) [slot=values]' % self.field_selector

    def get_value(self):
        fields = self.case.browser.find_by_css(self._values_selector())
        if not fields:
            return ''
        return fields.first['value']


class AlightMultipleMixin(stories.MultipleMixin):
    """Multiple-select assertions using alight hidden value inputs."""

    def get_values(self):
        script = """
        window.GET_VALUES = [];
        document.querySelectorAll("%s").forEach(function(inp) {
            GET_VALUES.push(inp.value);
        });
        """ % self._values_selector()
        self.case.browser.execute_script(script)
        return self.case.browser.evaluate_script('window.GET_VALUES')


class AlightSelectOptionMultiple(AlightMultipleMixin, AlightSelectOption):
    """Multiple-select user story for the alight backend."""


class AlightInlineSelectOption(
    stories.InlineSelectOptionMixin,
    AlightSelectOption,
):
    """Single-select user story for alight inlines."""

    def _scope_inline_input_selector(self):
        self.input_selector = '%s %s' % (
            self.field_container_selector,
            self.input_selector,
        )


class AlightInlineSelectOptionMultiple(
    AlightMultipleMixin,
    AlightInlineSelectOption,
):
    """Multiple-select user story for alight inlines."""


class AlightCreateOption(AlightSelectOption, stories.CreateOption):
    """Create an option on the fly — alight backend only."""

    def create_option(self, name):
        create_sel = self.case.get_create_option_selector(name)
        self._open_and_type(name)
        self.case.browser.is_element_present_by_css(create_sel)
        value_selector = self._values_selector()
        initial_count = self.case.browser.evaluate_script(
            'document.querySelectorAll("%s").length' % value_selector
        )
        self.case.js_click(create_sel)
        deadline = time.time() + 5
        while time.time() < deadline:
            count = self.case.browser.evaluate_script(
                'document.querySelectorAll("%s").length' % value_selector
            )
            if count > initial_count:
                break
            time.sleep(0.1)


class AlightCreateOptionMultiple(AlightMultipleMixin, AlightCreateOption):
    """Multiple-select variant of :class:`AlightCreateOption`."""
