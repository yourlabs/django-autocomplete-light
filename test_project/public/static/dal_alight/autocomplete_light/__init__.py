"""
Browser test helpers for autocomplete-light.
"""

import time

try:
    from selenium.webdriver.common.by import By

    def retry(cb, *args, expected=None, **kwargs):
        for _ in range(15):
            try:
                result = cb(*args, **kwargs)
            except Exception:
                pass
            else:
                if expected is not None and result == expected:
                    return result
                elif expected is None and result:
                    return result
            time.sleep(0.1)
        return cb(*args, **kwargs)

    class AutocompleteLight:
        def __init__(self, browser, autocomplete_light_id):
            self.id = autocomplete_light_id
            self.browser = browser

        def component(self):
            return self.browser.find_by_id(self.id)

        def attr(self, name):
            return self.browser.evaluate_script(
                f'document.getElementById("{self.id}").' + name
            )

        def input(self):
            return self.attr('input')

        def box(self):
            return self.attr('box')

        def hilight(self):
            return self.browser.evaluate_script(
                f'document.getElementById("{self.id}").box.querySelector("[data-value].hilight")'
            )

        def choices(self):
            return self.browser.evaluate_script(
                f'document.getElementById("{self.id}").box.querySelectorAll("[data-value]")'
            )

        def focus(self):
            return self.input().click()

        def defocus(self):
            return self.browser.find_by_css('body').click()

        def type(self, val):
            return self.browser.find_by_css(f'#{self.id} input')[0].type(val)

    class AutocompleteSelect(AutocompleteLight):
        def alight(self):
            return self.attr('input')

        def input(self):
            return self.attr('input.input')

        def box(self):
            return self.attr('input.box')

        def selected(self):
            return self.browser.evaluate_script(
                f'document.getElementById("{self.id}").deck.querySelectorAll("[data-value]")'
            )

        def selectedOptions(self):
            return self.attr('select.selectedOptions')

        def select(self):
            return self.attr('select')

        def value(self):
            return self.select().get_property('value')

        def choices(self):
            return self.browser.evaluate_script(
                f'document.getElementById("{self.id}").input.box.querySelectorAll("[data-value]")'
            )

        def unselect(self, index):
            self.selected()[index].find_element(By.TAG_NAME, 'span').click()

        def assert_selected(self, label, value):
            selected = retry(self.selected)
            assert len(selected) == 1
            assert selected[0].get_attribute('data-value') == str(value)
            assert self.value() == str(value)
            assert selected[0].text.split('\n')[0] == label
            assert self.input().get_property('hidden')

    class AutocompleteSelectMultiple(AutocompleteSelect):
        def assert_selected(self, *label_values):
            selected = retry(self.selected)
            assert len(selected) == len(label_values)
            assert len(self.selectedOptions()) == len(label_values)
            for label_value, choice in zip(label_values, selected):
                label, value = label_value
                assert choice.get_attribute('data-value') == str(value)
                assert choice.text.split('\n')[0] == label
            assert not self.alight().get_property('hidden')

    def get_input(browser, id):
        return retry(browser.evaluate_script)(
            f'document.getElementById("{id}").input',
        )

except ImportError:
    pass
