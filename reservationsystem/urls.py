from django.urls import path

from . import views

app_name = 'v1'
urlpatterns = [
    path('trips', views.trip_list, name='trips-list'),
    path('stations', views.stations_list, name='stations-list'),
    path('reservations', views.create_reservation, name='reservation-list'),
]
