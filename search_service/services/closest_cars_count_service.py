from typing import Tuple
from typing import List

from geopy import distance


def calculate_closest_cars(
        cargo_coordinates: Tuple[float, float],
        cars_coordinates: List[tuple]
) -> int:
    """
    The function is designed to calculate the number of "cars" that are less than 450 miles away from the loading point.
    The load point is based on the latitude and longitude values from the Location class object to which the
    Cargo model object is linked.

    The geodesic function from the geopy library is used to calculate
    the distance in miles for each cars_coordinates object.

    The output is an integer number - the number of cars that match the given condition
    :param cargo_coordinates: A tuple consisting of latitude and longitude values.
    :param cars_coordinates: A list consisting of tuples that includes the current
    coordinates of each Car object from the database
    :return: An integer is returned
    """
    closest_cars_count: int = 0

    for car_coordinate in cars_coordinates:
        distance_dt = distance.distance(cargo_coordinates, car_coordinate).miles
        if distance_dt <= 450:
            closest_cars_count += 1

    return closest_cars_count
