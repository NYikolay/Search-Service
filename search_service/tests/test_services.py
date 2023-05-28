import pytest
from decimal import Decimal

from search_service.services.cars_distance_service import get_cars_distance
from search_service.services.closest_cars_count_service import calculate_closest_cars
from search_service.tests.fixtures import car_factory, location_factory, cargo_factory

pytestmark = pytest.mark.django_db


def test_get_cars_distance():
    cargo_coordinates = (18.41878, -66.6679)
    cars_data = [
        ('9430R', 41.48009, -87.72981),
        ('8874I', 45.57223, -116.82384),
        ('2238U', 43.69797, -85.48272)
    ]

    expected_cars_distance = [
        {'uid': '9430R', 'distance': 2017.8485455287596},
        {'uid': '8874I', 'distance': 3413.3129919186613},
        {'uid': '2238U', 'distance': 2057.3859711172377}
    ]

    cars_distance = get_cars_distance(cargo_coordinates, cars_data)

    assert cars_distance == expected_cars_distance


def test_calculate_closest_cars():
    cargo_coordinates = (18.41878, -66.6679)
    cars_coordinates = [
        (18.13412, -67.11399),
        (45.57223, -116.82384),
        (18.27019, -66.86727),
        (42.27202, -85.49893)
    ]

    closest_cars = calculate_closest_cars(cargo_coordinates, cars_coordinates)

    assert closest_cars == 2
