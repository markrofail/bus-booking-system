from datetime import datetime
from typing import Iterable

from django.db.models import F

from reservationsystem.models import Trip, BusStation


def get_all_trips(*, date_from: datetime, date_to: datetime, start_station: BusStation,
                  end_station: BusStation) -> Iterable[Trip]:
    trips = Trip.objects.filter(
        departure_time__gte=date_from,
        departure_time__lte=date_to,
        trip_route__tripstop__station=start_station
    ).annotate(
        start_station_number=F('trip_route__tripstop__stop_number')
    ).filter(
        trip_route__tripstop__station=end_station,
        trip_route__tripstop__stop_number__gt=F('start_station_number')
    )
    return trips
