from datetime import datetime

from django.test import Client, TestCase

from .models import BusStation


class StationsEndPointTests(TestCase):
    fixtures = ['busstations']

    def testAllStations(self):
        station_count = BusStation.objects.all().count()

        response = self.client.get('/api/v1/stations')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), station_count)

class TripsEndPointTests(TestCase):
    fixtures = ['busstations', 'buses', 'triproutes', 'tripstops', 'trips']

    def testQueryTrips(self):
        query_params = dict()
        query_params['date_from'] = datetime(2020, 1, 17, 0, 0, 0, 0)
        query_params['date_to'] = datetime(2020, 1, 19, 0, 0, 0, 0)

        query_params['start_station'] = BusStation.objects.get(name="Asyut")
        query_params['end_station'] = BusStation.objects.get(name="Banha").id

        response = self.client.get('/api/v1/trips', query_params)
        print(response.json())
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), 1)
        trip_name = response_json[0]['name']
        self.assertEqual(trip_name, "Trip Zentry")
