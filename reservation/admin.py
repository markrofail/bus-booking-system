from django.contrib import admin

from .models import Bus, BusStation
from .models import Trip, TripRoute, TripStop
from .models import Reservation

admin.site.register(Bus)
admin.site.register(BusStation)
admin.site.register(Trip)
admin.site.register(Reservation)


class TripStopInline(admin.TabularInline):
    model = TripStop
    extra = 1


class TripRouteAdmin(admin.ModelAdmin):
    inlines = [TripStopInline]


admin.site.register(TripRoute, TripRouteAdmin)
