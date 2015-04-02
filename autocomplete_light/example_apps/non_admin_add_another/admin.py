from django.contrib import admin

import autocomplete_light

from .models import NonAdminAddAnotherModel


class NonAdminAddAnotherModelAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(NonAdminAddAnotherModel, 
            fields=('name', 'widgets'))

admin.site.register(NonAdminAddAnotherModel, NonAdminAddAnotherModelAdmin)
