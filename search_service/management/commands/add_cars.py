import random
import string
from typing import List

from django.core.management.base import BaseCommand

from search_service.models import Location, Car


class Command(BaseCommand):
    def handle(self, **options):
        """
        Creates Car objects in the database, provided they have not been created before.

        The first thing is the formation of unique, randomly selected uid.
        By convention: a number between 1000 and 9999 + a random capital letter of the English alphabet at the end,
        example: "1234A", "2534B", "9999Z"

        Then 20 random Location objects are selected from the database

        Finally, using list comprehension and the zip() function, which combines random_uids and random_locations into
        a tuple, instances of the Car class are formed and written to the database using bulk_create
        :param options:
        :return:
        """
        if not Car.objects.exists():
            random_uids: List[str] = [
                f'{str(random.randint(1000, 9999))}{random.choice(string.ascii_uppercase)}'
                for i in range(20)
            ]
            random_uids: List[str] = random.sample(random_uids, k=len(random_uids))

            random_locations = Location.objects.order_by('?')[:20]

            cars = [
                Car(
                    uid=random_uid,
                    location=location,
                    load_capacity=random.randint(1, 1000)
                ) for random_uid, location in zip(random_uids, random_locations)
            ]

            Car.objects.bulk_create(cars)
