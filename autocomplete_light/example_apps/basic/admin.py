from django.contrib import admin

from .forms import *
from .models import *

try:
    import genericm2m
except ImportError:
    genericm2m = None

try:
    import taggit
except ImportError:
    taggit = None



models = [FkModel, OtoModel, MtmModel, GfkModel]

if genericm2m:
    models.append(GmtmModel)

if taggit:
    models.append(TaggitModel)


for model in models:
    ModelForm = autocomplete_light.modelform_factory(model,
        exclude=['for_inline', 'noise'])

    Inline = type(str('%sInline') % model.__name__, (admin.TabularInline,), {
        'form': ModelForm, 'model': model, 'fk_name': 'for_inline'})

    ModelAdmin = type(str('%sAdmin' % model.__name__), (admin.ModelAdmin,), {
        'form': ModelForm, 'inlines': [Inline]})

    admin.site.register(model, ModelAdmin)
