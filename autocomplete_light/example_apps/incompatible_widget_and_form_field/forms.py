import autocomplete_light.shortcuts as autocomplete_light

from .models import Film


class FilmForm(autocomplete_light.ModelForm):
    class Meta:
        model = Film
        exclude = []
