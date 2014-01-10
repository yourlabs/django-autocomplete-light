try:
    import genericm2m
except ImportError:
    genericm2m = None

try:
    import taggit
except ImportError:
    taggit = None

import autocomplete_light

from .models import *


class FkModelForm(autocomplete_light.ModelForm):
    class Meta:
        model = FkModel


class OtoModelForm(autocomplete_light.ModelForm):
    class Meta:
        model = OtoModel


class MtmModelForm(autocomplete_light.ModelForm):
    class Meta:
        model = MtmModel


class GfkModelForm(autocomplete_light.ModelForm):
    class Meta:
        model = GfkModel


if genericm2m:
    class GmtmModelForm(autocomplete_light.ModelForm):
        class Meta:
            model = GmtmModel


if taggit:
    class TaggitModelForm(autocomplete_light.ModelForm):
        class Meta:
            model = TaggitModel
