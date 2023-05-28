import pytest
from decimal import Decimal

from search_service.services.cars_distance_service import get_cars_distance
from search_service.services.closest_cars_count_service import calculate_closest_cars
from search_service.tests.fixtures import car_factory, location_factory, cargo_factory

pytestmark = pytest.mark.django_db


def test_get_cars_distance():
    cargo_coordinates = (Decimal('18.418780000000000'), Decimal('-66.667900000000000'))
    cars_data = [
        ('9430R', Decimal('41.480090000000000'), Decimal('-87.729810000000000')),
        ('8874I', Decimal('45.572230000000000'), Decimal('-116.823840000000000')),
        ('2238U', Decimal('43.697970000000000'), Decimal('-85.482720000000000'))
    ]

    expected_cars_distance = [
        {'uid': '9430R', 'distance': 2017.8485455287596},
        {'uid': '8874I', 'distance': 3413.3129919186613},
        {'uid': '2238U', 'distance': 2057.3859711172377}
    ]

    cars_distance = get_cars_distance(cargo_coordinates, cars_data)

    assert cars_distance == expected_cars_distance


def test_calculate_closest_cars():
    cargo_coordinates = (Decimal('18.418780000000000'), Decimal('-66.667900000000000'))
    cars_coordinates = [
        (Decimal('18.134120000000000'), Decimal('-67.113990000000000')),
        (Decimal('45.572230000000000'), Decimal('-116.823840000000000')),
        (Decimal('18.270190000000000'), Decimal('-66.867270000000000')),
        (Decimal('42.272020000000000'), Decimal('-85.498930000000000'))
    ]

    closest_cars = calculate_closest_cars(cargo_coordinates, cars_coordinates)

    assert closest_cars == 2
