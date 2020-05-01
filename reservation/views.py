from datetime import datetime

from django import forms
from django.db.models import F, Q, Count
from rest_framework import permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BusStation, Reservation, Trip
from .serializers import (BusStationSerializer, ReservationPostBodySerializer,
                          ReservationSerializer, TripGetParamSerializer,
                          TripSerializer)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def stations_list(request):
    """
    List all BusStations
    """
    stations = BusStation.objects.all()
    serializer = BusStationSerializer(stations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def trip_list(request):
    """
    List all Trips
    """
    # [Step1] retreive and validate query params from request
    query_params = TripGetParamSerializer(data=request.query_params)
    if not query_params.is_valid():
        return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)
    query_params = query_params.validated_data

    # [Step2] search for appropriate trips
    trips = Trip.objects.filter(
        departure_time__gte=query_params['date_from'],
        departure_time__lte=query_params['date_to'],
        trip_route__tripstop__station=query_params['start_station']
    ).annotate(
        start_station_number=F('trip_route__tripstop__stop_number')
    ).filter(
        trip_route__tripstop__station=query_params['end_station'],
        trip_route__tripstop__stop_number__gt=F('start_station_number')
    )

    # [Step3] return results
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_reservation(request):
    """
    Create a new Reservation
    """
    # [Step1] retreive and validate body from request
    request_body = ReservationPostBodySerializer(data=request.data)
    if not request_body.is_valid():
        return Response(request_body.errors, status=status.HTTP_400_BAD_REQUEST)
    request_body = request_body.validated_data

    # [Step2] check if trip has a free reservation
    trip_id = request_body['trip_id']
    trips = Trip.objects.annotate(
        current_reservations=Count('reservation')
    ).filter(
        id=trip_id.id,
        bus__capacity__gt=F('current_reservations'),
    )
    if not trips:
        error = 'this trip has no available seats'
        return Response({'error_message': error}, status=status.HTTP_400_BAD_REQUEST)

    # [Step3] create reservation
    new_reservation = Reservation(trip=trip_id)
    new_reservation.save()

    # [Step4] return reservation data
    serializer = ReservationSerializer(new_reservation)
    return Response(serializer.data)
    return Response(None)
