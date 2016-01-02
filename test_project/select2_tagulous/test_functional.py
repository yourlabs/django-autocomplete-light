from dal.test import case

from select2_taggit.test_functional import TagSelect2AdminTestMixin

from .models import TestModel


class TagulousSelect2AdminTest(TagSelect2AdminTestMixin,
                               case.AutocompleteTestCase):
    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TestModel
    tag_model = TestModel.test.tag_model
