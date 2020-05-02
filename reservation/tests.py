from django.test import TestCase
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


# Create your tests here.
