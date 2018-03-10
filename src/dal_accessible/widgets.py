"""Accessible autocomplete implementation module."""
from dal.widgets import (
    QuerySetSelectMixin,
    Select,
    SelectMultiple,
    WidgetMixin
)
from django import forms
from django.conf import settings
from django.contrib.staticfiles import finders
from django.utils import six
from django.utils import translation


class AccessibleWidgetMixin(object):
    pass


class ModelAccessible(QuerySetSelectMixin,
                      AccessibleWidgetMixin,
                      forms.Select):
    autocomplete_function = 'accessible'
