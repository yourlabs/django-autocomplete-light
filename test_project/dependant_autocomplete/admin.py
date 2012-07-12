from django.contrib import admin

import autocomplete_light

from models import Dummy
from forms import DummyForm


class DummyAdmin(admin.ModelAdmin):
    form = DummyForm
admin.site.register(Dummy, DummyAdmin)
