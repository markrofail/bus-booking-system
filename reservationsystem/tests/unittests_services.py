from django.test import TestCase

from reservationsystem.models import BusStation, Trip
from reservationsystem.services.stations import get_all_stations
from reservationsystem.services.trips import has_available_seats, reserve_seat


class StationServicesTests(TestCase):
    fixtures = ['busstations']

    def test_get_all_stations(self):
        station_count = BusStation.objects.all().count()
        result = get_all_stations()
        self.assertEqual(len(result), station_count)


class TripServicesTests(TestCase):
    fixtures = ['busstations', 'buses', 'triproutes', 'tripstops', 'trips']

    def test_has_available_seats_free(self):
        """
        check if has_available_seats() returns True if no reservations
        """
        trip_id = Trip.objects.get(pk=1)

        # check reservation_set size
        self.assertEqual(trip_id.reservation_set.count(), 0)

        # check using service method
        self.assertTrue(has_available_seats(trip_id))

    def test_reserve_seat_one(self):
        """
        check if reserve_seat({{trip}}) actually reserves a seat
        """
        trip_id = Trip.objects.get(pk=1)

        # check initial `last_reserved_seat` value
        self.assertEqual(trip_id.last_reserved_seat, 0)

        reserve_seat(trip_id)
        trip_id.refresh_from_db()

        # check new `last_reserved_seat` value
        self.assertEqual(trip_id.last_reserved_seat, 1)

    def test_reserve_seat_some(self, ):
        """
        check if reserve_seat({{trip}}) reserves n seats
        """
        num_reservations = 5
        trip_id = Trip.objects.get(pk=1)

        # check initial `last_reserved_seat` value
        self.assertEqual(trip_id.last_reserved_seat, 0)

        for i in range(num_reservations):
            reserve_seat(trip_id)
            trip_id.refresh_from_db()

        # check new `last_reserved_seat` value
        self.assertEqual(trip_id.last_reserved_seat, num_reservations)

    def test_has_available_seats_full(self, ):
        """
        check if reserve_seat({{trip}}) stops reserving at capacity
        """
        trip_id = Trip.objects.get(pk=1)
        bus_capacity = trip_id.bus.capacity
        num_reservations = 50

        # check initial `last_reserved_seat` value
        self.assertEqual(trip_id.last_reserved_seat, 0)

        for i in range(num_reservations):
            reserve_seat(trip_id)
            trip_id.refresh_from_db()

        # check new `last_reserved_seat` value
        self.assertEqual(trip_id.last_reserved_seat, bus_capacity)

    def test_reserve_seat_all(self, ):
        """
        check if reserve_seat({{trip}}) stops reserving at capacity
        """
        trip_id = Trip.objects.get(pk=1)
        bus_capacity = trip_id.bus.capacity
        num_reservations = 50

        # check initial `last_reserved_seat` value
        self.assertEqual(trip_id.last_reserved_seat, 0)

        for i in range(num_reservations):
            reserve_seat(trip_id)
            trip_id.refresh_from_db()

        # check new `last_reserved_seat` value
        self.assertEqual(trip_id.last_reserved_seat, bus_capacity)
