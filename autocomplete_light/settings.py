from django.conf import settings

__all__ = ('DEFAULT_SEARCH_FIELDS',)

DEFAULT_SEARCH_FIELDS = getattr(settings,
    'AUTOCOMPLETE_LIGHT_DEFAULT_SEARCH_FIELDS',
    ('name',)
)
