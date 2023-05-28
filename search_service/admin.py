from django.contrib import admin

from search_service.models import Car, Location, Cargo

admin.site.register(Car)
admin.site.register(Location)
admin.site.register(Cargo)
