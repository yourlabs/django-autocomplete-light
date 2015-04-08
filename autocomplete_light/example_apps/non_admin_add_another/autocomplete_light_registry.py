import autocomplete_light.shortcuts as autocomplete_light

from .models import NonAdminAddAnotherModel

autocomplete_light.register(NonAdminAddAnotherModel,
    add_another_url_name='non_admin_add_another_model_create')
