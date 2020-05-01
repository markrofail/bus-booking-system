from django.urls import path

from . import views

app_name = 'v1'
urlpatterns = [
    path('stations', views.stations_list, name='stations-list'),
]
