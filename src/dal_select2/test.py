"""Helpers for DAL user story based tests."""

import time

from dal.test import stories


class Select2Story(object):
    """Define Select2 CSS selectors."""

    clear_selector = '.select2-selection__clear'
    container_selector = '.select2-container'
    dropdown_selector = '.select2-dropdown'
    input_selector = '.select2-search__field'
    label_selector = '.select2-selection__rendered'
    labels_selector = \
        '.select2-selection__rendered .select2-selection__choice'
    option_selector = '.select2-results__option[aria-selected]'
    widget_selector = '.select2-selection'

    def wait_script(self):
        """Wait for scripts to be loaded and ready to work."""
        tries = 100
        while tries:
            try:
                return self.browser.evaluate_script('yl.registerFunction')
            except Exception:
                time.sleep(.15)
            tries -= 1
        raise Exception('$.select2 was not defined after 15 seconds.')

    def clean_label(self, label):
        """Remove the "remove" character used in select2."""
        return label.replace('\xd7', '')


class Select2SelectOption(stories.SelectOption):
    """Single-select user story for the select2 backend."""

    def get_value(self):
        field = self.case.browser.find_by_css(self.field_selector)
        return field['value']


class Select2MultipleMixin(stories.MultipleMixin):
    """Multiple-select assertions for select2 ``<select>`` widgets."""

    def get_values(self):
        script = """
        window.GET_VALUES = [];
        document.querySelectorAll("%s option:checked").forEach(function(opt) {
            GET_VALUES.push(opt.value);
        });
        """ % self.field_selector
        self.case.browser.execute_script(script)
        return self.case.browser.evaluate_script('window.GET_VALUES')


class Select2SelectOptionMultiple(Select2MultipleMixin, Select2SelectOption):
    """Multiple-select user story for the select2 backend."""


class Select2InlineSelectOption(
    stories.InlineSelectOptionMixin,
    Select2SelectOption,
):
    """Single-select user story for select2 inlines."""

    def _scope_inline_input_selector(self):
        pass


class Select2InlineSelectOptionMultiple(
    Select2MultipleMixin,
    Select2InlineSelectOption,
):
    """Multiple-select user story for select2 inlines."""

    def __init__(self, case, inline_number, inline_related_name=None,
                 **kwargs):
        super().__init__(
            case,
            inline_number,
            inline_related_name=inline_related_name,
            **kwargs
        )
        self.input_selector = '%s %s' % (
            self.field_container_selector,
            self.input_selector,
        )


class Select2CreateOption(Select2SelectOption, stories.CreateOption):
    """Create an option on the fly — select2 backend only."""

    def create_option(self, name):
        self._open_and_type(name)
        self.case.browser.is_element_present_by_text(name)
        self.case.click(self.option_selector)
        self.case.browser.is_element_not_present_by_css(
            '.select2-results__options'
        )


class Select2CreateOptionMultiple(Select2MultipleMixin, Select2CreateOption):
    """Multiple-select create-on-the-fly for the select2 backend."""


class Select2RenameOption(Select2SelectOption, stories.RenameOption):
    """Rename related object via admin popup — select2 backend."""


class Select2AddAnotherOption(Select2SelectOption, stories.AddAnotherOption):
    """Add related object via admin popup — select2 backend."""
