from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from search_service.filters import CargoFilterBackend
from search_service.models import Cargo, Location, Car
from search_service.serializers import CreateCargoSerializer, CargoListSerializer, CargoSerializer, \
    CarUpdateSerializer
from search_service.services.cars_distance_service import get_cars_distance
from search_service.services.closest_cars_count_service import calculate_closest_cars

from drf_spectacular.utils import extend_schema, OpenApiParameter


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
    serializer_class = CargoListSerializer
    filter_backends = [CargoFilterBackend]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="weight",
                location=OpenApiParameter.QUERY,
                description='Cargo weight',
                required=False,
                type=int
            ),
            OpenApiParameter(
                name="miles",
                location=OpenApiParameter.QUERY,
                description='Miles of the nearest cars to the Cargo. '
                            'All Cargo where the distance of Cars to that Cargo is <= miles will be output',
                required=False,
                type=int
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        # Если отправлять запрос в браузере через интерфейс DRF то SQL запросы дублируются.
        # При использовании json, postman и прочее, они дублироваться не будут.
        # Проверить можно принтом тут же
        cars_coordinates = Car.objects.values_list('location__latitude', 'location__longitude')
        queryset = Cargo.objects.select_related('pick_up_location', 'delivery_location')

        for cargo in queryset:
            cargo.closest_cars_count = calculate_closest_cars(
                (cargo.pick_up_location.latitude, cargo.pick_up_location.longitude),
                cars_coordinates
            )

        return queryset


class CargoViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Cargo.objects.select_related('pick_up_location', 'delivery_location')
    serializer_class = CargoSerializer

    def get_object(self):
        cars_data = Car.objects.values_list('uid', 'location__latitude', 'location__longitude')

        obj = get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
        obj.cars_distance = get_cars_distance(
            (obj.pick_up_location.latitude, obj.pick_up_location.longitude),
            cars_data
        )

        return obj


class CarUpdateView(UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarUpdateSerializer
    lookup_field = 'uid'

    def perform_update(self, serializer):
        location = Location.objects.get(zip=serializer.validated_data['zip_code'])
        serializer.save(location=location)




