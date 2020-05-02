from rest_framework import serializers

from .models import BusStation, Trip, Reservation


class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = ['id', 'name']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'name', 'departure_time']


class ReservationSerializer(serializers.ModelSerializer):
    bus_seat_name = serializers.SerializerMethodField(read_only=True)

    def get_bus_seat_name(self, obj):
        return obj.bus_seat.name

    class Meta:
        model = Reservation
        fields = ['id', 'trip', 'bus_seat_name']
  
class TripGetParamSerializer(serializers.Serializer):
    """
    Serializer for QueryParams validation on GET /trips
    """
    date_from = serializers.DateTimeField()
    date_to = serializers.DateTimeField()

    busstop_error_message = "invalid param format 'station_end'; use GET '/stations' to retreive list of stations"
    error_messages={
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

class ReservationPostBodySerializer(serializers.Serializer):
    """
    Serializer for QueryParams validation on POST /reservation
    """
    trip_error_message = "invalid param format 'trip_id'; use GET '/trips' to retreive list of available trips"

    trip_id = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(),
        error_messages={
        "does_not_exist": trip_error_message,
        "incorrect_type": trip_error_message,
    })
