from autocomplete_light import shortcuts

from .models import HstoreModel


class HstoreModelForm(shortcuts.ModelForm):
    class Meta:
        model = HstoreModel
        exclude = []
