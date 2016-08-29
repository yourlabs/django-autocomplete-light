from dal.autocomplete import Select2ListView

from .forms import get_choice_list


class Select2ListViewAutocomplete(Select2ListView):
    def create(self, text):
        return text

    def get_list(self):
        return get_choice_list()
