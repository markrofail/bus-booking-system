from django.urls import path

from . import views

app_name = 'v1'
urlpatterns = [
    path('trips', views.TripListApi.as_view(), name='trips-list'),
    path('stations', views.StationListApi.as_view(), name='stations-list'),
    path('reservations', views.ReservationCreateApi.as_view(), name='reservation-list'),
]
