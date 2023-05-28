from django.core.exceptions import ValidationError

from rest_framework import serializers

from search_service.models import Cargo, Location, Car


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class CarDistanceSerializer(serializers.Serializer):
    uid = serializers.CharField()
    distance = serializers.FloatField()


class CreateCargoSerializer(serializers.ModelSerializer):
    pick_up_zip = serializers.IntegerField(write_only=True)
    delivery_zip = serializers.IntegerField(write_only=True)
    pick_up_location = LocationSerializer(read_only=True)
    delivery_location = LocationSerializer(read_only=True)

    class Meta:
        model = Cargo
        fields = (
            'id',
            'weight',
            'description',
            'pick_up_zip',
            'delivery_zip',
            'pick_up_location',
            'delivery_location'
        )

    def create(self, validated_data):
        obj = Cargo.objects.create(
            pick_up_location=validated_data['pick_up_location'],
            delivery_location=validated_data['delivery_location'],
            weight=validated_data['weight'],
            description=validated_data['description'],
        )
        obj.save()
        return obj

    def validate(self, attrs):
        if not Location.objects.filter(zip__in=[attrs['pick_up_zip'], attrs['delivery_zip']]).exists():
            raise ValidationError({
                'error_text': 'The entered zip code does not exist'
            })

        return attrs


class CargoListSerializer(serializers.ModelSerializer):
    closest_cars_count = serializers.IntegerField(read_only=True)
    pick_up_location = LocationSerializer(read_only=True)
    delivery_location = LocationSerializer(read_only=True)

    class Meta:
        model = Cargo
        fields = (
            'id',
            'closest_cars_count',
            'pick_up_location',
            'delivery_location',
        )


class CargoSerializer(serializers.ModelSerializer):
    pick_up_location = LocationSerializer(read_only=True)
    delivery_location = LocationSerializer(read_only=True)
    cars_distance = CarDistanceSerializer(read_only=True, many=True)

    class Meta:
        model = Cargo
        fields = (
            'id',
            'weight',
            'description',
            'pick_up_location',
            'delivery_location',
            'cars_distance'
        )


class CarUpdateSerializer(serializers.ModelSerializer):
    zip_code = serializers.IntegerField(write_only=True)
    location = LocationSerializer(read_only=True)
    uid = serializers.CharField(read_only=True)

    class Meta:
        model = Car
        fields = '__all__'
        lookup_field = "uid"

    def validate(self, attrs):
        if not Location.objects.filter(zip=attrs['zip_code']).exists():
            raise ValidationError({
                'error_text': 'The entered zip code does not exist'
            })

        return attrs


