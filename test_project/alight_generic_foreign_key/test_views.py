import pytest
from django.urls import reverse

from .forms import TForm


@pytest.mark.django_db
def test_search(client):
    url = reverse(TForm.declared_fields['test2'].as_url(TForm).name)
    response = client.get(url + '?q=test+1')
    assert response.status_code == 200
    assert 'text/html' in response['Content-Type']
