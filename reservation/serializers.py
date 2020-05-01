from rest_framework import serializers

from .models import BusStation


class BusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStation
        fields = ['id', 'name']