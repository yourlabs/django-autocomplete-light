from django.contrib import admin

from autocomplete_light import shortcuts

from .models import YourModel


class YourModelAdmin(admin.ModelAdmin):
    form = shortcuts.modelform_factory(YourModel, exclude=[])
    fields = (('name', 'relation'),('name2', 'date_and_time'))
admin.site.register(YourModel, YourModelAdmin)
