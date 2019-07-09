from dal.autocomplete import ModelSelect2

from django import forms


class TModelSelect2(ModelSelect2):
    autocomplete_function = 'tSelect2'

    @property
    def media(self):
        base_media = super(TModelSelect2, self).media
        custom_media = forms.Media(js=('t_select2.js',))
        return base_media + custom_media
