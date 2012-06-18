import cities_light

COUNTRIES = ('FR', 'US', 'BE', 'GB', 'ES', 'PT', 'DE', 'NL')


def filter_city_import(sender, items, **kwargs):
    if items[8] not in COUNTRIES:
        raise cities_light.InvalidItems()
cities_light.signals.city_items_pre_import.connect(filter_city_import)


def filter_region_import(sender, items, **kwargs):
    if items[0].split('.')[0] not in COUNTRIES:
        raise cities_light.InvalidItems()
cities_light.signals.region_items_pre_import.connect(filter_region_import)
