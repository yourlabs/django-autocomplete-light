"""Helpers for DAL user story based tests."""

import time


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
                return self.browser.evaluate_script('$.select2')
            except:
                time.sleep(.15)
            tries -= 1
        raise Exception('$.select2 was not defined after 15 seconds.')

    def clean_label(self, label):
        """Remove the "remove" character used in select2."""
        return label.replace('\xd7', '')
