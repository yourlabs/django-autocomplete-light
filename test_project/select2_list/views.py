from dal.autocomplete import Select2ListView

from .forms import get_choice_list, get_choice_list_with_id


class Select2ListViewAutocomplete(Select2ListView):
    def create(self, text):
        return text

    def get_list(self):
        return get_choice_list()


class Select2ProvidedValueListViewAutocomplete(Select2ListView):
    def create(self, text):
        return text

    def get_list(self):
        return get_choice_list_with_id()
