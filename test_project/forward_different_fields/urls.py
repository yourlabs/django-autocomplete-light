from dal import autocomplete

from django.conf.urls import url


class ListWithForwardsView(autocomplete.Select2ListView):
    def get_list(self):
        name = self.forwarded.get("name")
        checkbox = self.forwarded.get("checkbox")
        select = self.forwarded.get("select")
        select_radio = self.forwarded.get("select_radio")
        multiselect = self.forwarded.get("multiselect")
        multiselect_checks = self.forwarded.get("multiselect_checks")
        multiselect_checks_poor = self.forwarded.get("multiselect_checks_poor")
        const42 = self.forwarded.get("const42")
        reversed_name = self.forwarded.get("reverse_name")

        return [str(self.forwarded)]


urlpatterns = [
    url(
        '^forward_different_fields/$',
        ListWithForwardsView.as_view(),
        name='forward_different_fields'
    ),
]
