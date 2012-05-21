from django.contrib import admin

from models import ModelGroup
from forms import ModelGroupForm


class ModelGroupAdmin(admin.ModelAdmin):
    form = ModelGroupForm
admin.site.register(ModelGroup, ModelGroupAdmin)
