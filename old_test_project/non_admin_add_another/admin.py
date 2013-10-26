from django.contrib import admin

import autocomplete_light

from models import Widget


class WidgetAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Widget)

admin.site.register(Widget, WidgetAdmin)
