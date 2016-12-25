from dal.test import case

from dal_select2.test import Select2Story

from select2_generic_m2m.test_functional import AdminGenericM2MBase

from .models import TModel


class AdminGM2MTestCase(AdminGenericM2MBase,
                        Select2Story,
                        case.AdminMixin,
                        case.ContentTypeOptionMixin,
                        case.AutocompleteTestCase):
    model = TModel
