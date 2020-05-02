from typing import Iterable

from reservationsystem.models import BusStation


def get_all_stations() -> Iterable[BusStation]:
    return BusStation.objects.all()
