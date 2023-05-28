from typing import List, Tuple

from rest_framework.filters import BaseFilterBackend

from search_service.models import Car

from geopy import distance


class CargoFilterBackend(BaseFilterBackend):

    @staticmethod
    def is_valid_filter_cargo(cargo, cars_coordinates: List[dict], miles: str):
        """
        The method receives as input the Cargo object, machine coordinates and query miles.
        Then it calculates the distance from each car to the current cargo using the map function.
        Then we check if any of the distances <= than query milel,
        the Cargo object is considered valid and added to the queryset
        :param cargo: An instance of the Cargo model
        :param cars_coordinates: Coordinates of all existing cars in the database
        :param miles: Query param sent by user
        :return: True or False, depending on whether the Cargo object passed validation
        """
        cargo_coordinates: Tuple[float, float] = (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude)

        cars_distance: List[int] = list(map(
            lambda car_coordinates: distance.distance(cargo_coordinates, car_coordinates).miles, cars_coordinates
        ))

        is_valid_distance: List[bool] = [car_distance <= int(miles) for car_distance in cars_distance]

        return any(is_valid_distance)

    def filter_queryset(self, request, queryset, view):
        weight = request.query_params.get('weight')
        if weight and weight.isdigit():
            queryset = queryset.filter(weight=weight)

        miles = request.query_params.get('miles')
        if miles and miles.isdigit():
            cars_coordinates = Car.objects.values_list('location__latitude', 'location__longitude')
            miles_filtered_queryset = []
            for cargo in queryset:
                if self.is_valid_filter_cargo(cargo, cars_coordinates, miles):
                    miles_filtered_queryset.append(cargo)
            queryset = miles_filtered_queryset

        return queryset
