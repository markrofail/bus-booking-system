from django.db import models


class Reservation(models.Model):
    trip = models.ForeignKey('reservationsystem.trip', on_delete=models.CASCADE)
    customer = models.ForeignKey('users.customer', on_delete=models.DO_NOTHING)
    bus_seat = models.ForeignKey('reservationsystem.busseat', on_delete=models.DO_NOTHING, editable=False)

    def __str__(self):
        return f"Reservation for: {self.trip} by: {self.customer}"
