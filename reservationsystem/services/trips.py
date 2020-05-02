from datetime import datetime
from typing import Iterable

from django.db.models import F

from reservationsystem.models import Trip, BusStation, BusSeat


def get_all_trips(*, date_from: datetime, date_to: datetime, start_station: BusStation,
                  end_station: BusStation) -> Iterable[Trip]:
    """
    [Step1] filter trips with departure time between `date_form` and `date_to`
    [Step2] filter trips with trip route that contain the `start_station` before the `end_station`
    """

    trips = Trip.objects.filter(
        departure_time__gte=date_from,
        departure_time__lte=date_to,
        trip_route__tripstop__station=start_station,
        bus__capacity__gt = F('last_reserved_seat')
    ).annotate(
        # save 1st trip stop number as `start_station_number`
        start_station_number=F('trip_route__tripstop__stop_number')
    ).filter(
        trip_route__tripstop__station=end_station,
        # compare 2nd trip stop number with `start_station_number`
        trip_route__tripstop__stop_number__gt=F('start_station_number')
    )
    return trips


def has_available_seats(trip: Trip) -> bool:
    """
    compares the trip's bus capacity with the last reserved seat number
    """
    return trip.last_reserved_seat < trip.bus.capacity


def reserve_seat(trip: Trip) -> BusSeat:
    """
    reserves a seat by incrementing `last_reserved_seat` and returning corresponding bus seat
    """
    if has_available_seats(trip):
        # [Step1] get bus_seat
        bus_seat = BusSeat.objects.get(bus=trip.bus, order__exact=trip.last_reserved_seat)

        # [Step2] increment tip's `last_reserved_seat`
        trip.last_reserved_seat = F('last_reserved_seat') + 1
        trip.save()

        # [Step3] return bus_seat
        return bus_seat
