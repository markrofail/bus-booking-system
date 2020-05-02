from rest_framework import serializers

from reservationsystem.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    bus_seat_name = serializers.SerializerMethodField(read_only=True)

    def get_bus_seat_name(self, obj):
        return obj.bus_seat.name

    class Meta:
        model = Reservation
        fields = ['id', 'trip', 'bus_seat_name']
