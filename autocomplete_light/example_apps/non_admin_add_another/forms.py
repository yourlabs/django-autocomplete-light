import autocomplete_light.shortcuts as al

from .models import NonAdminAddAnotherModel

NonAdminAddAnotherModelForm = al.modelform_factory(NonAdminAddAnotherModel,
        exclude=[])
