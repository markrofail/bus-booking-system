from django.db import models

from reservationsystem.models import BusSeat


class Trip(models.Model):
    name = models.CharField(max_length=200)
    bus = models.ForeignKey('reservationsystem.bus', on_delete=models.PROTECT)
    trip_route = models.ForeignKey('reservationsystem.triproute', on_delete=models.PROTECT)
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
