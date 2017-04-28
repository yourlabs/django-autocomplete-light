from dal import autocomplete

from django.conf.urls import url

from .models import TModel


class ListWithForwardsView(autocomplete.Select2ListView):
    def get_list(self):

        name = self.forwarded.get("name")
        checkbox = self.forwarded.get("checkbox")
        select = self.forwarded.get("select")
        select_radio = self.forwarded.get("select_radio")
        multiselect = self.forwarded.get("multiselect")
        multiselect_checks = self.forwarded.get("multiselect_checks")
        multiselect_checks_poor = self.forwarded.get("multiselect_checks_poor")

        if name == "Helen" and \
                checkbox is True and \
                select == "c" and \
                select_radio == "b" and \
                multiselect == ["b", "c"] and \
                multiselect_checks == ["a", "c"] and \
                multiselect_checks_poor == ["d"]:
            return ["It works!"]
        else:
            return ["Check another combination!"]


urlpatterns = [
    url(
        '^forward_different_fields/$',
        ListWithForwardsView.as_view(),
        name='forward_different_fields'
    ),
]
