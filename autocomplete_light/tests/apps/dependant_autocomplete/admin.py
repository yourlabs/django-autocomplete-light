from django.contrib import admin

import autocomplete_light

from .models import Dummy
from .forms import DummyForm


class DummyInline(admin.TabularInline):
	model = Dummy
	form = DummyForm


class DummyAdmin(admin.ModelAdmin):
    form = DummyForm
    inlines = [DummyInline]
admin.site.register(Dummy, DummyAdmin)
