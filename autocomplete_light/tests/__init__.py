from django import VERSION


if VERSION < (1, 7):
    import autocomplete_light
    autocomplete_light.autodiscover()
