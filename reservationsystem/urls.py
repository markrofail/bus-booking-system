from django.urls import path, include

from . import views

api_v1_urls = [
    path('trips', views.TripListApi.as_view(), name='trips-list'),
    path('stations', views.StationListApi.as_view(), name='stations-list'),
    path('reservations', views.ReservationCreateApi.as_view(), name='reservation-list'),
]

app_name = 'reservationsystem'
urlpatterns = [
    path('', include((api_v1_urls, 'v1'))),
]
