from django.urls import re_path as url

from dal import autocomplete


class ListWithForwardsView(autocomplete.AlightListView):
    def get_list(self):
        self.forwarded.get("name")
        self.forwarded.get("checkbox")
        self.forwarded.get("select")
        self.forwarded.get("select_radio")
        self.forwarded.get("multiselect")
        self.forwarded.get("multiselect_checks")
        self.forwarded.get("multiselect_checks_poor")
        self.forwarded.get("const42")
        self.forwarded.get("reverse_name")

        return [str(self.forwarded)]


urlpatterns = [
    url(
        '^alight_forward_different_fields/$',
        ListWithForwardsView.as_view(),
        name='alight_forward_different_fields',
    ),
]
