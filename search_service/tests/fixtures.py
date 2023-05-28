import pytest

from rest_framework.test import APIClient

from search_service.tests.factories import LocationFactory, CarFactory, CargoFactory


@pytest.fixture
def filled_location_factory():
    return LocationFactory


@pytest.fixture
def filled_car_factory():
    return CarFactory


@pytest.fixture
def filled_cargo_factory():
    return CargoFactory


@pytest.fixture
def api_client():
    return APIClient

