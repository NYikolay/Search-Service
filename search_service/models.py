from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Car(models.Model):
    uid = models.CharField(max_length=5, unique=True, primary_key=True)
    location = models.ForeignKey(
        'Location',
        null=True,
        on_delete=models.SET_NULL,
        related_name='cars'
    )
    load_capacity = models.FloatField(validators=[
        MaxValueValidator(1000),
        MinValueValidator(1)
    ])

    def __str__(self):
        return f'Uid - {self.uid} | load capacity - {self.load_capacity} | location - {self.location.city}'


class Location(models.Model):
    city = models.CharField(max_length=65)
    state = models.CharField(max_length=65)
    zip = models.IntegerField()
    latitude = models.FloatField()  # рациональнее использовать Decimal() но в тестовых целях возьмём Float()
    longitude = models.FloatField()

    def __str__(self):
        return f'zip - {self.zip}, city - {self.city}, ' \
               f'state - {self.state} | lat - {self.latitude}, lng - {self.longitude}'


class Cargo(models.Model):
    pick_up_location = models.ForeignKey(
        Location,
        null=True,
        on_delete=models.SET_NULL,
        related_name='pick_up_cargos'
    )
    delivery_location = models.ForeignKey(
        Location,
        null=True,
        on_delete=models.SET_NULL,
        related_name='delivery_cargos'
    )
    weight = models.FloatField(validators=[
        MaxValueValidator(1000),
        MinValueValidator(1)
    ])
    description = models.TextField()

    def __str__(self):
        return f'From {self.pick_up_location.city} ---> {self.delivery_location.city} | weight - {self.weight}'

