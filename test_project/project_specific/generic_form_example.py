import autocomplete_light

from models import TaggedItem

class TaggedItemForm(autocomplete_light.GenericModelForm):
    content_object = autocomplete_light.GenericForeignKeyField(
        widget=autocomplete_light.AutocompleteWidget(
            'MyGenericChannel', max_items=1))

    class Meta:
        model = TaggedItem
        exclude = (
            'content_type',
            'object_id',
        )
