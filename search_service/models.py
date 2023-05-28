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


class Location(models.Model):
    city = models.CharField(max_length=65)
    state = models.CharField(max_length=65)
    zip = models.IntegerField()
    latitude = models.DecimalField(max_digits=18, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)


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

