import autocomplete_light
from autocomplete_light import AutocompleteTaggitChoiceList

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
    choices=[m.objects.all() for m in models]
    search_fields=[['name']] * len(models)


autocomplete_light.register(A)


try:
    from taggit.models import Tag
    from .models import OtherTag
except ImportError:
    pass
else:
    autocomplete_light.register(Tag)
    autocomplete_light.register(OtherTag, AutocompleteTaggitChoiceList)
