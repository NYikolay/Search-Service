# Generated by Django 4.2.1 on 2023-05-26 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_service', '0002_alter_car_load_capacity_alter_location_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='load_capacity',
            field=models.FloatField(),
        ),
    ]
