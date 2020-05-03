from django.db import models


class TripRoute(models.Model):
    name = models.CharField(max_length=200)
    duration = models.DurationField('duration')
    stations = models.ManyToManyField('reservationsystem.busstation', through='TripStop')

    def __str__(self):
        return self.name
