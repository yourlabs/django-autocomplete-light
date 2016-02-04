"""Test case for autocomplete implementations."""

import uuid

from django import VERSION
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils import six

from sbo_selenium import SeleniumTestCase

from selenium.common.exceptions import NoSuchElementException


class AutocompleteTestCase(SeleniumTestCase):
    """Provide a class-persistent selenium instance and assertions."""


class AdminMixin(object):
    """Mixin for tests that should happen in ModelAdmin."""

    def get(self, url):
        """Get a URL, logs in if necessary."""
        super(AdminMixin, self).get(url)

        try:
            self.sel.find_element_by_css_selector('input[value="Log in"]')
        except NoSuchElementException:
            return

        username = self.sel.find_element_by_name('username')
        if username.get_attribute('value') != 'test':
            username.send_keys('test')

        password = self.sel.find_element_by_name('username')
        if password.get_attribute('value') != 'test':
            password.send_keys('test')

        self.sel.find_element_by_css_selector('input[value="Log in"]').click()

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
        self.enter_text('[name=name]', not_id)


class OptionMixin(object):
    """Mixin to make a unique option per test."""

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
