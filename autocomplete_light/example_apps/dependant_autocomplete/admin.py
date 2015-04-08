import autocomplete_light
from django.contrib import admin

from .forms import DummyForm
from .models import Dummy


class DummyInline(admin.TabularInline):
	model = Dummy
	form = DummyForm


class DummyAdmin(admin.ModelAdmin):
    form = DummyForm
    inlines = [DummyInline]
admin.site.register(Dummy, DummyAdmin)
