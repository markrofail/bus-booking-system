from django.contrib import admin

from .models import Bus, BusStation, BusSeat
from .models import Trip, TripRoute, TripStop
from .models import Reservation

admin.site.register(BusStation)
admin.site.register(Trip)
admin.site.register(Reservation)


class TripStopInline(admin.TabularInline):
    model = TripStop
    extra = 1


class TripRouteAdmin(admin.ModelAdmin):
    inlines = [TripStopInline]

class BusSeatInline(admin.TabularInline):
    model = BusSeat


class BusAdmin(admin.ModelAdmin):
    inlines = [BusSeatInline]


admin.site.register(Bus, BusAdmin)
admin.site.register(TripRoute, TripRouteAdmin)
