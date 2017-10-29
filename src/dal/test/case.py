"""Test case for autocomplete implementations."""

import os
import uuid

from django import VERSION
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import transaction
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.utils import six

from splinter import Browser


GLOBAL_BROWSER = None


class AutocompleteTestCase(StaticLiveServerTestCase):
    """Provide a class-persistent selenium instance and assertions."""

    @classmethod
    def setUpClass(cls):
        """Instanciate a browser for the whole test session."""
        global GLOBAL_BROWSER

        if GLOBAL_BROWSER is None:
            GLOBAL_BROWSER = Browser(os.environ.get('BROWSER', 'firefox'))
        cls.browser = GLOBAL_BROWSER

        super(AutocompleteTestCase, cls).setUpClass()

    def get(self, url):
        """Open a URL."""
        self.browser.visit('%s%s' % (
            self.live_server_url,
            url
        ))

        if '/admin/login/' in self.browser.url:
            # Should be pre-filled by HTML template
            # self.browser.fill('username', 'test')
            # self.browser.fill('password', 'test')
            self.browser.find_by_value('Log in').first.click()

        self.wait_script()

    def click(self, selector):
        """Click an element by css selector."""
        self.browser.find_by_css(selector).first.click()

    def enter_text(self, selector, text):
        """Enter text in an element by css selector."""
        self.browser.find_by_css(selector).first.value = ''
        self.browser.find_by_css(selector).first.type(text)

    def assert_not_visible(self, selector):
        """Assert an element is not visible by css selector."""
        e = self.browser.find_by_css(selector)
        assert not e or e.first.visible is False

    def assert_visible(self, selector):
        """Assert an element is visible by css selector."""
        e = self.browser.find_by_css(selector).first
        assert e.visible is True


class AdminMixin(object):
    """Mixin for tests that should happen in ModelAdmin."""

    def get_modeladmin_url(self, action, **kwargs):
        """Return a modeladmin url for a model and action."""
        return reverse('admin:%s_%s_%s' % (
            self.model._meta.app_label,
            self.model._meta.model_name,
            action
        ), kwargs=kwargs)

    def fill_name(self):
        """Fill in the name input."""
        i = self.id()
        half = int(len(i))
        not_id = i[half:] + i[:half]
        self.browser.fill('name', not_id)


class OptionMixin(object):
    """Mixin to make a unique option per test."""

    @transaction.atomic
    def create_option(self):
        """Create a unique option from self.model into self.option."""
        unique_name = six.text_type(uuid.uuid1())

        if VERSION < (1, 10):
            # Support for the name to be changed through a popup in the admin.
            unique_name = unique_name.replace('-', '')

        option, created = self.model.objects.get_or_create(
            name=unique_name)
        return option


class ContentTypeOptionMixin(OptionMixin):
    """Same as option mixin, with content type."""

    def create_option(self):
        """Return option, content type."""
        option = super(ContentTypeOptionMixin, self).create_option()
        ctype = ContentType.objects.get_for_model(option)
        return option, ctype
