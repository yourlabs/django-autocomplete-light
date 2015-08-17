import autocomplete_light.shortcuts as autocomplete_light

from .models import *

models = [OtoModel, FkModel, MtmModel, GfkModel]

try:
    import genericm2m
except ImportError:
    pass
else:
    models.append(GmtmModel)

for model in models:
    autocomplete_light.register(model)


class A(autocomplete_light.AutocompleteGenericBase):
    choices = [m.objects.all() for m in models]
    search_fields = [['name']] * len(models)

class A2(autocomplete_light.AutocompleteGenericBase):
    choices = [m.objects.all() for m in models]
    search_fields = [['name']] * len(models)
    values = ['1','2', '3' ]
    attrs = {'data-class-defined': 1}

    def __init__(self, *args, **kw):
        self.attrs = self.attrs.copy()
        self.attrs.update({'data-init-defined': 2})

autocomplete_light.register(A)
autocomplete_light.register(A2)


# The autocomplete for class B is used to set up the test case for
# autocomplete_light.tests.widgets.TextWidgetTestCase.test_widget_attrs_copy.
# This bug is triggered only when the autocomplete is registered with a
# widget_attrs dictionary.
class B(autocomplete_light.AutocompleteGenericBase):
    choices = [m.objects.all() for m in models]
    search_fields = [['name']] * len(models)

class B2(autocomplete_light.AutocompleteGenericBase):
    choices = [m.objects.all() for m in models]
    search_fields = [['name']] * len(models)
    attrs = {'data-class-defined': 1}

    def __init__(self, *args, **kw):
        self.attrs = self.attrs.copy()
        self.attrs.update({'data-init-defined': 2})


autocomplete_light.register(B, widget_attrs={'data-widget-maximum-values': 4})
autocomplete_light.register(B2, )


try:
    from taggit.models import Tag
except ImportError:
    pass
else:
    autocomplete_light.register(Tag)
