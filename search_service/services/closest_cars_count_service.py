from typing import List, Tuple
from geopy.distance import geodesic


def calculate_closest_cars(cargo, cars_coordinates) -> int:
    """
    The function is designed to calculate the number of "cars" that are less than 450 miles away from the loading point.
    The load point is based on the latitude and longitude values from the Location class object to which the
    Cargo model object is linked.

    The geodesic function from the geopy library is used to calculate
    the distance in miles for each cars_coordinates object.

    The output is an integer number - the number of cars that match the given condition
    :param cargo: An instance of the Cargo class.
    :param cars_coordinates: A list consisting of tuples that includes the current
    coordinates of each Car object from the database
    :return: An integer is returned
    """
    closest_cars_count: int = 0

    for car_coordinate in cars_coordinates:
        cargo_coordinates: Tuple[float, float] = (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude)

        distance: float = geodesic(cargo_coordinates, car_coordinate).miles
        if distance <= 450:
            closest_cars_count += 1

    return closest_cars_count


def get_cars_distance(cargo, cars_data) -> List[dict]:
    """
    The function generates a list that contains a unique identifier and distance of all Cars objects
    from the database to the Cargo object passed to the function as a parameter.
    :param cargo: An instance of the Cargo class.
    :param cars_data: List of unique identifiers and coordinates of Cars objects
    The list of unique identifiers and coordinates of Cars objects has the following format:
    [(uid, latitude, longitude), (uid, latitude, longitude) ....... and so on].
    :return: in the description at the top /\
    """
    car_distance_list: List[dict] = []

    cargo_coordinates: Tuple[float, float] = (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude)

    for car_uid, car_latitude, car_longitude in cars_data:
        car_distance_dict: dict = {
            "uid": car_uid,
            "distance": geodesic(cargo_coordinates, (car_latitude, car_longitude)).miles
        }
        car_distance_list.append(car_distance_dict)

    return car_distance_list
