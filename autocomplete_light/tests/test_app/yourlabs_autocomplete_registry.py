try:
    import genericm2m
except ImportError:
    genericm2m = None

import autocomplete_light

from .models import *

autocomplete_light.register(OtoModel)
autocomplete_light.register(FkModel)
autocomplete_light.register(MtmModel)
autocomplete_light.register(GfkModel)

if genericm2m:
    autocomplete_light.register(GmtmModel)


class AutocompleteGeneric(autocomplete_light.AutocompleteGenericBase):
    choices = (
        OtoModel.objects.all(),
        FkModel.objects.all(),
        MtmModel.objects.all(),
        GfkModel.objects.all(),
    )

    if genericm2m:
        choices += (GmtmModel.objects.all(),)

    # Should we default on that ? seems kind of dangerous ...
    search_fields = ('name',)*5
