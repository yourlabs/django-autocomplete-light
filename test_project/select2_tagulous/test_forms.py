from django import test

from select2_taggit.test_forms import TagSelect2TestMixin

from .forms import TestForm
from .models import TestModel

Tag = TestModel.test.tag_model


class TagulousFormTest(TagSelect2TestMixin, test.TestCase):
    form = TestForm
    model = TestModel
    tag = TestModel.test.tag_model
    url_name = 'select2_tagulous'
