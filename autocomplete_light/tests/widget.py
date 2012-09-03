import time

from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver

class WidgetTestCase(LiveServerTestCase):
    fixtures = ['cities_light.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(WidgetTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(WidgetTestCase, cls).tearDownClass()
        cls.selenium.quit()

    def autocomplete_visible(self, id=None):
        if id is None: id = self.default_id
        return self.autocomplete_element(id=None).is_displayed()

    def autocomplete_element(self, id=None):
        if id is None: id = self.default_id
        return self.selenium.find_element_by_css_selector(
            '.yourlabs-autocomplete.outer-container.id-%s' % id)

    def autocomplete_hilighted_choice_element(self, id=None):
        if id is None: id = self.default_id
        return self.selenium.find_element_by_css_selector(
            '.yourlabs-autocomplete.inner-container.id-%s [data-value].hilight' % id)


    def autocomplete_choice_elements(self, id=None):
        if id is None: id = self.default_id
        return self.selenium.find_elements_by_css_selector(
            '.yourlabs-autocomplete.inner-container.id-%s [data-value]' % id)

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
            'input[name=_continue]').click()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/fk_autocomplete/address/add'))

        self.default_id = 'id_city_text'
        time.sleep(1)

        self.input_element().send_keys('par')
        time.sleep(1)

        self.assertTrue(self.autocomplete_visible())
        self.assertEqual(20, len(self.autocomplete_choice_elements()))


        # select paris
        self.autocomplete_choice_elements()[1].click()

        time.sleep(1)
        self.assertFalse(self.autocomplete_visible())
        self.assertFalse(self.input_visible())

        selected = self.widget_choice_elements()
        self.assertEqual(1, len(selected))
        self.assertTrue('Paris' in selected[0].text)
        self.assertTrue('France' in selected[0].text)


        self.save()
        time.sleep(1)


        self.assertFalse(self.autocomplete_visible())
        self.assertFalse(self.input_visible())

        # remove
        selected = self.widget_choice_elements()
        selected[0].find_element_by_css_selector('.remove').click()

        self.assertFalse(self.autocomplete_visible())
        self.assertTrue(self.input_visible())

        self.input_element().send_keys('par')
        time.sleep(1)

        self.keyboard_test()

        self.assertEqual('',
            self.input_element().get_attribute('value'))

    def keyboard_test(self):
        tests = (
            {
                'key': Keys.ARROW_DOWN,
                'expected': 0,
            },
            {
                'key': Keys.ARROW_DOWN,
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
