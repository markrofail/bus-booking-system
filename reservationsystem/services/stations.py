from typing import Iterable

from reservationsystem.models import BusStation


def get_all_stations() -> Iterable[BusStation]:
    """
    returns all bus stations in the database
    """
    return BusStation.objects.all()
