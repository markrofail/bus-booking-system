from django.db import models


class Reservation(models.Model):
    trip = models.ForeignKey('reservationsystem.trip', on_delete=models.CASCADE)
    customer = models.ForeignKey('users.customer', on_delete=models.DO_NOTHING)
    bus_seat = models.ForeignKey('reservationsystem.busseat', on_delete=models.DO_NOTHING, editable=False)

    departure_stop = models.ForeignKey('reservationsystem.tripstop', on_delete=models.DO_NOTHING, related_name='reservation_start')
    arrival_stop = models.ForeignKey('reservationsystem.tripstop', on_delete=models.DO_NOTHING, related_name='reservation_end')

    def __str__(self):
        return f"{self.trip} by: {self.customer} [departure:{self.departure_station}] [arrival:{self.arrival_station}]"
