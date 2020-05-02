from rest_framework import serializers

from reservationsystem.models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'name', 'departure_time']
