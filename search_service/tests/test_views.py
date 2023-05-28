from search_service.models import Cargo, Location, Car
from search_service.tests.fixtures import car_factory, location_factory, cargo_factory, api_client

import pytest

pytestmark = pytest.mark.django_db


def test_create_cargo_view(api_client, location_factory):
    """
    Checking if the view works correctly with valid data.
    The output should be 201 status code and a Cargo object created in the database
    """
    endpoint = '/api/v1/create-cargo/'
    client = api_client()
    location_1 = location_factory(zip=601)
    location_2 = location_factory(zip=618)

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
    endpoint = '/api/v1/create-cargo/'
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


def test_cargo_list_view(api_client, car_factory, location_factory, cargo_factory):
    """
    Checking validity of CargoListView view.

    Three Location objects are created according to the following attributes:
    Distance between close_pick_up_location and car_location is known to be < 450 miles to check the condition by which:
    number of nearest cars to cargo ( =< 450 miles)
    And far_pick_up_location distance to spirit of previous Location > 450 miles

    Creating Car object in database that has a car_location and a Cargo object that has a close_pick_up_location.
    Also, another Cargo object is created that has a far_pick_up_location

    In the response we have to get 200 status code and check the following indicators:
    The number of cars closest to the close_cargo object must equal 1
    The number of nearest cars to the far_cargo object must equal 0
    """
    endpoint = '/api/v1/cargos/'
    client = api_client()

    close_pick_up_location = location_factory(latitude=18.18027, longitude=-66.75266)
    far_pick_up_location = location_factory(latitude=38.95649, longitude=-94.74304)
    car_location = location_factory(latitude=17.98892, longitude=-67.1566)

    car = car_factory(location=car_location)

    close_cargo = cargo_factory(pick_up_location=close_pick_up_location)
    far_cargo = cargo_factory(pick_up_location=far_pick_up_location)

    response = client.get(endpoint).json()

    for cargo_values in response:
        if cargo_values.get('id') == close_cargo.id:
            assert cargo_values.get('closest_cars_count') == 1
        else:
            assert cargo_values.get('closest_cars_count') == 0


def test_detail_cargo_view_set(api_client, car_factory, location_factory, cargo_factory):
    """
    Check if CargoViewSet GET method works correctly.

    The database is filled with the necessary Location, Car, Cargo objects

    The output is expected to contain such fields as weight, description, pick_up_location, delivery_location ,
    and number of cars with distance to current cargo == 2
    """
    client = api_client()

    pick_up_location = location_factory(latitude=38.95649, longitude=-94.74304)
    delivery_location = location_factory(latitude=18.18027, longitude=-66.75266)

    cargo = cargo_factory(pick_up_location=pick_up_location, delivery_location=delivery_location)

    car_factory(location=delivery_location)
    car_factory(uid='2534B', location=delivery_location)

    endpoint = f'/api/v1/cargo/{cargo.id}/'
    response = client.get(endpoint).json()

    assert response.get('weight')
    assert response.get('description')
    assert response.get('pick_up_location')
    assert response.get('delivery_location')
    assert len(response.get('cars_distance')) == 2


def test_delete_cargo_view_set(api_client, cargo_factory):
    """
    Check if DELETE method of CargoViewSet view works correctly.
    """
    client = api_client()

    cargo = cargo_factory()

    endpoint = f'/api/v1/cargo/{cargo.id}/'
    response = client.delete(endpoint)

    assert response.status_code == 204
    assert not Cargo.objects.filter().exists()


def test_put_cargo_view_set(api_client, cargo_factory):
    client = api_client()

    cargo = cargo_factory()

    endpoint = f'/api/v1/cargo/{cargo.id}/'
    response = client.put(
        endpoint,
        {
            "pick_up_location": cargo.pick_up_location,
            "delivery_location": cargo.delivery_location,
            "weight": 1122,
            "description": "Test123"
        }
    )

    assert response.status_code == 200
    assert not Cargo.objects.filter(weight=cargo.weight, description=cargo.description).exists()
    assert Cargo.objects.filter(weight=1122, description='Test123').exists()


def test_car_update_view(api_client, car_factory, location_factory):
    """
    Check if PUT method of CarUpdateView view works correctly

    Binding of the location should be performed by zip code. Hence, we create a Car object in the database with a
    random location and a Location object from which we take the zip code to bind it to the Car object to be updated.

    As a result, we check that the created Car object has been updated
    """
    client = api_client()

    car = car_factory()
    location = location_factory(zip=66103)

    endpoint = f'/api/v1/car-update/{car.uid}/'
    response = client.put(
        endpoint,
        {
            "zip_code": 66103,
            "load_capacity": 554
        }
    )
    assert response.status_code == 200
    assert not Car.objects.filter(uid=car.uid, location=car.location,load_capacity=car.load_capacity).exists()
    assert Car.objects.filter(uid=car.uid, location=location, load_capacity=554).exists()

