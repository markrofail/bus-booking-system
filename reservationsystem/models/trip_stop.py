from django.db import models


class TripStop(models.Model):
    trip_route = models.ForeignKey('reservationsystem.triproute', on_delete=models.CASCADE)
    station = models.ForeignKey('reservationsystem.busstation', on_delete=models.CASCADE)
    stop_number = models.IntegerField('stop number')

    def __str__(self):
        return f"{self.trip_route}.{self.stop_number}: {self.station}"
