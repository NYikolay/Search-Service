from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from search_service.filters import CargoFilterBackend
from search_service.models import Cargo, Location, Car
from search_service.serializers import CreateCargoSerializer, CargoListSerializer, CargoSerializer, \
    CarUpdateSerializer
from search_service.services.closest_cars_count_service import calculate_closest_cars, get_cars_distance


class CreateCargoView(CreateAPIView):
    queryset = Cargo.objects.select_related('pick_up_location', 'delivery_location')
    serializer_class = CreateCargoSerializer

    def perform_create(self, serializer):
        zip_codes = (serializer.validated_data['pick_up_zip'], serializer.validated_data['delivery_zip'])
        locations = Location.objects.filter(zip__in=zip_codes)

        if len(locations) == 1:
            serializer.save(
                pick_up_location=locations[0],
                delivery_location=locations[0]
            )
        else:
            serializer.save(
                pick_up_location=locations[0],
                delivery_location=locations[1]
            )


class CargoListView(ListAPIView):
    cars_coordinates = Car.objects.values_list('location__latitude', 'location__longitude')
    serializer_class = CargoListSerializer
    filter_backends = [CargoFilterBackend]

    def get_queryset(self):
        # Если отправлять запрос в браузере через интерфейс DRF то он дублируется.
        # При использовании json, postman и прочее, запрос будет один.
        queryset = Cargo.objects.select_related('pick_up_location', 'delivery_location')

        for cargo in queryset:
            cargo.closest_cars_count = calculate_closest_cars(cargo, self.cars_coordinates)

        return queryset


class CargoViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Cargo.objects.select_related('pick_up_location', 'delivery_location')
    cars_data = Car.objects.values_list('uid', 'location__latitude', 'location__longitude')
    serializer_class = CargoSerializer

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
        obj.cars_distance = get_cars_distance(obj, self.cars_data)

        return obj


class CarUpdateView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarUpdateSerializer
    lookup_field = 'uid'

    def perform_update(self, serializer):
        location = Location.objects.get(zip=serializer.validated_data['zip_code'])
        serializer.save(location=location)




