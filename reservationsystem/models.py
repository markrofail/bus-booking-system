from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver


class BusSeat(models.Model):
    bus = models.ForeignKey('reservationsystem.Bus', on_delete=models.CASCADE, editable=False)
    order = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(63)])

    row = models.CharField(max_length=1, editable=False)
    column = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], editable=False)

    @property
    def name(self):
        return f"{self.row}{self.column}"

    def __str__(self):
        return f"{self.bus.name} {self.name}"

    def save(self, *args, **kwargs):
        # execute only onCreate (when id is None)
        if not self.id:
            # automatically compute row and column of seat before saving
            row_size = 2
            self.row = chr(ord('A') + self.order//row_size)
            self.column = (self.order % row_size) + 1

        super(BusSeat, self).save(*args, **kwargs)


class Bus(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField(default=12, editable=False)

    def __str__(self):
        return f"{self.name}: {self.capacity} seats"

@receiver(post_save, sender=Bus)
def populate_bus_seats(sender, instance, **kwargs):
    if not hasattr(instance, 'seats_set'):
        for i in range(instance.capacity):
            BusSeat.objects.create(bus=instance, order=i)

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
        return f"{self.trip_route}.{self.stop_number}: {self.station}"


class Trip(models.Model):
    name = models.CharField(max_length=200)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    trip_route = models.ForeignKey(TripRoute, on_delete=models.PROTECT)
    departure_time = models.DateTimeField('departure time')

    last_reserved_seat = models.IntegerField(default=0, editable=False)

    def has_available_seats(self):
        return self.last_reserved_seat < self.bus.capacity

    def reserve_seat(self):
        if self.has_available_seats():
            return BusSeat.objects.get(bus=self.bus, order__exact=self.last_reserved_seat)
            self.last_reserved_seat = F('last_reserved_seat') + 1
            self.save()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    customer = models.ForeignKey('users.customer', on_delete=models.DO_NOTHING)
    bus_seat = models.ForeignKey('reservationsystem.busseat', on_delete=models.DO_NOTHING, editable=False)

    def __str__(self):
        return f"Reservation for: {self.trip}"

    def save(self, *args, **kwargs):
        # execute only onCreate (when id is None)
        if not self.id:
            busseat = self.trip.reserve_seat()
            self.bus_seat = busseat
        super(Reservation, self).save(*args, **kwargs)
