import autocomplete_light.shortcuts as autocomplete_light

from .models import Item

autocomplete_light.register(Item,
    choices=Item.objects.filter(private=False))
