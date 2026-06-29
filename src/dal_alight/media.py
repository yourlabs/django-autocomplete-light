"""Media helpers for dal_alight module scripts.

Django 5.2+ ships :class:`django.forms.widgets.Script` for ``type="module"``
script tags.  Older Django versions lack that class but
:meth:`django.forms.Media.render_js` still honours objects with ``__html__``
since 5.1.  We backport ``Script`` here so widget media always renders ES
module scripts on every supported Django version without a second classic
``<script>`` execution (which would re-run ``customElements.define``).
"""

from django import forms
from django.forms.utils import flatatt
from django.templatetags.static import static
from django.utils.html import format_html, html_safe


@html_safe
class MediaAsset:
    """Backport of ``django.forms.widgets.MediaAsset`` (Django 5.2+)."""

    element_template = '{path}'

    def __init__(self, path, **attributes):
        self._path = path
        self.attributes = attributes

    def __eq__(self, other):
        return (
            (self.__class__ is other.__class__ and self.path == other.path)
            or (isinstance(other, str) and self._path == other)
        )

    def __hash__(self):
        return hash(self._path)

    def __str__(self):
        return format_html(
            self.element_template,
            path=self.path,
            attributes=flatatt(self.attributes),
        )

    def __repr__(self):
        return f'{type(self).__qualname__}({self._path!r})'

    @property
    def path(self):
        if self._path.startswith(('http://', 'https://', '/')):
            return self._path
        return static(self._path)


class Script(MediaAsset):
    """Backport of ``django.forms.widgets.Script`` (Django 5.2+)."""

    element_template = '<script src="{path}"{attributes}></script>'

    def __init__(self, src, **attributes):
        super().__init__(src, **attributes)


def get_script_class():
    """Return Django's Script when available, else our backport."""
    try:
        from django.forms.widgets import Script as DjangoScript
    except ImportError:
        return Script
    return DjangoScript


def alight_media():
    """Widget media: CSS + ES module JS for autocomplete-light."""
    script = get_script_class()
    return forms.Media(
        css=dict(all=['dal_alight/autocomplete-light.css']),
        js=[
            script('dal_alight/autocomplete-light.js', type='module'),
            script('dal_alight/dal-django.js', type='module'),
        ],
    )
