import autocomplete_light
from django.contrib import admin

from .models import NonAdminAddAnotherModel


class NonAdminAddAnotherModelAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(NonAdminAddAnotherModel, 
            fields=('name', 'widgets'))

admin.site.register(NonAdminAddAnotherModel, NonAdminAddAnotherModelAdmin)
