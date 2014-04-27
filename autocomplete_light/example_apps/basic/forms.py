from django import VERSION

try:
    import genericm2m
except ImportError:
    genericm2m = None

try:
    import taggit
except ImportError:
    taggit = None

import autocomplete_light

autocomplete_light.autodiscover()

from .models import *


class DjangoCompatMeta:
    if VERSION >= (1, 6):
        fields = '__all__'


class FkModelForm(autocomplete_light.ModelForm):
    class Meta(DjangoCompatMeta):
        model = FkModel


class OtoModelForm(autocomplete_light.ModelForm):
    class Meta(DjangoCompatMeta):
        model = OtoModel


class MtmModelForm(autocomplete_light.ModelForm):
    class Meta(DjangoCompatMeta):
        model = MtmModel


class GfkModelForm(autocomplete_light.ModelForm):
    class Meta(DjangoCompatMeta):
        model = GfkModel


if genericm2m:
    class GmtmModelForm(autocomplete_light.ModelForm):
        class Meta(DjangoCompatMeta):
            model = GmtmModel


if taggit:
    class TaggitModelForm(autocomplete_light.ModelForm):
        class Meta(DjangoCompatMeta):
            model = TaggitModel
