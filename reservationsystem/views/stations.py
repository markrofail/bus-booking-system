from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from reservationsystem.models import BusStation
from reservationsystem.serializers import BusStationSerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def stations_list(request):
    """
    List all BusStations
    """
    stations = BusStation.objects.all()
    serializer = BusStationSerializer(stations, many=True)
    return Response(serializer.data)
