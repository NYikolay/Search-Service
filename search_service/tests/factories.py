import factory

from search_service.models import Location, Car, Cargo


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    city = factory.Faker('city')
    state = 'Puerto Rico'
    zip = 601
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car

    uid = '1234A'
    location = factory.SubFactory(LocationFactory)
    load_capacity = 152.0


class CargoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cargo

    pick_up_location = factory.SubFactory(LocationFactory)
    delivery_location = factory.SubFactory(LocationFactory)
    weight = 156.0
    description = factory.Faker('lorem')
