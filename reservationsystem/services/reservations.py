from typing import Optional

from reservationsystem.models import Reservation, Trip
from reservationsystem.services.trips import reserve_seat, has_available_seats
from users.models import Customer


def create_reservation(trip: Trip, customer: Customer) -> Optional[Reservation]:
    """
    creates a reservation and binds it to a customer
    """
    # [Step1] check if there are seats available
    if not has_available_seats(trip):
        return

    # [Step2] create reservation
    new_reservation = Reservation(trip=trip, customer=customer)

    # [Step2.1] reserve seat to customer
    bus_seat = reserve_seat(trip)
    new_reservation.bus_seat = bus_seat

    # [Step3] return new reservation
    new_reservation.save()
    return new_reservation
