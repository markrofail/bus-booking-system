from django.db.models import F
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from reservationsystem.models import Trip
from reservationsystem.serializers import TripSerializer, TripGetParamSerializer


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
