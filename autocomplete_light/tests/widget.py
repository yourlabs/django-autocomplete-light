import unittest
import os
import time

from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import ui
from selenium.common.exceptions import NoSuchElementException


"""
Selenium tests (which have waits and all) don't work on travis since the
update, i don't know why, i've spent countless hours trying to debug it, asked
numerous times on #travis, was recommended to contact support which i did
but support didn't reply so here goes ....
"""
@unittest.skipIf(os.environ.get('TRAVIS', False), 'No travis support')
class WidgetTestCase(LiveServerTestCase):
    fixtures = ['test.json', 'initial_data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(WidgetTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(WidgetTestCase, cls).tearDownClass()
        cls.selenium.quit()

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

    def save(self):
        return self.selenium.find_element_by_css_selector(
            'input[name=_save]').click()

    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        self.wait.until(lambda selenium: selenium.find_element_by_name("username"))

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        self.wait.until(lambda selenium: selenium.find_element_by_id("user-tools"))

    def test_login(self):
        self.wait = ui.WebDriverWait(self.selenium,120)

        def wait_for_selector(selector, displayed=None):
            def f(selenium):
                element = selenium.find_element_by_css_selector(selector)
                if displayed is not None:
                    return element.is_displayed() == displayed
                return True
            self.wait.until(f)

        self.login()

        self.default_id = 'id_city_text'

        self.selenium.get('%s%s' % (self.live_server_url, '/admin/fk_autocomplete/address/add'))
        wait_for_selector("[data-widget-ready]")

        self.input_element().send_keys('par')
        wait_for_selector(".yourlabs-autocomplete", True)

        self.assertEqual(20, len(self.autocomplete_choice_elements()))

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
