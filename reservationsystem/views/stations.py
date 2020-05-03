from rest_framework import permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from reservationsystem.models import BusStation
from reservationsystem.services.stations import get_all_stations


class StationListApi(APIView):
    """
    List all BusStations
    """

    permission_classes = [permissions.AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BusStation
            fields = ['id', 'name']

    def get(self, request, format=None):
        stations = get_all_stations()
        serializer = self.OutputSerializer(stations, many=True)
        return Response(serializer.data)
