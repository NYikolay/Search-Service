import json

from django.urls import reverse

from search_service.models import Cargo
from search_service.tests.fixtures import filled_car_factory, filled_location_factory, filled_cargo_factory, api_client

import pytest

pytestmark = pytest.mark.django_db


def test_create_cargo_view(api_client, filled_location_factory):
    """
    Checking if the view works correctly with valid data.
    The output should be 201 status code and a Cargo object created in the database
    """
    endpoint = reverse('search_service:create_cargo')
    client = api_client()
    location_1 = filled_location_factory(zip=601)
    location_2 = filled_location_factory(zip=618)

    response = client.post(
        endpoint,
        {
            "weight": 123,
            "description": "test",
            "pick_up_zip": 601,
            'delivery_zip': 618
        },
        format="json"
    )

    assert response.status_code == 201
    assert Cargo.objects.filter(pick_up_location=location_1).exists()


def test_fail_zip_create_cargo_view(api_client):
    """
    Check for invalid request when pick_up_zip or delivery_zip is incorrectly passed,
    when such values do not exist in the database.
    The output should be 400 data validation error and no Cargo object in the database
    """
    endpoint = reverse('search_service:create_cargo')
    client = api_client()

    response = client.post(
        endpoint,
        {
            "weight": 123,
            "description": "test",
            "pick_up_zip": 601,
            'delivery_zip': 618
        },
        format="json"
    )

    assert response.status_code == 400
    assert not Cargo.objects.filter().exists()


def test_cargo_list_view(api_client, filled_car_factory):
    endpoint = reverse('search_service:cargos_list')
    client = api_client()

    cars = filled_car_factory.create_batch(4)

    response = client.get(endpoint)

    assert response.status_code == 200

