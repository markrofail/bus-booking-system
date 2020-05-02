from datetime import datetime

from django.test import Client, TestCase

from .models import BusStation, Trip


class StationsEndPointTests(TestCase):
    fixtures = ['busstations']

    def testAllStations(self):
        station_count = BusStation.objects.all().count()

        response = self.client.get('/api/v1/reservationsystem/stations')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), station_count)


class TripsEndPointTests(TestCase):
    fixtures = ['busstations', 'buses', 'triproutes', 'tripstops', 'trips']

    def testQueryTrips(self):
        query_params = dict()
        query_params['date_from'] = datetime(2020, 1, 17, 0, 0, 0, 0)
        query_params['date_to'] = datetime(2020, 1, 19, 0, 0, 0, 0)

        query_params['start_station'] = BusStation.objects.get(name="Asyut").id
        query_params['end_station'] = BusStation.objects.get(name="Banha").id

        response = self.client.get('/api/v1/reservationsystem/trips', query_params)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), 1)

        trip_name = response_json[0]['name']
        self.assertEqual(trip_name, "Trip Zentry")


class ReservationEndPointTests(TestCase):
    fixtures = ['customers', 'busstations', 'buses', 'triproutes', 'tripstops', 'trips']

    def testPostReservation(self):
        token = login_as_bob()
        trip_id = Trip.objects.get(name="Trip Zentry").id

        request_headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        request_body = {"trip": trip_id}
        response = self.client.post('/api/v1/reservationsystem/reservations', request_body, **request_headers)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        bus_seat = response_json['bus_seat']
        self.assertEqual(bus_seat, "A1")


def login_as_bob():
    client = Client()

    request_body = dict(username='bob', password='loudreptile70')
    response = client.post('/api/v1/token/', request_body)

    return response.json()['access']
