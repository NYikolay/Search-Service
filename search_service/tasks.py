from config.celery import app
from search_service.models import Location, Car


@app.task
def update_cars_locations():
    print('......Cars locations updatind')

    random_locations = Location.objects.order_by('?')[:20]

    cars = Car.objects.all()
    for car, location in zip(cars, random_locations):
        car.location = location
        car.save()

    print('Cars locations have been updated......')

