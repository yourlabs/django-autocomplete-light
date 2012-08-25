from django.contrib import admin

import autocomplete_light

from models import Trip, City, Trip_City

from django.forms.widgets import HiddenInput

class Trip_CityInline(admin.TabularInline):
    model = Trip_City
    extra = 1
    form = autocomplete_light.modelform_factory(Trip_City)
    sortable_field_name = "order"
    fields = ['city', 'order']


class TripAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Trip)
    inlines = [Trip_CityInline]

admin.site.register(Trip, TripAdmin)
admin.site.register(City)

