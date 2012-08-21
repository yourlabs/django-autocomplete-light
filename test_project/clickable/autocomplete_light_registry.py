import autocomplete_light
from clickable.models import ClickableItem

class AutocompleteClickableItem(autocomplete_light.AutocompleteModelBase):
    choice_html_format = u'''<div data-value="%(value)s">
        <a href="/admin/clickable/clickableitem/%(value)s/?_popup=1" target="_blank">
            %(label)s
            </a>
        </div>'''

autocomplete_light.register(ClickableItem,
    AutocompleteClickableItem,
    search_fields=('name',))