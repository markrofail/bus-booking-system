
from django.db import models


class Reservation(models.Model):
    trip = models.ForeignKey('reservationsystem.trip', on_delete=models.CASCADE)
    customer = models.ForeignKey('users.customer', on_delete=models.DO_NOTHING)
    bus_seat = models.ForeignKey('reservationsystem.busseat',
                                 on_delete=models.DO_NOTHING, editable=False)

    def __str__(self):
        return f"Reservation for: {self.trip}"

    def save(self, *args, **kwargs):
        # execute only onCreate (when id is None)
        if not self.id:
            busseat = self.trip.reserve_seat()
            self.bus_seat = busseat
        super(Reservation, self).save(*args, **kwargs)
