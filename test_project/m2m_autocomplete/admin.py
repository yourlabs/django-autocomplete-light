from django.contrib import admin

import autocomplete_light

from models import VisitedCities


class VisitedCitiesInline(admin.TabularInline):
    form = autocomplete_light.modelform_factory(VisitedCities)
    model = VisitedCities


class VisitedCitiesAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(VisitedCities)
    inlines = [VisitedCitiesInline]


admin.site.register(VisitedCities, VisitedCitiesAdmin)
