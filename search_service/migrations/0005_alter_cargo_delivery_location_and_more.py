# Generated by Django 4.2.1 on 2023-05-27 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search_service', '0004_remove_car_id_alter_car_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='delivery_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_cargos', to='search_service.location'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='pick_up_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pick_up_cargos', to='search_service.location'),
        ),
    ]
