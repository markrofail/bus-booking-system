from datetime import datetime
from typing import Iterable

from django.db.models import F, Q

from reservationsystem.models import Trip, BusStation, TripStop, Reservation, BusSeat


def get_all_trips(*, date_from: datetime, date_to: datetime, departure_station: BusStation, arrival_station: BusStation) \
        -> Iterable[Trip]:
    """
    [Step1] filter trips with departure time between `date_form` and `date_to`
    [Step2] filter trips with trip route that contain the `departure_station` before the `arrival_station`
    """
    trips = Trip.objects.filter(
        departure_time__gte=date_from,
        departure_time__lte=date_to,
        trip_route__tripstop__station=departure_station,
    ).annotate(
        # save 1st trip stop number as `start_station_number`
        start_station_number=F('trip_route__tripstop__stop_number')
    ).filter(
        trip_route__tripstop__station=arrival_station,
        # compare 2nd trip stop number with `start_station_number`
        trip_route__tripstop__stop_number__gt=F('start_station_number')
    )
    return trips


def get_available_seats(*, trip: Trip, departure_station: BusStation, arrival_station: BusStation) -> Iterable[BusSeat]:
    """
        return all non-reserved seats from `departure_station` to `arrival_station`
    """
    # [StepPre] get corresponding trip stops from bus stations
    departure_stop = TripStop.objects.get(trip_route=trip.trip_route, station=departure_station)
    arrival_stop = TripStop.objects.get(trip_route=trip.trip_route, station=arrival_station)

    # [Step1] get all seats of Trip
    all_seats = set(list(trip.bus.busseat_set.all()))

    # [Step2] get reserved seats
    reserved_seats = get_seats_reserved(trip=trip, departure_stop=departure_stop, arrival_stop=arrival_stop)
    reserved_seats = set([seat.bus_seat for seat in reserved_seats])

    # [Step3] return set difference between the two
    available_seats = all_seats - reserved_seats
    return available_seats


def has_available_seats(*, trip: Trip, departure_stop: TripStop, arrival_stop: TripStop) -> bool:
    """
    checks if there is an available seat in Trip `trip` starting `departure_stop` and ending `arrival_stop`
    """
    reservation = get_seats_reserved(trip=trip, departure_stop=departure_stop, arrival_stop=arrival_stop)
    return reservation.count() < trip.bus.capacity


def get_seats_reserved(*, trip: Trip, departure_stop: TripStop, arrival_stop: TripStop) -> Iterable[Reservation]:
    """
    get reservations where
        the departure_stop is between the query arrival_stop and departure_stop
        the arrival_stop is between the query arrival_stop and departure_stop
        the query arrival_stop and departure_stop is between the departure_stop and the arrival_stop
    """
    reservations = Reservation.objects.filter(trip=trip).filter(
        # [case1] the departure_stop is between the query arrival_stop and departure_stop
        (Q(arrival_stop__stop_number__gt=departure_stop.stop_number)
         & Q(arrival_stop__stop_number__lte=arrival_stop.stop_number)) |
        # [case2]  the arrival_stop is between the query arrival_stop and departure_stop
        (Q(departure_stop__stop_number__gte=departure_stop.stop_number)
         & Q(departure_stop__stop_number__lt=arrival_stop.stop_number)) |
        # [case3] the query arrival_stop and departure_stop is between the departure_stop and arrival_stop
        (Q(departure_stop__stop_number__lt=departure_stop.stop_number)
         & Q(arrival_stop__stop_number__gt=arrival_stop.stop_number))
    )
    return reservations
