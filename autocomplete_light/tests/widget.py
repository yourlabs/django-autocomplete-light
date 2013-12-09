from __future__ import unicode_literals

import unittest
import os
import time

import six

from django.test import LiveServerTestCase

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import ui
from selenium.common.exceptions import NoSuchElementException


class WidgetTestCase(LiveServerTestCase):
    fixtures = ['basic_fk_model_test_case.json', 'initial_data.json']

    def setUp(self):
        if os.environ.get('TRAVIS', False):
            self.wait = ui.WebDriverWait(self.selenium, 300)
        else:
            self.wait = ui.WebDriverWait(self.selenium, 5)

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        #cls.selenium.implicitly_wait(300 if os.environ.get('TRAVIS', False) else 5)
        super(WidgetTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(WidgetTestCase, cls).tearDownClass()
        cls.selenium.quit()

    def open_url(self, url, wait_until=None, displayed=None):
        self.selenium.get('%s%s' % (self.live_server_url, url))
        self.wait_until(wait_until, displayed)

    def wait_until(self, wait_until, displayed=None):
        if hasattr(wait_until, '__call__'):
            self.wait.until(wait_until)
        elif isinstance(wait_until, six.string_types):
            self.wait_for_selector(wait_until, displayed)

    def wait_for_selector(self, selector, displayed=None):
        def f(selenium):
            element = selenium.find_element_by_css_selector(selector)
            if displayed is not None:
                return element.is_displayed() == displayed
            return True
        self.wait.until(f)

    def wait_for_selector_change(self, selector):
        self.wait_for_selector(selector)
        initial = self.selenium.find_element_by_css_selector(selector)

        def f(selenium):
            try:
                return selenium.find_element_by_css_selector(selector) != initial
            except NoSuchElementException:
                return False

        self.wait.until(f)

    def send_keys(self, keys, selector=None):
        if selector is None and self.autocomplete_name:
            selector = 'input[name=%s-autocomplete]' % self.autocomplete_name

        for key in keys:
            self.selenium.find_element_by_css_selector(selector).send_keys(key)

    def save(self):
        return self.selenium.find_element_by_css_selector(
            'input[name=_save]').click()

    def submit(self, wait_for_selector):
        try:
            e = self.selenium.find_element_by_css_selector('input[type=submit][name=_continue]')
        except NoSuchElementException:
            e = self.selenium.find_element_by_css_selector('input[type=submit]')
        e.click()
        self.wait_for_selector(wait_for_selector)

    def login(self):
        self.open_url('/admin/', 'input[name=username]')
        self.send_keys('test', 'input[name=username]')
        self.send_keys('test', 'input[name=password]')
        self.submit('#footer')

    def deck_choice_elements(self):
        return self.selenium.find_elements_by_css_selector(
            '#id_%s-deck [data-value]' % self.autocomplete_name)

    @property
    def widget(self):
        return self.selenium.find_element_by_css_selector(
                '.autocomplete-light-widget.%s' % self.autocomplete_name)

    @property
    def autocomplete(self):
        return self.selenium.find_element_by_css_selector(
                '.autocomplete-light-widget.%s .yourlabs-autocomplete' % self.autocomplete_name)

    @property
    def deck_choices(self):
        return self.selenium.find_elements_by_css_selector(
                '.autocomplete-light-widget.%s .deck [data-value]' %
                self.autocomplete_name)

    @property
    def autocomplete_choices(self):
        return self.selenium.find_elements_by_css_selector(
                '.autocomplete-light-widget.%s .yourlabs-autocomplete [data-value]' %
                self.autocomplete_name)

    @property
    def hilighted_choice(self):
        return self.selenium.find_element_by_css_selector(
                 '.autocomplete-light-widget.%s .yourlabs-autocomplete .hilight' %
                 self.autocomplete_name)

    @property
    def input(self):
        return self.selenium.find_element_by_css_selector(
                '.autocomplete-light-widget.%s input' %
                self.autocomplete_name)

    @property
    def select(self):
        return Select(self.selenium.find_element_by_css_selector(
                '.autocomplete-light-widget.%s select' %
                self.autocomplete_name))

    @property
    def select_values(self):
        return [o.get_attribute('value') for o in self.select.options if o.is_selected()]

    def assertSameChoice(self, autocomplete_choice, deck_choice):
        if autocomplete_choice.get_attribute('data-value') != deck_choice.get_attribute('data-value'):
            self.fail('Choices have different data-value')

        if autocomplete_choice.text not in deck_choice.text:
            # deck_choice has an additional span.remove
            self.fail('Choices have different text')

    def test_fk_model_add_relation(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/add/', '[data-widget-ready]')

        self.autocomplete_name = 'relation'
        self.send_keys('Selenium', 'input[name=name]')
        self.send_keys('ja')
        self.wait_for_selector('.yourlabs-autocomplete', True)

        self.assertTrue(self.autocomplete.is_displayed())
        self.assertEqual(4, len(self.autocomplete_choices))
        self.autocomplete_choices[1].click()
        self.assertFalse(self.autocomplete.is_displayed())
        self.assertFalse(self.input.is_displayed())
        self.assertEqual(len(self.deck_choices), 1)
        self.assertSameChoice(self.autocomplete_choices[1], self.deck_choices[0])
        self.assertEqual(self.select_values, ['4'])

        self.submit('[data-widget-ready]')

        self.assertEqual(self.select_values, ['4'])
        self.assertFalse(self.input.is_displayed())
        self.deck_choices[0].find_element_by_css_selector('.remove').click()
        self.assertTrue(self.input.is_displayed())
        self.assertEqual(self.select_values, [])

        def keyboard_test(keys, n):
            self.send_keys(keys)
            self.wait_for_selector_change('.autocomplete-light-widget.%s .yourlabs-autocomplete .hilight'
                    % self.autocomplete_name)
            self.assertSameChoice(self.hilighted_choice, self.autocomplete_choices[n])
        keyboard_test('jac', 0)
        keyboard_test([Keys.ARROW_DOWN], 1)
        keyboard_test([Keys.ARROW_DOWN], 0)
        keyboard_test([Keys.ARROW_UP], 1)
        keyboard_test([Keys.ARROW_UP], 0)
        keyboard_test([Keys.ARROW_UP], 1)

        self.send_keys([Keys.ENTER])
        self.wait_for_selector('.autocomplete-light-widget.%s .deck [data-value]' % self.autocomplete_name)
        self.assertSameChoice(self.autocomplete_choices[1], self.deck_choices[0])
        self.assertEqual(self.select_values, ['4'])

        return
        # select paris
        self.autocomplete_choice_elements()[1].click()

        wait_for_selector(".yourlabs-autocomplete", False)
        wait_for_selector("#%s" % self.default_id, False)

        selected = self.widget_choice_elements()
        self.assertEqual(1, len(selected))
        self.assertTrue('Paris' in selected[0].text)
        self.assertTrue('France' in selected[0].text)

        self.save()
        wait_for_selector('#changelist')
        element = self.selenium.find_element_by_css_selector(
            '#changelist tr.row1 a').click()

        wait_for_selector("[data-widget-ready]")

        # remove
        selected = self.widget_choice_elements()
        selected[0].find_element_by_css_selector('.remove').click()

        self.assertFalse(self.autocomplete_visible())
        self.assertTrue(self.input_visible())

        self.input_element().send_keys('par')
        wait_for_selector('.yourlabs-autocomplete', True)

        self.keyboard_test()

        self.assertEqual('',
            self.input_element().get_attribute('value'))

    def keyboard_test(self):
        tests = (
            {
                'key': Keys.ARROW_DOWN,
                'expected': 1,
            },
            {
                'key': Keys.ARROW_DOWN,
                'expected': 2,
            },
            {
                'key': Keys.ARROW_UP,
                'expected': 1,
            },
            {
                'key': Keys.ARROW_UP,
                'expected': 0,
            },
            {
                'key': Keys.ARROW_UP,
                'expected': -1,
            },
            {
                'key': Keys.ARROW_UP,
                'expected': -2,
            },
        )

        for test in tests:
            self.input_element().send_keys(test['key'])

            self.assertEqual(
                self.autocomplete_choice_elements()[test['expected']].id,
                self.autocomplete_hilighted_choice_element().id
            )

        self.input_element().send_keys(Keys.TAB)
        self.assertEqual(
            self.autocomplete_choice_elements()[test['expected']].get_attribute('data-value'),
            self.widget_select_element().get_attribute('value'),
        )

    def autocomplete_visible(self):
        try:
            return self.autocomplete_element().is_displayed()
        except NoSuchElementException:
            return False

    def autocomplete_element(self):
        return self.selenium.find_element_by_css_selector(
            '.yourlabs-autocomplete')

    def autocomplete_hilighted_choice_element(self):
        return self.selenium.find_element_by_css_selector(
            '.yourlabs-autocomplete [data-value].hilight')

    def autocomplete_choice_elements(self):
        return self.selenium.find_elements_by_css_selector(
            '.yourlabs-autocomplete [data-value]')

    def input_element(self, id=None):
        if id is None: id = self.default_id
        return self.selenium.find_element_by_css_selector('#' + id)

    def input_visible(self, id=None):
        if id is None: id = self.default_id
        return self.input_element(id=None).is_displayed()

    def widget_choice_elements(self, id=None):
        if id is None: id = self.default_id
        return self.selenium.find_elements_by_css_selector(
            '#%s .deck [data-value]' % id.replace('_text', '-wrapper'))

    def widget_select_element(self, id=None):
        return self.widget_element(id).find_element_by_tag_name('select')

    def widget_element(self, id=None):
        if id is None: id = self.default_id
        return self.selenium.find_element_by_css_selector(
            '#%s' % id.replace('_text', '-wrapper'))
