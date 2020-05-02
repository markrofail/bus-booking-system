from reservationsystem.models import Reservation, Trip
from users.models import Customer


def create_reservation(trip: Trip, customer: Customer) -> Reservation:
    if not trip.has_available_seats():
        return None

    # [Step3] create reservation
    new_reservation = Reservation(trip=trip, customer=customer)
    new_reservation.save()

    return new_reservation
