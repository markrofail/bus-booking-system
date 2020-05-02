from rest_framework import permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from reservationsystem.models import BusStation, Trip
from reservationsystem.services.trips import get_all_trips


class TripListApi(APIView):
    """
    Create a new Reservation
    """

    permission_classes = [permissions.AllowAny]

    class InputSerializer(serializers.Serializer):
        """
        Serializer for QueryParams validation on GET /trips
        """
        date_from = serializers.DateTimeField()
        date_to = serializers.DateTimeField()

        busstop_error_message = "invalid param format 'station_end'; use GET '/stations' to retrieve list of stations"
        error_messages = {
            "does_not_exist": busstop_error_message,
            "incorrect_type": busstop_error_message,
        }

        start_station = serializers.PrimaryKeyRelatedField(
            queryset=BusStation.objects.all(),
            error_messages=error_messages
        )
        end_station = serializers.PrimaryKeyRelatedField(
            queryset=BusStation.objects.all(),
            error_messages=error_messages
        )

        def validate(self, data):
            """
            Check that date_from is before date_to.
            """
            if data['date_from'] > data['date_to']:
                raise serializers.ValidationError("'date_to' must be later than 'date_from'")
            return data

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Trip
            fields = ['id', 'name', 'departure_time']

    def get(self, request, format=None):
        """
        List all Trips
        """
        # [Step1] retrieve and validate query params from request
        query_params = self.InputSerializer(data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)
        query_params = query_params.validated_data

        # [Step2] search for appropriate trips
        trips = get_all_trips(
            date_from=query_params['date_from'],
            date_to=query_params['date_to'],
            start_station=query_params['start_station'],
            end_station=query_params['end_station'],
        )

        # [Step3] return results
        serializer = self.OutputSerializer(trips, many=True)
        return Response(serializer.data)
