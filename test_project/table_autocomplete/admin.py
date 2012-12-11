from django.contrib import admin
from models import TableWidget

from autocomplete_light import modelform_factory


class TableWidgetAdmin(admin.ModelAdmin):
    form = modelform_factory(TableWidget)
admin.site.register(TableWidget, TableWidgetAdmin)
