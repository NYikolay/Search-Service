import pytest

from rest_framework.test import APIClient

from search_service.tests.factories import LocationFactory, CarFactory, CargoFactory


@pytest.fixture
def location_factory():
    return LocationFactory


@pytest.fixture
def car_factory():
    return CarFactory


@pytest.fixture
def cargo_factory():
    return CargoFactory


@pytest.fixture
def api_client():
    return APIClient

