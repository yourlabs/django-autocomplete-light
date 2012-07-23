from django.contrib import admin

import autocomplete_light

from models import Trip, Trip_City


class Trip_CityInline(admin.TabularInline):
    model = Trip_City
    extra = 1
    form = autocomplete_light.modelform_factory(Trip_City)

class TripAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Trip)
    inlines = [Trip_CityInline]

admin.site.register(Trip, TripAdmin)

