from django.core.management.base import BaseCommand
import pandas as pd

from search_service.models import Location


class Command(BaseCommand):
    def handle(self, **options):
        """
        Creates Location objects in the database, provided they have not been created before.
        The data to create model instances is read from the uszips.csv file using Pandas.
        Objects are created at 10,000 with batch_size to save time and use memory more efficiently.
        :param options:
        :return:
        """
        if not Location.objects.exists():
            z_codes_df = pd.read_csv('static/uszips.csv', usecols=['zip', 'lat', 'lng', 'city', 'state_name'])

            locations = [
                Location(
                    city=city,
                    state=state_name,
                    zip=zip_code,
                    latitude=lat,
                    longitude=lng
                ) for zip_code, lat, lng, city, state_name in z_codes_df.itertuples(index=False)
            ]

            Location.objects.bulk_create(locations, batch_size=10000)


