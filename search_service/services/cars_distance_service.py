from typing import List, Tuple

from geopy import distance


def get_cars_distance(cargo_coordinates: Tuple[float, float], cars_data: List[tuple]) -> List[dict]:
    """
    The function generates a list that contains a unique identifier and distance of all Cars objects
    from the database to the Cargo object passed to the function as a parameter.
    :param cargo_coordinates: A tuple consisting of latitude and longitude values.
    :param cars_data: List of unique identifiers and coordinates of Cars objects
    The list of unique identifiers and coordinates of Cars objects has the following format:
    [(uid, latitude, longitude), (uid, latitude, longitude) ....... and so on].
    :return: in the description at the top /\
    """
    car_distance_list: List[dict] = []

    for car_uid, car_latitude, car_longitude in cars_data:
        car_distance_dict: dict = {
            "uid": car_uid,
            "distance": distance.distance(cargo_coordinates, (car_latitude, car_longitude)).miles
        }
        car_distance_list.append(car_distance_dict)

    return car_distance_list

