from autocomplete_light import shortcuts

from .models import NonIntegerPk


class NonIntegerPkForm(shortcuts.ModelForm):
    class Meta:
        model = NonIntegerPk
        exclude = []
