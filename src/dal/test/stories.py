"""User stories, functional tests for AutocompleteTestCase."""

import time

from django.utils import six

from selenium.common.exceptions import (
    StaleElementReferenceException,
)


class BaseStory(object):
    """Base UserStory class."""

    def __init__(self,
                 case,
                 clear_selector=None,
                 dropdown_selector=None,
                 field_name=None,
                 input_selector=None,
                 label_selector=None,
                 labels_selector=None,
                 model=None,
                 option_selector=None,
                 widget_selector=None):
        """If any kwarg is None, get it from case attributes."""
        self.case = case
        self.clear_selector = clear_selector or self.case.clear_selector
        self.dropdown_selector = (dropdown_selector or
                                  self.case.dropdown_selector)
        self.field_name = field_name or self.case.field_name
        self.input_selector = input_selector or self.case.input_selector
        self.label_selector = label_selector or self.case.label_selector
        self.labels_selector = labels_selector or self.case.labels_selector
        self.model = model or self.case.model
        self.option_selector = option_selector or self.case.option_selector
        self.widget_selector = widget_selector or self.case.widget_selector

        self.field_container_selector = ('fieldset.aligned .field-%s' %
                                         self.field_name)
        self.field_selector = '#id_%s' % self.field_name
        self.field_clear_selector = '%s %s' % (
            self.field_container_selector,
            self.clear_selector
        )
        self.in_popup = False

    def find_option(self, text):
        """Incremental sleep until option appeared."""
        tries = 0
        options = self.case.sel.find_elements_by_css_selector(
            self.option_selector)

        while True:
            for option in options:
                try:
                    if text in option.text:
                        return option
                except StaleElementReferenceException:
                    break

            if tries > 20:
                raise Exception('Option did not appear')

            time.sleep(tries)
            tries += 1
            options = self.case.sel.find_elements_by_css_selector(
                self.option_selector)

    def get_field_label_selector(self):
        """Return CSS selector for field option label."""
        return '%s %s' % (self.field_container_selector, self.label_selector)

    def clean_label_from_remove_buton(self):
        """Clean child nodes before checking (ie. clear option)."""
        self.case.sel.execute_script(
            '$("%s *").remove()' % self.get_field_label_selector()
        )

    def get_label(self):
        """Return autocomplete widget label."""
        label = self.case.sel.find_element_by_css_selector(
            self.get_field_label_selector()
        )

        self.clean_label_from_remove_buton()
        return six.text_type(label.text)

    def assert_label(self, text):
        """Assert that the autocomplete label matches text."""
        self.case.assertEquals(
            six.text_type(text),
            six.text_type(self.get_label()),
        )

    def get_value(self):
        """Return the autocomplete field value."""
        field = self.case.sel.find_element_by_css_selector(
            self.field_selector)

        return field.get_attribute('value')

    def assert_value(self, value):
        """Assart that the actual field value matches value."""
        self.case.assertEquals(
            self.get_value(),
            six.text_type(value)
        )

    def assert_selection(self, value, label):
        """Assert value is selected and has the given label."""
        self.assert_label(label)
        self.assert_value(value)

    def assert_selection_persists(self, value, label):
        """Assert value and lebel, submit the form and assert again."""
        self.assert_selection(value, label)
        self.submit()
        self.assert_label(label)
        self.assert_value(value)

    def switch_to_popup(self):
        """Switch to popup window."""
        self.case.sel.switch_to_window(
            self.case.sel.window_handles[-1])
        self.in_popup = True

    def switch_to_main(self):
        """Switch back to main window."""
        self.case.sel.switch_to_window(
            self.case.sel.window_handles[0])
        self.in_popup = False

    def submit(self):
        """Submit the form."""
        sel = 'input[type=submit]'

        if not self.in_popup:
            sel += '[name=_continue]'

        self.case.click(sel)

    def toggle_autocomplete(self):
        """Open the autocomplete dropdown."""
        self.case.click('%s %s' % (
            self.field_container_selector,
            self.widget_selector,
        ))

    def refresh_autocomplete(self):
        """Re-open the autocomplete box."""
        self.toggle_autocomplete()
        self.case.wait_until_not_visible(self.option_selector)
        self.toggle_autocomplete()

    def get_suggestions(self):
        """Return the list of suggestions in the autocomplete box."""
        def _options():
            return self.case.sel.find_elements_by_css_selector(
                self.option_selector)

        options = _options()
        while len(options) and 'Searching' in options[0].text:
            time.sleep(0.3)
            options = _options()
        return [(o.get_attribute('value'), o.text) for o in options]

    def get_suggestions_labels(self):
        """Return labels for suggestions in the autocomplete box."""
        return [o[1] for o in self.get_suggestions()]


class SelectOption(BaseStory):
    """User selects an option."""

    def select_option(self, text):
        """Assert that selecting option "text" sets input's value."""
        self.toggle_autocomplete()

        self.case.assert_visible(self.dropdown_selector)
        self.case.enter_text(self.input_selector, text)
        self.find_option(text).click()
        self.case.assert_not_visible(self.dropdown_selector)

    def clear_option(self):
        """Clear current option."""
        self.case.click(self.field_clear_selector)


class InlineSelectOption(SelectOption):
    """Same as UserCanSelectOption, in a given inline."""

    def __init__(self, case, inline_number, inline_related_name=None,
                 **kwargs):
        """
        Same as UserCanSelectOption, in inline inline_number.

        Where inline_related_name should be the related_name option for the
        foreign key used for the InlineModelAdmin.
        """
        self.inline_number = inline_number
        self.inline_related_name = (inline_related_name or
                                    case.inline_related_name)

        super(InlineSelectOption, self).__init__(case, **kwargs)

        self.field_container_selector = '#%s-%s' % (
            self.inline_related_name, self.inline_number)
        self.field_selector = '#id_%s-%s-%s' % (
            self.inline_related_name,
            self.inline_number,
            self.field_name
        )

    def select_option(self, text):
        """Ensure the inline is displayed before calling parent method."""
        num = len(self.case.sel.find_elements_by_css_selector(
            '.dynamic-%s' % self.inline_related_name))

        add = self.case.sel.find_element_by_partial_link_text('Add another')
        while num < self.inline_number + 1:
            add.click()
            num += 1

        super(InlineSelectOption, self).select_option(text)


class RenameOption(SelectOption):
    """User story to rename an option in django admin."""

    def rename_option(self, current_name, add_keys):
        """Click the change button and rename in the popup."""
        self.case.click('#change_id_%s' % self.field_name)

        self.switch_to_popup()
        name_input = self.case.sel.find_element_by_id('id_name')
        self.case.assertEquals(
            name_input.get_attribute('value'),
            current_name
        )

        self.case.enter_text('#id_name', add_keys)
        self.submit()

        self.switch_to_main()


class AddAnotherOption(BaseStory):
    """Add-another user story."""

    def add_another(self, name):
        """Click the add button and add another option in the popup."""
        self.case.click('#add_id_%s' % self.field_name)

        self.switch_to_popup()
        self.case.enter_text('#id_name', name)
        self.submit()
        self.switch_to_main()


class CreateOption(SelectOption):
    """Create an option on the fly."""

    def create_option(self, name):
        """
        Select the only option after typing name and submit.

        name should be unique.
        """
        self.toggle_autocomplete()
        self.case.enter_text(self.input_selector, name)

        self.case.wait_until_element_contains(
            self.option_selector,
            name
        )
        self.case.click(self.option_selector)


class MultipleMixin(object):
    """Enable multiple choice support with stories."""

    def get_field_labels_selector(self):
        """Return CSS selector for field option label."""
        return '%s %s' % (self.field_container_selector, self.labels_selector)

    def clean_label_from_remove_buton(self):
        """Clean child nodes before checking (ie. clear option)."""
        self.case.sel.execute_script(
            '$("%s span").remove()' % self.get_field_labels_selector()
        )

    def get_labels(self):
        """Return autocomplete widget label."""
        self.clean_label_from_remove_buton()

        labels = self.case.sel.find_elements_by_css_selector(
            self.get_field_labels_selector()
        )

        return [six.text_type(label.text) for label in labels]

    def get_values(self):
        """Return the autocomplete field value."""
        script = """
        val = [];
        $('%s option:selected').each(function() {
            val.push($(this).attr('value'));
        });
        return val
        """ % self.field_selector
        return self.case.sel.execute_script(script)

    def assert_labels(self, texts):
        """Assert that all labels match texts."""
        labels = self.get_labels()

        for text in texts:
            self.case.assertIn(text, labels)

        self.case.assertEquals(len(texts), len(labels))

    def assert_values(self, values):
        """Assart that the actual field values matches values."""
        text_values = [six.text_type(v) for v in values]
        actual_values = self.get_values()

        for actual_value in actual_values:
            self.case.assertIn(
                actual_value,
                text_values
            )

        self.case.assertEquals(len(values), len(actual_values))

    def assert_selection(self, values, labels):
        """Assert selections have values and labels."""
        self.assert_labels(labels)
        self.assert_values(values)

    def assert_selection_persists(self, values, labels):
        """Same as above, but also submits the form and check again."""
        self.assert_selection(values, labels)
        self.submit()
        self.assert_labels(labels)
        self.assert_values(values)


class CreateOptionMultiple(MultipleMixin, CreateOption):
    """Multiple version of CreateOptions."""


class SelectOptionMultiple(MultipleMixin, SelectOption):
    """Multiple version of CreateOptions."""
