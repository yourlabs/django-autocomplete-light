import pytest
from django.urls import reverse

from .forms import TForm


@pytest.mark.django_db
def test_search(client):
    url = reverse(TForm.declared_fields['test2'].as_url(TForm).name)
    client.get(url + '?q=test+1').json()
