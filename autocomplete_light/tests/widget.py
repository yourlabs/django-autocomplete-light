from __future__ import unicode_literals

import os

from django import VERSION
from django.test import LiveServerTestCase

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support import ui


if VERSION[0] == 1 and VERSION[1] < 7:
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
        if not self._StoppableWSGIServer__is_shut_down.wait(30):
            raise RuntimeError(
                "Failed to shutdown the live test server in 2 seconds. The "
                "server might be stuck or generating a slow response.")
    StoppableWSGIServer.shutdown = patient_shutdown

    from django.test import LiveServerTestCase
else:
    # LiveServerTestCase doesn't serve static files in 1.7 anymore
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase as LiveServerTestCase


if os.environ.get('TRAVIS', False):
    WAIT_TIME = 30
elif os.environ.get('BUILD_ID', False):  #  Jenkins build server
    WAIT_TIME = 30
else:
    WAIT_TIME = 5


class WidgetTestCase(LiveServerTestCase):
    autocomplete_name = 'relation'
    fixtures = ['basic_fk_model_test_case.json', 'test_user.json']
    test_case_setup_done = False

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(WAIT_TIME)
        super(WidgetTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(WidgetTestCase, cls).tearDownClass()
        cls.selenium.quit()
        cls.test_case_setup_done = False

    def setUp(self):
        if self.__class__.test_case_setup_done is False:
            self.set_implicit_wait()
            self.setup_test_case()
        self.__class__.test_case_setup_done = True

    def open_url(self, url):
        self.selenium.get('%s%s' % (self.live_server_url, url))

    def send_keys(self, keys, autocomplete_name=None):
        autocomplete_name = autocomplete_name or self.autocomplete_name

        for key in keys:
            self.selenium.find_element_by_css_selector(
                'input[name=%s-autocomplete]' % autocomplete_name
                ).send_keys(key)

    def submit(self, name=None):
        selector = 'input[type=submit]'

        if name:
            selector += '[name=%s]' % name

        self.selenium.find_element_by_css_selector(selector).click()

    def login(self):
        self.open_url('/admin/')
        self.selenium.find_element_by_css_selector('input[name=username]').send_keys('test')
        self.selenium.find_element_by_css_selector('input[name=password]').send_keys('test')
        self.submit()

        # wait for page load
        self.selenium.find_elements_by_css_selector('#navigation-autocomplete')

    def deck_choice_elements(self, autocomplete_name=None):
        autocomplete_name = autocomplete_name or self.autocomplete_name

        return self.selenium.find_elements_by_css_selector(
            '#id_%s-deck [data-value]' % autocomplete_name)

    def autocomplete(self, autocomplete_name=None):
        autocomplete_name = autocomplete_name or self.autocomplete_name

        xpath = ''.join([
            '//*[@id="id_%s-autocomplete"]/' % autocomplete_name,
            'following-sibling::',
            'span[contains(',
                'concat(" ", normalize-space(@class), " "), ',
                '" yourlabs-autocomplete ")',
            ']'])
        return self.selenium.find_element_by_xpath(xpath)

    def deck_choices(self, autocomplete_name=None):
        autocomplete_name = autocomplete_name or self.autocomplete_name

        xpath = ''.join([
            '//*[@id="id_%s-autocomplete"]/' % autocomplete_name,
            'preceding-sibling::',
            'span[contains(',
                'concat(" ", normalize-space(@class), " "), ',
                '" deck ")',
            ']/*[@data-value]'])

        return self.selenium.find_elements_by_xpath(xpath)

    def hilighted_choice(self, autocomplete_name=None):
        autocomplete_name = autocomplete_name or self.autocomplete_name

        xpath = ''.join([
            '//*[@id="id_%s-autocomplete"]/' % autocomplete_name,
            'following-sibling::',
            'span[contains(',
                'concat(" ", normalize-space(@class), " "), ',
                '" yourlabs-autocomplete ")',
            ']',
            '/*[contains(',
                'concat(" ", normalize-space(@class), " "), ',
                '" hilight ")',
            ']'])

        return self.selenium.find_element_by_xpath(xpath)

    def autocomplete_choices(self, autocomplete_name=None):
        autocomplete_name = autocomplete_name or self.autocomplete_name

        xpath = ''.join([
            '//*[@id="id_%s-autocomplete"]/' % autocomplete_name,
            'following-sibling::',
            'span[contains(',
                'concat(" ", normalize-space(@class), " "), ',
                '" yourlabs-autocomplete ")',
            ']/*[@data-value]'])

        return self.selenium.find_elements_by_xpath(xpath)

    def input(self, autocomplete_name=None):
        autocomplete_name = autocomplete_name or self.autocomplete_name

        return self.selenium.find_element_by_css_selector(
                'input[name=%s-autocomplete]' % autocomplete_name)

    def select(self, autocomplete_name=None):
        autocomplete_name = autocomplete_name or self.autocomplete_name

        xpath = ''.join([
            '//*[@id="id_%s-autocomplete"]/' % autocomplete_name,
            'following-sibling::',
            'select'])

        return self.selenium.find_element_by_xpath(xpath)

    def set_implicit_wait(self):
        self.selenium.implicitly_wait(WAIT_TIME)
        self.selenium.set_page_load_timeout(WAIT_TIME)

    def unset_implicit_wait(self):
        self.selenium.implicitly_wait(0)
        self.selenium.set_page_load_timeout(0)

    def select_values(self):
        self.select  # wait for select

        # don't wait for options as there might be none
        self.unset_implicit_wait()

        ret = [o.get_attribute('value') for o in Select(self.select()).options if
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

    def assertAutocompleteEmpty(self):
        self.unset_implicit_wait()
        self.assertTrue(len(self.autocomplete_choices()) == 0)
        self.set_implicit_wait()


class ActivateAutocompleteInBlankFormTestCase(WidgetTestCase):
    def setup_test_case(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/add/')
        self.send_keys('ja')

    def test_autocomplete_shows_up(self):
        self.assertTrue(self.autocomplete().is_displayed())

    def test_autocomplete_has_four_choices(self):
        self.assertEqual(4, len(self.autocomplete_choices()))

class XhrPendingTestCase(WidgetTestCase):
    def setup_test_case(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/add/')

    def test_xhr_pending(self):
        self.send_keys('ja')
        self.selenium.find_element_by_css_selector(
            'input[name=%s-autocomplete]' % self.autocomplete_name)
        self.selenium.find_element_by_css_selector(
            'input:not(.xhr-pending)[name=%s-autocomplete]' % self.autocomplete_name)


class SelectChoiceInEmptyFormTestCase(WidgetTestCase):
    def setup_test_case(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/add/')
        self.send_keys('ja')
        self.autocomplete_choices()[1].click()

    def test_autocomplete_disappears(self):
        self.assertFalse(self.autocomplete().is_displayed())

    def test_input_disappears(self):
        self.assertFalse(self.input().is_displayed())

    def test_deck_choice_shows_up(self):
        self.assertEqual(len(self.deck_choices()), 1)

    def test_deck_choice_same_as_selected(self):
        self.assertSameChoice(self.autocomplete_choices()[1], self.deck_choices()[0])

    def test_hidden_select_value(self):
        self.assertEqual(self.select_values(), ['4'])


class WidgetInitialStatusInEditForm(WidgetTestCase):
    def setup_test_case(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/1/')

    def test_hidden_select_values(self):
        self.assertEqual(self.select_values(), ['4'])

    def test_input_is_hidden(self):
        self.assertFalse(self.input().is_displayed())


class RemoveChoiceInEditFormTestCase(WidgetTestCase):
    def setup_test_case(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/1/')
        self.deck_choices()[0].find_element_by_css_selector('.remove').click()

    def test_input_shows_up(self):
        self.assertTrue(self.input().is_displayed())

    def test_hidden_select_option_was_unselected(self):
        self.unset_implicit_wait()
        self.assertEqual(self.select_values(), [])
        self.set_implicit_wait()

    def test_element_was_remove_from_deck(self):
        self.unset_implicit_wait()
        self.assertEqual(0, len(self.deck_choices()))
        self.set_implicit_wait()


class KeyboardTestCase(WidgetTestCase):
    def setup_test_case(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/add/')
        self.send_keys('jac')

    def assertHilightedChoiceNmber(self, n):
        self.assertSameChoice(self.hilighted_choice(), self.autocomplete_choices()[n])

    def send_keys_wait_assert_choice_number(self, key, choice):
        old_hilight = self.hilighted_choice()

        self.send_keys([key])
        ui.WebDriverWait(self.selenium, WAIT_TIME).until(
            lambda x: old_hilight != self.hilighted_choice())

        self.assertSameChoice(self.hilighted_choice(), self.autocomplete_choices()[choice])

    def test_00_first_to_second_with_down(self):
        self.send_keys_wait_assert_choice_number(Keys.ARROW_DOWN, 1)

    def test_01_last_to_first_with_down(self):
        self.send_keys_wait_assert_choice_number(Keys.ARROW_DOWN, 0)

    def test_02_first_to_last_with_up(self):
        self.send_keys_wait_assert_choice_number(Keys.ARROW_UP, -1)

    def test_03_last_to_first_with_up(self):
        self.send_keys_wait_assert_choice_number(Keys.ARROW_UP, 0)

    def test_04_tab_to_select_choice(self):
        self.send_keys([Keys.TAB])
        self.assertSameChoice(self.autocomplete_choices()[0], self.deck_choices()[0])
        self.assertEqual(self.select_values(), ['4'])


class InlineBlankTestCase(ActivateAutocompleteInBlankFormTestCase):
    autocomplete_name = 'reverse_for_inline-3-relation'

    def setup_test_case(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/add/')
        self.selenium.find_element_by_css_selector('.add-row a').click()
        self.send_keys('ja')


class InlineSelectChoiceTestCase(SelectChoiceInEmptyFormTestCase):
    autocomplete_name = 'reverse_for_inline-3-relation'

    def setup_test_case(self):
        self.login()
        self.open_url('/admin/basic/fkmodel/add/')
        self.selenium.find_element_by_css_selector('.add-row a').click()
        self.send_keys('ja')
        self.autocomplete_choices()[1].click()
