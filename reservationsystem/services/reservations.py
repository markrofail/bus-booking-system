from typing import Optional

from reservationsystem.models import Reservation, Trip, BusStation, TripStop, BusSeat
from reservationsystem.services.trips import has_available_seats
from users.models import Customer


def create_reservation(*, trip: Trip, departure_station: BusStation, arrival_station: BusStation, bus_seat: BusSeat,
                       customer: Customer) -> Optional[Reservation]:
    """
    creates a reservation and binds it to a customer
    """
    # [StepPre] get corresponding trip stops from bus stations
    departure_stop = TripStop.objects.get(trip_route=trip.trip_route, station=departure_station)
    arrival_stop = TripStop.objects.get(trip_route=trip.trip_route, station=arrival_station)

    # [Step1] check if there are seats available
    if not has_available_seats(trip=trip, departure_stop=departure_stop, arrival_stop=arrival_stop):
        return

    departure_stop = TripStop.objects.get(trip_route=trip.trip_route, station=departure_station)
    arrival_stop = TripStop.objects.get(trip_route=trip.trip_route, station=arrival_station)

    # [Step2] create reservation
    new_reservation = Reservation(trip=trip, customer=customer, bus_seat=bus_seat,
                                  departure_stop=departure_stop, arrival_stop=arrival_stop, )

    # [Step3] return new reservation
    new_reservation.save()
    return new_reservation
