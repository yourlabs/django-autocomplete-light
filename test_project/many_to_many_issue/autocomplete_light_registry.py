#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : al_registry.py
#
#       Purpose :
#
#       Creation Date : Thu 28 Jan 2016 23:13:45 EET
#
#       Last Modified : Thu 28 Jan 2016 23:14:41 EET
#
#       Developer : rara_tiru  | email: tantiras@yandex.com
#
# ==============================================================================


from autocomplete_light import shortcuts as al
from many.models import Cat


class CatAutocomplete(al.AutocompleteModelBase):
    search_fields = ['name', ]
    model = Cat


al.register(Cat, CatAutocomplete)

