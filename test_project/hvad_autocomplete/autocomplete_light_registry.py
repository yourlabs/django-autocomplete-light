from autocomplete_light.contrib.hvad import register#, HvadAutocompleteModelBase
from .models import Category

### simple way if you only need one language
register(Category, search_fields=('name',),
         autocomplete_js_attributes={'placeholder': 'category ..'},
         lang='de')

### more sophisticated way, where lang is set in javascript
# class CategoryAutocomplete(HvadAutocompleteModelBase):
#     search_fields = ('name', )
#     autocomplete_js_attributes={'placeholder': 'category ..'}

# register(Category, CategoryAutocomplete)
