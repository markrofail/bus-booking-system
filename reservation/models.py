from django.db import models


class Bus(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField('capacity')

    def __str__(self):
        return f"{self.name}: {self.capacity} seats"


class BusStation(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TripRoute(models.Model):
    name = models.CharField(max_length=200)
    duration = models.DurationField('duration')
    stations = models.ManyToManyField(BusStation, through='TripStop')

    def __str__(self):
        return self.name


class TripStop(models.Model):
    trip_route = models.ForeignKey(TripRoute, on_delete=models.CASCADE)
    station = models.ForeignKey(BusStation, on_delete=models.CASCADE)
    stop_number = models.IntegerField('stop number')

    def __str__(self):
        return (
            f"Stop Number:{self.stop_number} "
            f"on: {self.trip_route} "
            f"at: {self.stop_number}"
        )


class Trip(models.Model):
    name = models.CharField(max_length=200)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    trip_route = models.ForeignKey(TripRoute, on_delete=models.PROTECT)
    departure_time = models.DateTimeField('departure time')

    def hasAvailableSeats(self):
        return self.reservation_set.count() < self.bus.capacity

    def __str__(self):
        return self.name


class Reservation(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    customer = models.ForeignKey('users.customer', on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation for: {self.trip}"
