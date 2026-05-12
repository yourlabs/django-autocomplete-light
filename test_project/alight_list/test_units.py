"""Unit tests covering the AlightGroupListView path for alight_list."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_group_list_returns_html(client):
    url = reverse('alight_group_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'text/html' in response['Content-Type']


@pytest.mark.django_db
def test_group_list_renders_group_headers(client):
    url = reverse('alight_group_list')
    response = client.get(url)
    content = response.content.decode()
    assert 'autocomplete-light-group' in content
    assert 'Tropical' in content
    assert 'Temperate' in content


@pytest.mark.django_db
def test_group_list_renders_items(client):
    url = reverse('alight_group_list')
    response = client.get(url)
    content = response.content.decode()
    assert 'data-value="mango"' in content
    assert 'data-value="apple"' in content


@pytest.mark.django_db
def test_group_list_filters_by_query(client):
    url = reverse('alight_group_list')
    response = client.get(url + '?q=man')
    content = response.content.decode()
    assert 'mango' in content
    assert 'apple' not in content
