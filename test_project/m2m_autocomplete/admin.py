from django.contrib import admin

import autocomplete_light

from models import VisitedCities


class VisitedCitiesAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(VisitedCities)
admin.site.register(VisitedCities, VisitedCitiesAdmin)
