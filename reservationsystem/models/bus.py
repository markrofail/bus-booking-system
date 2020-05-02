from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from reservationsystem.models import BusSeat


class Bus(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField(default=12, editable=False)

    def __str__(self):
        return f"{self.name}: {self.capacity} seats"


@receiver(post_save, sender='reservationsystem.bus')
def populate_bus_seats(sender, instance, **kwargs):
    if not hasattr(instance, 'seats_set'):
        for i in range(instance.capacity):
            BusSeat.objects.create(bus=instance, order=i)
