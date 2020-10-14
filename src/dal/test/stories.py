"""User stories, functional tests for AutocompleteTestCase."""
from __future__ import unicode_literals

import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
)

import six

import tenacity


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
        self.dropdown_selector = (dropdown_selector
                                  or self.case.dropdown_selector)
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

    @tenacity.retry(stop=tenacity.stop_after_delay(3))
    def find_option(self, text):
        """Incremental sleep until option appeared."""
        options = self.case.browser.find_by_css(self.option_selector)

        for option in options:
            if text in option.text:
                return option

        raise Exception('Option %s not found' % text)

    def get_field_label_selector(self):
        """Return CSS selector for field option label."""
        return '%s %s' % (self.field_container_selector, self.label_selector)

    def clean_label_from_remove_buton(self):
        """Clean child nodes before checking (ie. clear option)."""
        self.case.browser.execute_script(
            '''
            document.querySelectorAll("%s *").forEach(function(node) {
                node.parentNode.removeChild(node);
            });
            ''' % self.get_field_label_selector()
        )

    def get_label(self):
        """Return autocomplete widget label."""
        label = self.case.browser.find_by_css(
            self.get_field_label_selector()
        )

        self.clean_label_from_remove_buton()
        return self.clean_label(six.text_type(label.text))

    def clean_label(self, label):
        """Given an option text, return the actual label."""
        return label

    @tenacity.retry(stop=tenacity.stop_after_delay(3))
    def assert_label(self, text):
        """Assert that the autocomplete label matches text."""
        assert six.text_type(text) == six.text_type(self.get_label())

    def get_value(self):
        """Return the autocomplete field value."""
        field = self.case.browser.find_by_css(
            self.field_selector)

        return field['value']

    @tenacity.retry(stop=tenacity.stop_after_delay(3))
    def assert_value(self, value):
        """Assart that the actual field value matches value."""
        assert self.get_value() == six.text_type(value)

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

    @tenacity.retry(stop=tenacity.stop_after_delay(3))
    def assert_suggestion_labels_are(self, expected):
        """Retrying assert that suggestions match expected labels."""
        assert sorted(expected) == sorted(self.get_suggestions_labels())

    def switch_to_popup(self):
        """Wait for and switch to popup window."""
        tries = 10
        while tries:
            if len(self.case.browser.windows) == 2:
                break
            time.sleep(0.1)
            tries -= 1

        self.case.browser.windows.current = self.case.browser.windows[1]
        self.in_popup = True

    def switch_to_main(self):
        """Switch back to main window."""
        self.case.browser.windows.current = self.case.browser.windows[0]
        self.in_popup = False

    def submit(self):
        """Submit the form."""
        sel = 'input[type=submit]'

        if not self.in_popup:
            sel += '[name=_continue]'

        el = self.case.browser.find_by_css(sel).first
        el.click()

        # Wait until the form was actually submited
        tries = 100
        while tries:
            # Popup is gone
            if len(self.case.browser.windows) == 1 and self.in_popup:
                break

            # Page changed
            try:
                el.visible
            except:
                break

            tries -= 1
            time.sleep(.05)

        if not self.in_popup:
            self.case.wait_script()

    def toggle_autocomplete(self):
        """Open the autocomplete dropdown."""
        self.case.click('%s %s' % (
            self.field_container_selector,
            self.widget_selector,
        ))

    def refresh_autocomplete(self):
        """Re-open the autocomplete box."""
        self.toggle_autocomplete()
        self.case.browser.is_element_not_present_by_css(self.option_selector)
        self.toggle_autocomplete()

    def get_suggestions(self):
        """Return the list of suggestions in the autocomplete box."""
        def get_options():
            return self.case.browser.find_by_css(self.option_selector)

        def is_searching(options):
            try:
                return 'Searching' in options[0].text
            except StaleElementReferenceException:
                return True
            except IndexError:
                return True

        options = get_options()
        while is_searching(options) is True:
            time.sleep(0.1)
            options = get_options()
        return [(o['value'], o.text) for o in options]

    def get_suggestions_labels(self):
        """Return labels for suggestions in the autocomplete box."""
        return [o[1] for o in self.get_suggestions()]


class SelectOption(BaseStory):
    """User selects an option."""

    def select_option(self, text):
        """Assert that selecting option "text" sets input's value."""
        dropdown = self.case.browser.find_by_css(self.dropdown_selector)
        if not len(dropdown) or not dropdown.visible:
            self.toggle_autocomplete()

        self.case.assert_visible(self.dropdown_selector)
        self.case.enter_text(self.input_selector, text)
        self.find_option(text).click()

    def clear_option(self):
        """Clear current option."""
        self.case.click(self.field_clear_selector)


class InlineSelectOption(SelectOption):
    """Same as UserCanSelectOption, in a given inline."""

    def __init__(self, case, inline_number, inline_related_name=None,
                 **kwargs):
        """
        Do the same as UserCanSelectOption, in inline inline_number.

        Where inline_related_name should be the related_name option for the
        foreign key used for the InlineModelAdmin.
        """
        self.inline_number = inline_number
        self.inline_related_name = (inline_related_name
                                    or case.inline_related_name)

        super(InlineSelectOption, self).__init__(case, **kwargs)

        self.field_container_selector = '#%s-%s .field-%s' % (
            self.inline_related_name, self.inline_number, self.field_name)
        self.field_selector = '#id_%s-%s-%s' % (
            self.inline_related_name,
            self.inline_number,
            self.field_name
        )

        # Ensure the inline is displayed else click to add it
        add = self.case.browser.find_link_by_partial_text('Add another').first

        num = len(
            self.case.browser.find_by_css(
                '.dynamic-%s' % self.inline_related_name
            )
        )
        while num < self.inline_number + 1:
            add.click()

            # Did it work or wasn't the js loaded yet ?
            try:
                self.case.browser.find_by_css(
                    self.field_selector.replace(
                        str(self.inline_number),
                        str(num),
                    )
                ).first  # as usual, rely on implicit wait
            except:
                continue

            num += 1


class RenameOption(SelectOption):
    """User story to rename an option in django admin."""

    def rename_option(self, current_name, add_keys):
        """Click the change button and rename in the popup."""
        self.case.click('#change_id_%s' % self.field_name)

        self.switch_to_popup()
        name_input = self.case.browser.find_by_id('id_name')
        self.case.assertEquals(
            name_input['value'],
            current_name
        )

        self.case.enter_text('#id_name', add_keys)
        self.submit()

        self.switch_to_main()


class AddAnotherOption(BaseStory):
    """Add-another user story."""

    def add_another(self, name):
        """Click the add button and add another option in the popup."""
        self.case.browser.find_by_id('add_id_%s' % self.field_name).click()

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

        self.case.browser.is_element_present_by_text(name)
        self.case.click(self.option_selector)
        self.case.browser.is_element_not_present_by_css(
            '.select2-results__options'
        )


class MultipleMixin(object):
    """Enable multiple choice support with stories."""

    def get_field_labels_selector(self):
        """Return CSS selector for field option label."""
        return '%s %s' % (self.field_container_selector, self.labels_selector)

    def clean_label_from_remove_buton(self):
        """Clean child nodes before checking (ie. clear option)."""
        self.case.browser.execute_script(
            '''
            document.querySelectorAll("%s span").forEach(function(node) {
                node.parentNode.removeChild(node);
            });
            ''' % self.get_field_labels_selector()
        )

    def get_labels(self):
        """Return autocomplete widget label."""
        self.clean_label_from_remove_buton()

        labels = self.case.browser.find_by_css(
            self.get_field_labels_selector()
        )

        return [
            self.clean_label(six.text_type(label.text))
            for label in labels
        ]

    def get_values(self):
        """Return the autocomplete field value."""
        script = """
        window.GET_VALUES = [];
        document.querySelectorAll("%s option:checked").forEach(function(opt) {
            GET_VALUES.push(opt.value);
        });
        """ % self.field_selector
        self.case.browser.execute_script(script)
        return self.case.browser.evaluate_script('window.GET_VALUES')

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
        """Do the same as above, but also submits the form and check again."""
        self.assert_selection(values, labels)
        self.submit()
        self.assert_labels(labels)
        self.assert_values(values)


class CreateOptionMultiple(MultipleMixin, CreateOption):
    """Multiple version of CreateOptions."""


class SelectOptionMultiple(MultipleMixin, SelectOption):
    """Multiple version of CreateOptions."""


class InlineSelectOptionMultiple(MultipleMixin, InlineSelectOption):
    """Multiple options for InlineSelectOption."""

    def __init__(self, case, inline_number, inline_related_name=None,
                 **kwargs):
        """Set input_selector with field_container_selector."""
        super(InlineSelectOptionMultiple, self).__init__(
            case,
            inline_number,
            inline_related_name=inline_related_name,
            **kwargs
        )

        self.input_selector = '%s %s' % (
            self.field_container_selector,
            self.input_selector,
        )
