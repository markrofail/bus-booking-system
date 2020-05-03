from datetime import datetime

from django.test import TestCase

from reservationsystem.models import BusStation, Trip, BusSeat
from reservationsystem.services.reservations import create_reservation
from reservationsystem.services.stations import get_all_stations
from reservationsystem.services.trips import get_seats_reserved, has_available_seats, get_all_trips
from users.models import Customer


# noinspection PyUnresolvedReferences
class StationServicesTests(TestCase):
    fixtures = ['busstations']

    def test_get_all_stations(self):
        station_count = BusStation.objects.all().count()
        result = get_all_stations()
        self.assertEqual(len(result), station_count)


class TripSearchServicesTests(TestCase):
    fixtures = ['customers', 'busstations', 'buses', 'triproutes', 'tripstops', 'trips']

    def test_get_all_trips(self):
        """
        check if has_available_seats() returns True if no reservations
        """
        date_from = datetime(2020, 1, 17, 0, 0, 0, 0)
        date_to = datetime(2020, 1, 19, 0, 0, 0, 0)

        start_station = BusStation.objects.get(name="Asyut")
        end_station = BusStation.objects.get(name="Banha")

        trip = get_all_trips(date_from=date_from, date_to=date_to, start_station=start_station, end_station=end_station)

        # check using service method
        self.assertEqual(len(trip), 1)
        self.assertEqual(trip[0].name, "Trip Zentry")


# noinspection PyUnresolvedReferences
class TripServicesTests(TestCase):
    fixtures = ['customers', 'busstations', 'buses', 'triproutes', 'tripstops', 'trips']

    def test_has_available_seats_free(self):
        """
        check if has_available_seats() returns True if no reservations
        """
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)

        # check using service method
        self.assertTrue(has_available_seats(trip=trip_id, departure_stop=trip_stop_a, arrival_stop=trip_stop_b))

    def test_has_available_seats_full(self):
        """
        check if reserve_seat({{trip}}) stops reserving at capacity
        """
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)

        num_reservations = 50
        bus_capacity = trip_id.bus.capacity
        customer = Customer.objects.first()

        for i in range(num_reservations):
            bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=(i % bus_capacity))
            res = create_reservation(
                trip=trip_id, bus_seat=bus_seat, customer=customer,
                departure_station=trip_stop_a.station,
                arrival_station=trip_stop_b.station,
            )

        # check new `last_reserved_seat` value
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_a,
            arrival_stop=trip_stop_b,
        ).count()
        self.assertEqual(reservations_num, bus_capacity)

    def test_has_available_seats_case1(self):
        """
        CASE 1
        Trip Route: A - B - C - D
        Reservation1: A to C
        Reservation2: B to D
        ◦----◦
          ◦----◦
        when making reservation2 it should say that the free seats = capacity - 1
        """
        # [Step1] retrieve required data
        # [Step1.1] get first trip and get its first 4 stops
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)
        trip_stop_c = trip_route.tripstop_set.get(stop_number=3)
        trip_stop_d = trip_route.tripstop_set.get(stop_number=4)

        # [Step1.2] get any customer and the first seat in the trip's  bus
        customer = Customer.objects.first()
        bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=1)

        # [Step2] reserve from A to C
        create_reservation(
            trip=trip_id, bus_seat=bus_seat, customer=customer,
            departure_station=trip_stop_a.station,
            arrival_station=trip_stop_c.station,
        )

        # [Step3] there now should be a reservation if you want to reserve from B to D
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_b,
            arrival_stop=trip_stop_d,
        ).count()
        self.assertEqual(reservations_num, 1)

    def test_has_available_seats_case2(self):
        """
        CASE 2
        Trip Route: A - B - C - D
        Reservation1: B to D
        Reservation2: A to C
          ◦----◦
        ◦----◦
        when making reservation2 it should say that the free seats = capacity - 1
        """
        # [Step1] retrieve required data
        # [Step1.1] get first trip and get its first 4 stops
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)
        trip_stop_c = trip_route.tripstop_set.get(stop_number=3)
        trip_stop_d = trip_route.tripstop_set.get(stop_number=4)

        # [Step1.2] get any customer and the first seat in the trip's  bus
        customer = Customer.objects.first()
        bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=1)

        # [Step2] reserve from A to C
        create_reservation(
            trip=trip_id, bus_seat=bus_seat, customer=customer,
            departure_station=trip_stop_b.station,
            arrival_station=trip_stop_d.station,
        )

        # [Step3] there now should be a reservation if you want to reserve from B to D
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_a,
            arrival_stop=trip_stop_c,
        ).count()
        self.assertEqual(reservations_num, 1)

    def test_has_available_seats_case3(self):
        """
        CASE 3
        Trip Route: A - B - C - D
        Reservation1: B to C
        Reservation2: A to D
          ◦--◦
        ◦------◦
        when making reservation2 it should say that the free seats = capacity - 1
        """
        # [Step1] retrieve required data
        # [Step1.1] get first trip and get its first 4 stops
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)
        trip_stop_c = trip_route.tripstop_set.get(stop_number=3)
        trip_stop_d = trip_route.tripstop_set.get(stop_number=4)

        # [Step1.2] get any customer and the first seat in the trip's  bus
        customer = Customer.objects.first()
        bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=1)

        # [Step2] reserve from A to C
        create_reservation(
            trip=trip_id, bus_seat=bus_seat, customer=customer,
            departure_station=trip_stop_b.station,
            arrival_station=trip_stop_c.station,
        )

        # [Step3] there now should be a reservation if you want to reserve from B to D
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_a,
            arrival_stop=trip_stop_d,
        ).count()
        self.assertEqual(reservations_num, 1)

    def test_has_available_seats_case4(self):
        """
        CASE 4
        Trip Route: A - B - C - D
        Reservation1: A to D
        Reservation2: B to C
        ◦------◦
          ◦--◦
        when making reservation2 it should say that the free seats = capacity - 1
        """
        # [Step1] retrieve required data
        # [Step1.1] get first trip and get its first 4 stops
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)
        trip_stop_c = trip_route.tripstop_set.get(stop_number=3)
        trip_stop_d = trip_route.tripstop_set.get(stop_number=4)

        # [Step1.2] get any customer and the first seat in the trip's  bus
        customer = Customer.objects.first()
        bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=1)

        # [Step2] reserve from A to C
        create_reservation(
            trip=trip_id, bus_seat=bus_seat, customer=customer,
            departure_station=trip_stop_a.station,
            arrival_station=trip_stop_d.station,
        )

        # [Step3] there now should be a reservation if you want to reserve from B to D
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_b,
            arrival_stop=trip_stop_c,
        ).count()
        self.assertEqual(reservations_num, 1)

    def test_has_available_seats_case5(self):
        """
        CASE 5
        Trip Route: A - B - C
        Reservation1: A to B
        Reservation2: B to C
        ◦--◦
           ◦--◦
        when making reservation2 it should say that the free seats = capacity
        """
        # [Step1] retrieve required data
        # [Step1.1] get first trip and get its first 4 stops
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)
        trip_stop_c = trip_route.tripstop_set.get(stop_number=3)

        # [Step1.2] get any customer and the first seat in the trip's  bus
        customer = Customer.objects.first()
        bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=1)

        # [Step2] reserve from A to C
        create_reservation(
            trip=trip_id, bus_seat=bus_seat, customer=customer,
            departure_station=trip_stop_a.station,
            arrival_station=trip_stop_b.station,
        )

        # [Step3] there now should be a reservation if you want to reserve from B to D
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_b,
            arrival_stop=trip_stop_c,
        ).count()
        self.assertEqual(reservations_num, 0)

    def test_has_available_seats_case6(self):
        """
        CASE 6
        Trip Route: A - B - C
        Reservation1: B to C
        Reservation2: A to B
           ◦--◦
        ◦--◦
        when making reservation2 it should say that the free seats = capacity
        """
        # [Step1] retrieve required data
        # [Step1.1] get first trip and get its first 4 stops
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)
        trip_stop_c = trip_route.tripstop_set.get(stop_number=3)

        # [Step1.2] get any customer and the first seat in the trip's  bus
        customer = Customer.objects.first()
        bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=1)

        # [Step2] reserve from A to C
        create_reservation(
            trip=trip_id, bus_seat=bus_seat, customer=customer,
            departure_station=trip_stop_b.station,
            arrival_station=trip_stop_c.station,
        )

        # [Step3] there now should be a reservation if you want to reserve from B to D
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_a,
            arrival_stop=trip_stop_b,
        ).count()
        self.assertEqual(reservations_num, 0)

    def test_has_available_seats_case7(self):
        """
        CASE 7
        Trip Route: A - B - C - D - E
        Reservation1: A to B
        Reservation2: D to E
             ◦--◦
        ◦--◦
        when making reservation2 it should say that the free seats = capacity
        """
        # [Step1] retrieve required data
        # [Step1.1] get first trip and get its first 4 stops
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)
        trip_stop_d = trip_route.tripstop_set.get(stop_number=4)
        trip_stop_e = trip_route.tripstop_set.get(stop_number=5)

        # [Step1.2] get any customer and the first seat in the trip's  bus
        customer = Customer.objects.first()
        bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=1)

        # [Step2] reserve from A to C
        create_reservation(
            trip=trip_id, bus_seat=bus_seat, customer=customer,
            departure_station=trip_stop_a.station,
            arrival_station=trip_stop_b.station,
        )

        # [Step3] there now should be a reservation if you want to reserve from B to D
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_d,
            arrival_stop=trip_stop_e,
        ).count()
        self.assertEqual(reservations_num, 0)

    def test_has_available_seats_case8(self):
        """
        CASE 8
        Trip Route: A - B - C - D - E
        Reservation1: D to E
        Reservation2: A to B
        ◦--◦
             ◦--◦
        when making reservation2 it should say that the free seats = capacity
        """
        # [Step1] retrieve required data
        # [Step1.1] get first trip and get its first 4 stops
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)
        trip_stop_d = trip_route.tripstop_set.get(stop_number=4)
        trip_stop_e = trip_route.tripstop_set.get(stop_number=5)

        # [Step1.2] get any customer and the first seat in the trip's  bus
        customer = Customer.objects.first()
        bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=1)

        # [Step2] reserve from A to C
        create_reservation(
            trip=trip_id, bus_seat=bus_seat, customer=customer,
            departure_station=trip_stop_d.station,
            arrival_station=trip_stop_e.station,
        )

        # [Step3] there now should be a reservation if you want to reserve from B to D
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_a,
            arrival_stop=trip_stop_b,
        ).count()
        self.assertEqual(reservations_num, 0)

    def test_has_available_seats_case9(self):
        """
        CASE 9
        Trip Route: A - B
        Reservation1: A to B
        Reservation2: A to B
        ◦--◦
        ◦--◦
        when making reservation2 it should say that the free seats = capacity - 1
        """
        # [Step1] retrieve required data
        # [Step1.1] get first trip and get its first 4 stops
        trip_id = Trip.objects.first()
        trip_route = trip_id.trip_route
        trip_stop_a = trip_route.tripstop_set.get(stop_number=1)
        trip_stop_b = trip_route.tripstop_set.get(stop_number=2)

        # [Step1.2] get any customer and the first seat in the trip's  bus
        customer = Customer.objects.first()
        bus_seat = BusSeat.objects.get(bus=trip_id.bus, order=1)

        # [Step2] reserve from A to C
        create_reservation(
            trip=trip_id, bus_seat=bus_seat, customer=customer,
            departure_station=trip_stop_a.station,
            arrival_station=trip_stop_b.station,
        )

        # [Step3] there now should be a reservation if you want to reserve from B to D
        reservations_num = get_seats_reserved(
            trip=trip_id,
            departure_stop=trip_stop_a,
            arrival_stop=trip_stop_b,
        ).count()
        self.assertEqual(reservations_num, 1)
