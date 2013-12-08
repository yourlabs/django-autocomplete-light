import autocomplete_light

from .models import NonAdminAddAnotherModel

NonAdminAddAnotherModelForm = autocomplete_light.modelform_factory(
    NonAdminAddAnotherModel)
