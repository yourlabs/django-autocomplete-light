from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class WidgetTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(WidgetTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(WidgetTestCase, cls).tearDownClass()
        cls.selenium.quit()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/fk_autocomplete/address/add'))
        import ipdb; ipdb.set_trace()
