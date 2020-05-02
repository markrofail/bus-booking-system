from django.contrib import admin

from .models import (Bus, BusSeat, BusStation, Reservation, Trip, TripRoute,
                     TripStop)


class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ["bus_seat"]


class TripStopInline(admin.TabularInline):
    model = TripStop
    extra = 1


class TripRouteAdmin(admin.ModelAdmin):
    inlines = [TripStopInline]


class BusSeatInline(admin.TabularInline):
    model = BusSeat


class BusAdmin(admin.ModelAdmin):
    inlines = [BusSeatInline]


admin.site.register(Trip)
admin.site.register(BusStation)
admin.site.register(Bus, BusAdmin)
admin.site.register(TripRoute, TripRouteAdmin)
admin.site.register(Reservation, ReservationAdmin)
