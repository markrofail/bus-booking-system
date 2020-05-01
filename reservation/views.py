from datetime import datetime

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.db.models import Q, F

from .models import BusStation, Trip, BusStation
from .serializers import BusStationSerializer, TripSerializer, TripGetParamSerializer
from django import forms


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def stations_list(request):
    """
    List all BusStations
    """
    stations = BusStation.objects.all()
    serializer = BusStationSerializer(stations, many=True)
    return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class TripList(APIView):
    """
    List all Trips
    """
    def get(self, request, format=None):
        # [Step1] retreive and validate query params from request
        query_params = TripGetParamSerializer(data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)

        # [Step2] search for appropriate trips
        query_params = query_params.validated_data
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
