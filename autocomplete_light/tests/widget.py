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


# Patch for travis
from django.test.testcases import StoppableWSGIServer


def patient_shutdown(self):
    """
    Stops the serve_forever loop.

    Blocks until the loop has finished. This must be called while
    serve_forever() is running in another thread, or it will
    deadlock.
    """
    self._StoppableWSGIServer__serving = False
    if not self._StoppableWSGIServer__is_shut_down.wait(30 if os.environ.get('TRAVIS', False) else 2):
        raise RuntimeError(
            "Failed to shutdown the live test server in 2 seconds. The "
            "server might be stuck or generating a slow response.")
StoppableWSGIServer.shutdown = patient_shutdown


class WidgetTestCase(LiveServerTestCase):
    fixtures = ['basic_fk_model_test_case.json', 'initial_data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(300 if os.environ.get('TRAVIS', False) else 5)
        super(WidgetTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(WidgetTestCase, cls).tearDownClass()
        cls.selenium.quit()

    def open_url(self, url):
        self.selenium.get('%s%s' % (self.live_server_url, url))

    def send_keys(self, keys, selector=None):
        if selector is None and self.autocomplete_name:
            selector = 'input[name=%s-autocomplete]' % self.autocomplete_name

        for key in keys:
            self.selenium.find_element_by_css_selector(selector).send_keys(key)

    def save(self):
        return self.selenium.find_element_by_css_selector(
            'input[name=_save]').click()

    def submit(self, name=None):
        selector = 'input[type=submit]'

        if name:
            selector += '[name=%s]' % name

        self.selenium.find_element_by_css_selector(selector).click()

    def login(self):
        self.open_url('/admin/')
        self.send_keys('test', 'input[name=username]')
        self.send_keys('test', 'input[name=password]')
        self.submit()

    def deck_choice_elements(self):
        return self.selenium.find_elements_by_css_selector(
            '#id_%s-deck [data-value]' % self.autocomplete_name)

    @property
    def widget(self):
        return self.selenium.find_element_by_css_selector(
                '.autocomplete-light-widget.%s' % self.autocomplete_name)

    @property
    def autocomplete(self):
        xpath = ''.join([
            '//*[@id="id_%s-autocomplete"]/' % self.autocomplete_name,
            'following-sibling::',
            'span[contains(',
                'concat(" ", normalize-space(@class), " "), ',
                '" yourlabs-autocomplete ")',
            ']'])
        return self.selenium.find_element_by_xpath(xpath)

    @property
    def deck_choices(self):
        xpath = ''.join([
            '//*[@id="id_%s-autocomplete"]/' % self.autocomplete_name,
            'preceding-sibling::',
            'span[contains(',
                'concat(" ", normalize-space(@class), " "), ',
                '" deck ")',
            ']/*[@data-value]'])

        return self.selenium.find_elements_by_xpath(xpath)

    @property
    def autocomplete_choices(self):
        xpath = ''.join([
            '//*[@id="id_%s-autocomplete"]/' % self.autocomplete_name,
            'following-sibling::',
            'span[contains(',
                'concat(" ", normalize-space(@class), " "), ',
                '" yourlabs-autocomplete ")',
            ']/*[@data-value]'])

        return self.selenium.find_elements_by_xpath(xpath)

    @property
    def hilighted_choice(self):
        return self.selenium.find_element_by_css_selector(
                 '.autocomplete-light-widget.%s .yourlabs-autocomplete .hilight' %
                 self.autocomplete_name)

    @property
    def input(self):
        return self.selenium.find_element_by_css_selector(
                'input[name=%s-autocomplete]' % self.autocomplete_name)

    @property
    def select(self):
        xpath = ''.join([
            '//*[@id="id_%s-autocomplete"]/' % self.autocomplete_name,
            'following-sibling::',
            'select'])

        return self.selenium.find_element_by_xpath(xpath)

    def set_implicit_wait(self):
        self.selenium.implicitly_wait(300 if os.environ.get('TRAVIS', False) else 5)

    def unset_implicit_wait(self):
        self.selenium.implicitly_wait(0)

    @property
    def select_values(self):
        self.select  # wait for select

        # don't wait for options as there might be none
        self.unset_implicit_wait()

        ret = [o.get_attribute('value') for o in Select(self.select).options if
                o.is_selected()]

        # restore implicit wait
        self.set_implicit_wait()

        return ret

    def assertSameChoice(self, autocomplete_choice, deck_choice):
        if autocomplete_choice.get_attribute('data-value') != deck_choice.get_attribute('data-value'):
            self.fail('Choices have different data-value')

        if autocomplete_choice.text not in deck_choice.text:
            # deck_choice has an additional span.remove
            self.fail('Choices have different text')

    def test_fk_model_add_relation(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/add/')
        self.autocomplete_name = 'relation'

        self.send_keys('Selenium', 'input[name=name]')
        self.send_keys('ja')

        self.assertTrue(self.autocomplete.is_displayed())
        self.assertEqual(4, len(self.autocomplete_choices))
        self.autocomplete_choices[1].click()
        self.assertFalse(self.autocomplete.is_displayed())
        self.assertFalse(self.input.is_displayed())
        self.assertEqual(len(self.deck_choices), 1)
        self.assertSameChoice(self.autocomplete_choices[1], self.deck_choices[0])
        self.assertEqual(self.select_values, ['4'])

        self.submit('_continue')

        self.assertEqual(self.select_values, ['4'])
        self.assertFalse(self.input.is_displayed())
        self.deck_choices[0].find_element_by_css_selector('.remove').click()
        self.assertTrue(self.input.is_displayed())
        self.assertEqual(self.select_values, [])

    def test_keyboard(self):
        self.login()
        self.autocomplete_name = 'relation'
        self.open_url('/admin/basic/fkmodel/add/')

        def keyboard_test(keys, n):
            self.send_keys(keys)
            self.assertSameChoice(self.hilighted_choice, self.autocomplete_choices[n])
        keyboard_test('jac', 0)
        keyboard_test([Keys.ARROW_DOWN], 1)
        keyboard_test([Keys.ARROW_DOWN], 0)
        keyboard_test([Keys.ARROW_UP], 1)
        keyboard_test([Keys.ARROW_UP], 0)
        keyboard_test([Keys.ARROW_UP], 1)

        self.send_keys([Keys.TAB])
        self.assertSameChoice(self.autocomplete_choices[1], self.deck_choices[0])
        self.assertEqual(self.select_values, ['6'])

    def test_inline(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/add/')
        self.autocomplete_name = 'fkmodel_set-3-noise'

        self.unset_implicit_wait()
        try:
            self.autocomplete
        except NoSuchElementException:
            pass
        else:
            self.fail('The inline was already created')
        self.set_implicit_wait()

        self.selenium.find_element_by_css_selector('.add-row a').click()
        self.send_keys('ja')
        self.assertTrue(self.autocomplete.is_displayed())
        self.autocomplete_choices[1].click()
        self.assertFalse(self.autocomplete.is_displayed())
        self.assertFalse(self.input.is_displayed())
        self.assertEqual(len(self.deck_choices), 1)
        self.assertSameChoice(self.autocomplete_choices[1], self.deck_choices[0])
        self.assertEqual(self.select_values, ['4'])
