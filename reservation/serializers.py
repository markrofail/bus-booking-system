from rest_framework import serializers

from .models import BusStation, Trip


class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = ['id', 'name']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'name', 'departure_time']


class TripGetParamSerializer(serializers.Serializer):
    """
    Serializer for QueryParams validation on GET /trips
    """
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()

    busstop_error_message = "invalid param format 'station_end'; use GET '/stations' to retreive list of stations"
    start_station = serializers.PrimaryKeyRelatedField(
        queryset=BusStation.objects.all(),
        error_messages={"does_not_exist": busstop_error_message}
    )
    end_station = serializers.PrimaryKeyRelatedField(
        queryset=BusStation.objects.all(),
        error_messages={"does_not_exist": busstop_error_message}
    )

    def validate(self, data):
        """
        Check that date_from is before date_to.
        """
        if data['date_from'] > data['date_to']:
            raise serializers.ValidationError("'date_to' must be later than 'date_from'")
        return data
