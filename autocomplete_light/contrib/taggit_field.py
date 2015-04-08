"""
Support for django-taggit tags system. It is used automatically by
autocomplete_light.ModelForm but you can use it independently.

Note that you still need to register an autocomplete for the Tag model.

.. Warning::
    In this case, the tags field is a relation. Thus form.save() **must** be
    called with commit=True.

"""
import six

from ..fields import FieldBase
from ..widgets import TextWidget

try:
    from taggit.forms import TagField as TaggitTagField
    from taggit.utils import edit_string_for_tags
except ImportError:
    class TaggitTagField(object):
        pass
    edit_string_for_tags = None


class TaggitWidget(TextWidget):
    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, six.string_types):
            value = edit_string_for_tags(
                [o.tag for o in value.select_related("tag")])
        return super(TaggitWidget, self).render(name, value, attrs)


class TaggitField(FieldBase, TaggitTagField):
    widget = TaggitWidget

    def validate(self, value):
        return TaggitTagField.validate(self, value)
